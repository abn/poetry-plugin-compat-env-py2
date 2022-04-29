from __future__ import annotations

import json
import logging
import textwrap

from pathlib import Path
from typing import TYPE_CHECKING
from typing import Callable

from packaging.tags import Tag
from poetry.plugins.plugin import Plugin
from poetry.utils.env import VirtualEnv


if TYPE_CHECKING:
    from cleo.io.io import IO
    from poetry.poetry import Poetry


logger = logging.getLogger("poetry-plugin-compat-env-py2")
original_get_supported_tags: Callable[
    [VirtualEnv], list[Tag]
] = VirtualEnv.get_supported_tags


def get_supported_tags(self: VirtualEnv) -> list[Tag]:
    if self.get_version_info() >= (3, 0, 0):
        # this is not a python 2.7 environment
        return original_get_supported_tags(self)

    logger.debug(
        "Python 2 environment detected, using patched logic to retrieve system tags"
    )

    script = (
        Path(__file__)
        .parent.joinpath("vendored")
        .joinpath("tags.py.include")
        .read_text()
    )

    script = script.replace(
        "from ._typing import TYPE_CHECKING, cast",
        "TYPE_CHECKING = False\ncast = lambda type_, value: value",
    )
    script = script.replace(
        "from ._typing import MYPY_CHECK_RUNNING, cast",
        "MYPY_CHECK_RUNNING = False\ncast = lambda type_, value: value",
    )

    script += textwrap.dedent(
        """
        import json

        print(json.dumps([(t.interpreter, t.abi, t.platform) for t in sys_tags()]))
        """
    )

    output = self.run_python_script(script)

    return [Tag(*t) for t in json.loads(output)]


class CompatEnvPy2Plugin(Plugin):  # type: ignore[misc]
    def activate(self, poetry: Poetry, io: IO) -> None:
        VirtualEnv.get_supported_tags = get_supported_tags
