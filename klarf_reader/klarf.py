from pathlib import Path
from typing import List, Tuple

from .models.klarf_content import KlarfContent

from .readers import klarf_file_reader


class Klarf:
    @staticmethod
    def load_from_file(filepath: Path) -> KlarfContent:
        return klarf_file_reader.readKlarf(klarf=filepath)[0]

    @staticmethod
    def load_from_file_with_raw_content(
        filepath: Path,
    ) -> Tuple[KlarfContent, List[str]]:
        return klarf_file_reader.readKlarf(klarf=filepath)

    def __repr__(self):
        print(self.__dict__)
