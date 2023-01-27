The klarf-reader library is a python 3 lib that allow to parse and get klarf content as dataclass.

** Installing Karf-Reader

To install klarf-reader, if you already have Python, you can install with:

'''
pip install klarf-reader
'''

** How to import Karf-Reader

To access klarf-reader ansd its functions import it in yout Python code like this:

'''
from klarf_reader.klarf import Klarf
'''

** Reading the example code

To reader a klarf klarf you just have to give the klarf path and klarf-reader will return you an instance of KlarfContent that contains information from klarf file.

'''
path = Path('wd') / 'my_klarf_file'

content = Klarf.load_from_file(filepath=path)
'''
