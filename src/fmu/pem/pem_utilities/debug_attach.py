"""Helper for attaching a remote debugger (debugpy) from inside RokDoc."""

from __future__ import annotations

import contextlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

import debugpy

DEFAULT_PYTHON = sys.executable
DEFAULT_HOST = "localhost"
DEFAULT_PORT = 5678
DEFAULT_LOG_FILE = Path("/tmp/debug_attach.log")

_LISTENER_STARTED = False


def _notify(message: str, log_file: Path | None) -> None:
    """Surface a status message via stderr, a log file, and a desktop popup.

    Embedded Python hosts (e.g. RokDoc via JEP) frequently swallow stdout,
    so we fan out to several channels to make sure the user sees it.
    """
    # 1. Unbuffered stderr — usually visible even when stdout is captured.
    with contextlib.suppress(Exception):
        print(message, file=sys.stderr, flush=True)

    # 2. Log file — guaranteed visible via ``tail -f``.
    if log_file is not None:
        with contextlib.suppress(OSError), log_file.open("a") as fh:
            fh.write(message + "\n")

    # 3. Desktop popup, if a notifier is available.
    for cmd in (
        ["notify-send", "debugpy", message],
        ["zenity", "--info", "--no-wrap", f"--text={message}"],
        ["kdialog", "--passivepopup", message, "10"],
        ["xmessage", "-timeout", "10", message],
    ):
        if shutil.which(cmd[0]) is None:
            continue
        try:
            subprocess.Popen(  # noqa: S603
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except OSError:
            continue
        break


def wait_for_debugger(
    python: str = DEFAULT_PYTHON,
    host: str = DEFAULT_HOST,
    port: int = DEFAULT_PORT,
    break_on_attach: bool = True,
    log_file: Path | None = DEFAULT_LOG_FILE,
    port_fallback_count: int = 10,
) -> None:
    """Start a debugpy listener and block until VS Code attaches.

    Safe to call multiple times. The listener is bound only on the first
    call; subsequent calls reuse it and wait for a fresh attach.

    If ``port`` is already in use (typical when a previous process just
    released it and the socket is still in TIME_WAIT), the next
    ``port_fallback_count`` ports are tried in order. The chosen port is
    reported via :func:`_notify` so the user knows which one to attach to.
    """
    global _LISTENER_STARTED

    if debugpy.is_client_connected():
        # A client is still attached – just drop into a breakpoint.
        if break_on_attach:
            debugpy.breakpoint()
        return

    if not _LISTENER_STARTED:
        debugpy.configure(python=python)
        last_exc: Exception | None = None
        for candidate in range(port, port + port_fallback_count + 1):
            try:
                debugpy.listen((host, candidate))
                port = candidate
                _LISTENER_STARTED = True
                break
            except Exception as exc:  # noqa: BLE001
                last_exc = exc
        if not _LISTENER_STARTED:
            _notify(
                f"⚠ debugpy.listen({host}:{port}..+{port_fallback_count}) "
                f"failed: {last_exc!r}",
                log_file,
            )
            return

    _notify(
        f"⏸ Waiting for debugger to attach on {host}:{port} (pid {os.getpid()})",
        log_file,
    )
    debugpy.wait_for_client()
    _notify(f"▶ Debugger attached on {host}:{port}", log_file)

    if break_on_attach:
        debugpy.breakpoint()
