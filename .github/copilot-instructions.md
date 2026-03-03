# GitHub Copilot Instructions for fmu-pem

## Project overview

`fmu-pem` is a petro-elastic model (PEM) library for use in FMU (Fast Model
Update) seismic history matching workflows, typically as an ERT forward model
step preceding `fmu-sim2seis`. It reads Eclipse simulation output, applies rock
physics models, and writes elastic property grids.

The package is structured as a PEP 420 implicit namespace package under
`src/fmu/pem/` and is installed as the `pem` console script.

---

## Repository layout

```
src/fmu/pem/
  __main__.py                  # CLI entry point
  run_pem.py                   # Top-level orchestration
  forward_models/pem_model.py  # ERT ForwardModelStepPlugin
  hook_implementations/jobs.py # ERT hook registrations
  pem_functions/               # Rock physics calculation functions
  pem_utilities/               # Config parsing, pydantic models, I/O helpers
tests/
  conftest.py                  # Session-scoped fixtures; copies test data to tmp
  data/                        # Static test data (Eclipse files, YAML configs)
.github/
  workflows/build_test_deploy.yml
```

---

## Language and runtime

- **Python ≥ 3.11** is required; use modern type annotations (`X | Y`,
  `list[X]`, `tuple[X, Y]`).
- All source files must be compatible with the Python versions tested in CI
  (`3.11`, `3.12`).

---

## Code style

- **Formatter**: `ruff format` (line length 88, `skip-magic-trailing-comma =
  false`). Always run before committing.
- **Linter**: `ruff check` with rules `C, E, F, I, PIE, Q, RET, RSE, SIM, W`.
  `C901` (complexity) and `F401` (unused imports) are ignored.
- **Pre-commit hooks** enforce both automatically on every commit; never bypass
  them.
- Do **not** introduce `print` statements in production code; use logging or
  raise exceptions.
- Prefer explicit `Path` operations over string concatenation for file paths.

---

## Pydantic validation patterns

Config models live in `src/fmu/pem/pem_utilities/pem_config_validation.py` and
are validated via `read_pem_config` in `import_config.py`.

### Key conventions

- Use plain `Path` for all path fields — **never** `DirectoryPath` or
  `FilePath`. Existence checks must be implemented as explicit `model_validator`
  or `field_validator` methods so they can be made conditional.
- All filesystem-checking validators must inspect the pydantic validation
  context for the `pre_experiment` flag:

  ```python
  @model_validator(mode="after")
  def check_paths_exist(self, info: ValidationInfo) -> Self:
      pre_experiment = (
          info.context.get("pre_experiment", False) if info.context else False
      )
      if pre_experiment:
          return self
      # ... existence checks ...
      return self
  ```

- Pass the flag through via `model_validate`:

  ```python
  PemConfig.model_validate(data, context={"pre_experiment": pre_experiment})
  ```

- **Rationale**: at ERT's `validate_pre_experiment` stage the per-realization
  directory tree does not yet exist. Passing `pre_experiment=True` suppresses
  realization-specific filesystem checks while all non-path validators
  (type checks, numeric ranges, FIPNUM/PVTNUM overlap detection, etc.) still
  run.

---

## ERT forward model conventions

`pem_model.py` implements `ForwardModelStepPlugin` from the `ert` package.

- `validate_pre_realization_run`: lightweight — return `fm_step_json` unchanged
  unless there is a fast, non-filesystem check to perform.
- `validate_pre_experiment`: call `read_pem_config(..., pre_experiment=True)`.
  Never perform filesystem checks here; realization directories do not exist
  yet.
- Raise `ForwardModelStepValidationError` (never a bare exception) when
  validation fails in either hook.

---

## Testing

- Test framework: **pytest** with session-scoped `data_dir` fixture
  (`conftest.py`) that copies `tests/data/` into a temporary directory and
  pre-creates required output directories.
- Use `monkeypatch.chdir` to simulate the working directory of a realization.
- Use `tmp_path` (function-scoped) for tests that need a bare directory without
  realization subdirectories (e.g. `pre_experiment` tests).
- Use `pytest.raises(Exception)` to assert that filesystem checks fail when
  directories are absent; prefer tightening to a specific exception type when
  known.
- Test files are named `test_<module>.py`. Keep tests focused on a single
  behaviour per function.
- Tests that require the internal Equinor `rock-physics` package must be
  guarded with `if INTERNAL_EQUINOR`.

---

## Commits and pull requests

- Use **Conventional Commits**: `fix:`, `feat:`, `refactor:`, `test:`,
  `chore:`, `docs:` prefixes. Add a scope in parentheses where helpful, e.g.
  `fix(ert):`, `refactor(validation):`.
- Each commit must be **atomic** — one logical change per commit.
- Every commit must pass all pre-commit hooks before being pushed.
- PR descriptions must include a **Problem**, **Solution**, and per-commit
  **Changes** section.

---

## Dependencies

Core runtime dependencies are declared in `pyproject.toml` under
`[project.dependencies]`. Do not add new dependencies without updating
`pyproject.toml`; avoid pinning to exact versions in the package metadata
(use `>=` lower bounds).

Test-only dependencies belong under `[project.optional-dependencies] tests`.
