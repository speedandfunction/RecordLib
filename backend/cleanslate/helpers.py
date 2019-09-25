import zipfile
import BytesIO
from typing import List
import secrets
from RecordLib.petitions import Petition
from docxtpl import DocxTemplate
from contextlib import contextmanager

def random_temp_directory() -> str:
    """
    return a random name for a temporary directory.
    """
    alphabet = string.ascii_letters
    return ''.join(secrets.choice(alphabet) for i in range(30))


class Compresser:

    def __init__(self, files: List[Tuple[str, DocxTemplate]] = None):
        self.__buffer__ = BytesIO.BytesIO()
        self.archive = zipfile.ZipFile(self.__buffer__, mode='wb')
        base = os.path.dirname(os.path.abspath(__file__))
        while True:
            # Make sure the new directory we're creating to temporarily 
            # store files does not exist.
            self.__rootdir__ = os.path.join(base, "tmp", random_temp_directory())
            if not os.path.exists(self.__rootdir__):
                os.path.makedirs(self.__rootdir__)
                break

        if files is not None:
            for fname, f in files:
                self.append(fname, f)
    

    def append(self, filename, file) -> None:
        """
        Add 'file' to this zip archive
        
        TODO this should be done in membory somehow.
        """
        filepath = os.path.join(self.__rootdir__, filename)
        file.save(filepath)
        self.archive.write(filepath)

    def delete_dir() -> None:
        """ Delete the directory where all the files were temporarily written
        """
        os.rmtree(self.__rootdir__)

    def save(filename: str) -> str:
        """
        Save the archive to the temporary directory, and
        return the path to it.
        """
        path = os.path.join(self.__rootdir__, filename)
        with open(path, 'wb') as z:
            z.write(self.__buffer__)
        