from pathlib import Path

from models.klarf_content import KlarfContent

from readers import klarf_file_reader


class Klarf:
    @staticmethod
    def load_from_file(filepath: Path) -> KlarfContent:
        return klarf_file_reader.readKlarf(klarf=filepath)

    def __repr__(self):
        print(self.__dict__)
