# Poetry Plugin: Python 2 Environment Compatibility Patch

This is a rudimentary Poetry plugin to allow users impacted by [changes in Poetry 1.2.0](https://github.com/python-poetry/poetry/issues/4752)
that removes support for management of Python 2.7 project environments.

Compatibility is maintained by vendoring an older version of [`tags.py`](src/poetry_plugin_compat_env_py2/vendored/README.md)
for execution via monkey patching `poetry.utils.env.VirtualEnv.get_supported_tags` method.

Once installed and activated, plugin auto-detects a Python 2.7 environment when discovering tags.

## Installation

The easiest way to install the `compat-env-py2` plugin is via the `self add` command of Poetry.

```bash
poetry self add poetry-plugin-compat-env-py2
```

If you used `pipx` to install Poetry you can add the plugin via the `pipx inject` command.

```bash
pipx inject poetry poetry-plugin-compat-env-py2
```

Otherwise, if you used `pip` to install Poetry you can add the plugin packages via the `pip install` command.

```bash
pip install poetry-plugin-compat-env-py2
```
