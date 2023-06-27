from pathlib import Path
from typing import List, Tuple

from .models.klarf_content import KlarfContent

from .readers import klarf_file_reader


class Klarf:
    @staticmethod
    def load_from_file(
        filepath: Path,
        custom_columns_wafer: List[str] = None,
        custom_columns_defect: List[str] = None,
    ) -> KlarfContent:
        return Klarf.load_from_file_with_raw_content(
            filepath=filepath,
            custom_columns_wafer=custom_columns_wafer,
            custom_columns_defect=custom_columns_defect,
        )[0]

    @staticmethod
    def load_from_file_with_raw_content(
        filepath: Path,
        custom_columns_wafer: List[str] = None,
        custom_columns_defect: List[str] = None,
    ) -> Tuple[KlarfContent, List[str]]:
        return klarf_file_reader.readKlarf(
            klarf=filepath,
            custom_columns_wafer=custom_columns_wafer,
            custom_columns_defect=custom_columns_defect,
        )

    def __repr__(self):
        print(self.__dict__)
