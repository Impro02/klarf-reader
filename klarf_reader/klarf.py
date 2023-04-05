from pathlib import Path
from typing import List, Tuple

from .models.klarf_content import KlarfContent

from .readers import klarf_file_reader


class Klarf:
    @staticmethod
    def load_from_file(
        filepath: Path,
        custom_columns_lot: List[str] = None,
        custom_columns_defects: List[str] = None,
    ) -> KlarfContent:
        return Klarf.load_from_file_with_raw_content(
            filepath=filepath,
            custom_columns_lot=custom_columns_lot,
            custom_columns_defects=custom_columns_defects,
        )[0]

    @staticmethod
    def load_from_file_with_raw_content(
        filepath: Path,
        custom_columns_lot: List[str] = None,
        custom_columns_defects: List[str] = None,
    ) -> Tuple[KlarfContent, List[str]]:
        return klarf_file_reader.readKlarf(
            klarf=filepath,
            custom_columns_lot=custom_columns_lot,
            custom_columns_defects=custom_columns_defects,
        )

    def __repr__(self):
        print(self.__dict__)
