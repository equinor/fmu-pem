# Remote debugging with `debugpy`

`fmu-pem` ships a small helper, `pem_utilities.debug_attach.wait_for_debugger`,
that lets you attach VS Code's Python debugger to a running `pem` process
(typically one launched by ERT). This page documents how to use it.

## Why a remote debugger?

When `pem` runs as an ERT forward model step it is launched as a fresh
subprocess in a realisation directory. You cannot just press F5 in VS Code to
debug it because the process is started by ERT, not by VS Code. Instead, the
process opens a debug *server*, blocks until VS Code connects to it, and only
then continues execution.

`wait_for_debugger()` may be called more than once — either at several points
in a single process, or in different processes within the same ERT run (for
example two consecutive forward-model steps). Each call produces its own
attach session, so debugging *N* breaks requires *N* attaches. **NB! Make
sure that debugging is not attempted in ensemble runs with several
realizations**.

## Inserting the call

Call `wait_for_debugger()` from anywhere in the `pem` code path you want to
break into:

```python
from fmu.pem.pem_utilities.debug_attach import wait_for_debugger

wait_for_debugger()  # blocks until VS Code attaches
```

The helper:

- starts a `debugpy` listener on `localhost:5678` (port-fallback up to 5688),
- fans out a "waiting for debugger" notification to **stderr**, the log file
  `/tmp/debug_attach.log`, and a desktop popup (`notify-send`, `zenity`,
  `kdialog`, or `xmessage`, whichever is available),
- blocks on `debugpy.wait_for_client()`,
- emits a second notification once VS Code has attached, and
- drops into `debugpy.breakpoint()` so execution pauses on the next line.

## Required `launch.json` setup

Add the following to `.vscode/launch.json` in the workspace from which you
debug. The `inputs` block lets VS Code ask which port to attach to each time
you press F5, which is necessary because the second `pem` process picks the
next free port when 5678 is still in `TIME_WAIT`.

```jsonc
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Debug Server (prompt for port)",
            "type": "debugpy",
            "request": "attach",
            "connect": {
                "host": "localhost",
                "port": "${input:debugPort}"
            },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}",
                    "remoteRoot": "."
                }
            ],
            "justMyCode": false
        }
    ],
    "inputs": [
        {
            "id": "debugPort",
            "type": "promptString",
            "description": "debugpy port (see /tmp/debug_attach.log)",
            "default": "5678"
        }
    ]
}
```

## Workflow for an ERT run

The sequence below describes what to expect when `wait_for_debugger()` is
reached more than once during an ERT run (either multiple breaks in the same
process, or one break each in two consecutive forward-model steps).

1. Start the ERT run as usual.
2. When the first `wait_for_debugger()` call is reached you see a popup like
   `⏸ Waiting for debugger to attach on localhost:5678 (pid …)`. Note the
   port (also written to `/tmp/debug_attach.log`).
3. In VS Code, pick **Python: Debug Server (prompt for port)** from the
   Run-and-Debug dropdown, press F5, and enter the port (`5678` for the
   first break). Debug normally.
4. When you are done with that session, click the **Disconnect** button (the
   plug icon) in the VS Code debug toolbar. **This step is required** —
   `debugpy` only allows one client at a time, so the next break cannot
   accept a connection until you detach.
5. The next `wait_for_debugger()` call writes a second line to the log,
   typically with port `5679` because `5678` is still in `TIME_WAIT` on Linux
   (within the same process the original port is reused). Note the port
   shown in the log.
6. Press F5 again and enter that port when prompted.

You can monitor the log live in a separate terminal:

```bash
tail -f /tmp/debug_attach.log
```

## Behaviour notes

- The helper is safe to call multiple times within the same process; the
  listener is bound only once and subsequent calls reuse it.
- If port `5678` is occupied the helper tries `5679`, `5680`, …, up to ten
  ports above the default. The chosen port is reported in the notification
  channels.
- If a desktop notifier is unavailable (e.g. no `$DISPLAY` on a compute node),
  the helper silently falls back to stderr and the log file.
- The log file path can be overridden via the `log_file=` argument, or
  disabled by passing `log_file=None`.
- If the forward model runs on a different host than your workstation
  (LSF/SLURM), `localhost:567X` refers to the **compute node**, not your
  workstation. You then need an SSH tunnel, or to bind the listener to
  `0.0.0.0` and attach using the node's hostname.
