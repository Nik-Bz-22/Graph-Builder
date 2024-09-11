import pathlib
from typing import Final


ROOT_DIR: Final[pathlib.Path] = pathlib.Path(__file__).parents[2]
RESOURCE_FILE: Final[pathlib.Path] = ROOT_DIR.joinpath("resource")