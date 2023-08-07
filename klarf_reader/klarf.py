# MODULES
from pathlib import Path
from typing import Generator, List, Tuple

# MODELS
from .models.klarf_content import KlarfContent

# READERS
from .readers import klarf_file_reader


class Klarf:
    @staticmethod
    def load_from_file(
        filepath: Path,
        custom_columns_wafer: List[str] = None,
        custom_columns_defect: List[str] = None,
        parse_summary: bool = True,
        defects_as_generator: bool = False,
    ) -> KlarfContent:
        klarf_content, _ = Klarf.load_from_file_with_raw_content(
            filepath=filepath,
            custom_columns_wafer=custom_columns_wafer,
            custom_columns_defect=custom_columns_defect,
            parse_summary=parse_summary,
            defects_as_generator=defects_as_generator,
        )

        return klarf_content

    @staticmethod
    def load_from_file_with_raw_content(
        filepath: Path,
        custom_columns_wafer: List[str] = None,
        custom_columns_defect: List[str] = None,
        parse_summary: bool = True,
        defects_as_generator: bool = False,
    ) -> Tuple[KlarfContent, Generator[str, None, None],]:
        return klarf_file_reader.readKlarf(
            klarf=filepath,
            custom_columns_wafer=custom_columns_wafer,
            custom_columns_defect=custom_columns_defect,
            parse_summary=parse_summary,
            defects_as_generator=defects_as_generator,
        )

    def __repr__(self):
        print(self.__dict__)
