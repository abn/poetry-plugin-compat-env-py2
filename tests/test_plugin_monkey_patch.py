from __future__ import annotations

from poetry.utils.env import VirtualEnv

from poetry_plugin_compat_env_py2.plugins import CompatEnvPy2Plugin
from poetry_plugin_compat_env_py2.plugins import get_supported_tags


def test_plugin_monkey_patch_on_activate() -> None:
    plugin = CompatEnvPy2Plugin()
    original = VirtualEnv.get_supported_tags

    assert original != get_supported_tags

    plugin.activate(None, None)

    assert VirtualEnv.get_supported_tags == get_supported_tags
