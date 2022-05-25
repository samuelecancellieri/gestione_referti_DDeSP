#system import
import os

def elimina_documento(path_documento):
    try:
        os.remove(path_documento)
    except OSError as e:
        raise e
    else:
        return True
