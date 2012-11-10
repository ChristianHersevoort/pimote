import os
import logging
import hashlib

logger = logging.getLogger(__file__)

from settings import *
from models import db, File

class LibraryScanner:

    __extension_white_list = set([".mp4", '.mkv', '.txt'])

    def __init__(self):
        pass

    def scan(self):
        for dir in LIBRARY_DIRECTORIES:
            self.__recursive_scan(dir, root=None)

        #commit changes
        db.session.commit()

    def __recursive_scan(self, dir, root):
        try:

            dir_hash = self.__get_hash(dir)
            dir_name = os.path.basename(dir)
            logger.debug("scanning dir %s with hash %s" % (dir, dir_hash))

            dir_query = File.query.filter_by(hash=dir_hash).first()
            if dir_query is None:
                logger.debug("New directory found!")
                new_dir = File(dir_name, dir, dir_hash, root, is_dir=True)
                db.session.add(new_dir)

            for item in os.listdir(dir):
                #call the sub dirs recursively
                if os.path.isdir(os.path.join(dir, item)):
                    self.__recursive_scan(os.path.join(dir, item), dir_hash)
                    continue

                self.__add_file(os.path.join(dir, item), dir_hash)
        except OSError, e:
            logger.warn("Failed to scan directory '%s' with message '%s'" % (dir, e.strerror))

    def __get_hash(self, string):
        """Generates sha1 hash of a string"""
        hash = hashlib.sha1()
        hash.update(string)
        return hash.hexdigest()

    def __add_file(self, file_path, root):

        filename = os.path.basename(file_path)
        name, extension = os.path.splitext(filename)

        if extension == "":
           return

        if not self.__extension_white_list.__contains__(extension):
            logger.debug("Ignoring file '%s' with extension '%s'" % (filename, extension))
            return

        file_hash = self.__get_hash(file_path)

        file_query = File.query.filter_by(hash=file_hash).first()
        if file_query is None:
            logger.debug("New file found: '%s'" % filename)
            new_file = File(filename, file_path , file_hash, root=root)
            db.session.add(new_file)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s] %(message)s')


    #Create SQLite database if it doesn't exist
    if not os.path.isfile(DATABASE_FILE):
        db.create_all()


    l = LibraryScanner()
    l.scan()






