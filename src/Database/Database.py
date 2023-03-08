from typing import Literal
# Import python libraries
import pandas as pd
import os

class Database:
    def __init__(self) -> None:
        # local dict db
        self.db = {}
    
    def read_data(self, path:str, extension:Literal[".csv"] | None = '.xlsx'):
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
                
                else:
                    self.db = {}

        return self.db

    def filter_all(self, remove_na=True, by_columns=[], **by_groups) -> dict:
        new_db = {}
        for data in self.db:
            new_db.update({data : self.filter_data(self.db[data], remove_na, by_columns, **by_groups)})
        return new_db

    def filter_data(self, data:pd.DataFrame, remove_na=True, by_columns=[], **by_groups) -> pd.DataFrame:
        # Copy from data to df
        df = data.copy()
        # filter by groups
        # key = column name | value = value to filter
        for column, values in zip(by_groups.keys(), by_groups.values()):
            for value in values:
                df = df.loc[(df[column]==value), by_columns]
        # remove rows with all NaN data
        if remove_na:
            df.dropna(axis=1, how='all', inplace=True)

        return df
    
#    def get_all(self) -> dict:
#        return self.db
#
#    def get_data(self, key:str) -> pd.DataFrame:
#        try:
#            return self.db[key]
#        except KeyError:
#            raise KeyError(f'Key not found. Try: {list(self.db.keys())}')


if __name__ == '__main__':
    # Define a relative path (current code)
    RELATIVE_PATH = os.path.dirname(os.path.abspath(__file__))
    DATABASE_PATH = os.path.abspath(os.path.join(RELATIVE_PATH, '../../datasets/brazil'))
    columns = ['Goal', 'Indicator', 'SeriesCode', 'SeriesDescription',
             'GeoAreaName', 'TimePeriod', 'Value', 'Sex', 'Units', 'Age']
    db = Database()
    data = db.read_data(path=DATABASE_PATH)
    filtered = db.filter_all(by_columns=columns, GeoAreaName=['Brazil'])
    #print(new_db.get_all())
    #print(new_db.get_data('Goal03'))