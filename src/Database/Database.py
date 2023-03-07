from typing import Literal
# Import python libraries
import pandas as pd
import os

class Database:
    def __init__(self, path:str, extension:Literal[".csv"] | None = '.xlsx') -> None:
        # local dict db
        self.db = {}

        # Construct local dict db walking in path
        for root, dirs, files in os.walk(path):
            for file in files:
                # verify files with xlsx extension
                if file.endswith(extension) and extension == '.xlsx':
                    # get the full path of the file
                    filepath = os.path.join(root, file)
                    df = pd.read_excel(filepath, dtype='str', engine='openpyxl')
                    # Update local dict db with {key:'file_name'(without extension), value:'df'}
                    self.db.update({file[:6]:df})

                # verify files with csv extension
                elif file.endswith(extension) and extension == '.csv':
                    # get the full path of the file
                    filepath = os.path.join(root, file)
                    df = pd.read_csv(filepath, dtype='str', engine='openpyxl')
                    # Update local dict db with {key:'file_name'(without extension), value:'df'}
                    self.db.update({file[:6]:df})

    def show(self):
        print(self.db['Goal11'])



if __name__ == '__main__':
    # Define a relative path (current code)
    RELATIVE_PATH = os.path.dirname(os.path.abspath(__file__))
    DATABASE_PATH = os.path.abspath(os.path.join(RELATIVE_PATH, '../../datasets/brazil'))

    new_db = Database(path=DATABASE_PATH).show()