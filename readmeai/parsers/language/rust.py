"""
Parser for Rust cargo.toml dependency files.
"""

import sys
from typing import List

from readmeai.core.parsers import BaseFileParser

if sys.version_info < (3, 11):
    import toml
else:
    import tomllib as toml


class CargoTomlParser(BaseFileParser):
    """Parser for Rust cargo.toml dependency files."""

    def __init__(self) -> None:
        """Initializes the handler with given configuration."""
        super().__init__()

    def parse(self, content: str) -> List[str]:
        """Extract packages names from Rust TOML files."""
        try:
            data = toml.loads(content)
            dependencies = []

            if "dependencies" in data:
                dependencies.extend(data["dependencies"].keys())
            if "dev-dependencies" in data:
                dependencies.extend(data["dev-dependencies"].keys())

            for key in data:
                if key.startswith("dependencies.") and isinstance(
                    data[key], dict
                ):
                    dependencies.extend(data[key].keys())

            return dependencies

        except toml.TomlDecodeError as exc:
            return self.handle_parsing_error(f"cargo.toml: {str(exc)}")
