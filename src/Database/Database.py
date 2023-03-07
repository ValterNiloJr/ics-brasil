# Import python libraries
import pandas as pd
import os

class Database:
    def __init__(self, path:str, extension='.xlsx') -> None:
        # local dict db
        self.db = {}
        # Construct local dict db walking in path
        for root, dirs, files in os.walk(path):
            for file in files:
                # verify files with parameter extension
                if file.endswith(extension):
                    # get the full path of the file
                    filepath = os.path.join(root, file)
                    df = pd.read_excel(filepath, dtype='str', engine='openpyxl')
                    # Update local dict db with {key:'file_name'(without extension), value:'df'}
                    self.db.update({file[:6]:df})

    def show(self):
        print(self.db['Goal11'])



if __name__ == '__main__':
    # Define a relative path (current code)
    RELATIVE_PATH = os.path.dirname(os.path.abspath(__file__))
    DATABASE_PATH = os.path.abspath(os.path.join(RELATIVE_PATH, '../../datasets/brazil'))

    new_db = Database(DATABASE_PATH).show()