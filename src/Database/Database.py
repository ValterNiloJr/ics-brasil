from typing import Literal
# Import python libraries
import matplotlib.pyplot as plt
import pandas as pd
import os

class Database:
    # --> Constructor
    def __init__(self) -> None:
        # local dict db
        self.db = {}

    # --> DB Reader
    def read_db(self, path:str, extension:Literal[".csv"] | None = '.xlsx') -> dict:
        # Construct local dict db walking in path
        for root, dirs, files in os.walk(path):
            for file in files:
                # verify files with xlsx extension
                if file.endswith(extension) and extension == '.xlsx':
                    # get the full path of the file
                    filepath = os.path.join(root, file)
                    df = pd.read_excel(filepath, engine='openpyxl')
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
    
    # --> File Reader
    def read_file(self, filepath:str) -> pd.DataFrame:
        return pd.read_excel(filepath, dtype='str', engine='openpyxl')
        
    # --> DB Filter
    def filter_db(self, db:dict, remove_na=True, by_columns=[], **by_groups) -> dict:
        new_db = {}
        for data in db:
            new_db.update({data : self.filter_data(db[data], remove_na, by_columns, **by_groups)})
        return new_db

    # --> Data Filter
    def filter_data(self, data:pd.DataFrame, remove_na=True, by_columns=[], **by_groups) -> pd.DataFrame:
        # Copy from data to df
        df = data.copy()
        # filter by groups
        # key = column name | value = value to filter
        for column, value in zip(by_groups.keys(), by_groups.values()):
            if by_columns != []:
                df = df.loc[(df[column]==value), by_columns]
            else:
                df = df.loc[(df[column]==value)]

        # remove rows with all NaN data
        if remove_na:
            df.dropna(axis=1, how='all', inplace=True)

        return df
    
    # --> Filter Relevant Data
    def filter_relevant(self, db:dict, metric, corr=None, n_min=11) -> dict:
        relevant = {}
        list_params = []
        for data in db:
            indicators = list(db[data][metric].unique())
            
            for indicator in indicators:
                filtered_df = self.filter_data(db[data], SeriesDescription=indicator)
                if corr != None:
                    corr_aux = [x for i, x in enumerate(corr) if x in filtered_df.columns]
                    if corr_aux != []:
                        # group the DataFrame by combinations of values in the correlation columns 
                        #   and count the number of rows in each group
                        group = filtered_df.groupby(corr_aux).size()
                        # get the group key with the highest row count
                        greatest_combination = group.idxmax()
                    
                        if len(filtered_df) >= n_min:
                            params = {}
                            if len(corr_aux) > 1:
                                for i in range(len(corr_aux)):
                                    params.update({corr_aux[i] : greatest_combination[i]})
                            else:
                                params.update({corr_aux[0] : greatest_combination})

                            list_params.append({metric:indicator, **params})

            relevant.update({data: list_params})
            list_params = []

        return relevant

    # --> Get DB metadata
    def get_metadata(self, db:dict, relevants, values:str, date:str, remove_na=True) -> dict:
        meta = {}
        for data in db:
            meta.update(self.get_df_metadata(data, db[data], relevants[data], values, date, remove_na))
        
        return meta

    # --> Get DF metadata
    def get_df_metadata(self, name:str, data:pd.DataFrame, relevants:dict, values:str, date:str, remove_na=True) -> dict:
        meta = {}
        params = {}
        for relevant in relevants:
            filtered_relevant_df = self.filter_data(data, **relevant)
            if values in list(filtered_relevant_df.columns):
                # Get Trend of values
                if self.is_increasing(filtered_relevant_df[values]):
                    df_trend = {'trend': 'increasing'}
                elif self.is_decreasing(filtered_relevant_df[values]):
                    df_trend = {'trend': 'decreasing'}
                else:
                    df_trend = {'trend': 'not clear'}

                # Get Value of Trend
                first_value = float(filtered_relevant_df[values].iloc[0])
                last_value = float(filtered_relevant_df[values].iloc[-1])

                percentage_value = (last_value - first_value) / first_value * 100

                df_value = {'value': float(f'{abs(percentage_value):.2f}'), 'unit':'percent'}

                # Get Period
                begin_date = filtered_relevant_df[date].iloc[0]
                end_date = filtered_relevant_df[date].iloc[-1]

                df_period = {'period': f'{begin_date} - {end_date}'}

                params.update({relevant['SeriesDescription']: {**df_trend, **df_value, **df_period}})
                
        if not (remove_na == True and params == {}):
            meta.update({name: params})

        return meta

    # --> Calculate trand: if values is increasing
    def is_increasing(self, set_values:pd.Series) -> bool:
        moving_average = set_values.rolling(window=1).mean()
        return moving_average.iloc[-1] > moving_average.iloc[0]

    # --> Calculate trand: if values is decreasing
    def is_decreasing(self, set_values:pd.Series) -> bool:
        moving_average = set_values.rolling(window=1).mean()
        return moving_average.iloc[-1] < moving_average.iloc[0]

    # --> Calculate Sustainable Awareness Index (SAI)
    #def calculate_SAI(self, metadata):
    #    pass


if __name__ == '__main__':
    # Define a relative path (current code)
    RELATIVE_PATH = os.path.dirname(os.path.abspath(__file__))
    DATABASE_PATH = os.path.abspath(os.path.join(RELATIVE_PATH, '../../datasets/brazil'))
    
    columns = ['Goal', 'Indicator', 'SeriesCode', 'SeriesDescription',
             'GeoAreaName', 'TimePeriod', 'Value', 'Sex', 'Location', 'Units', 'Age']
    
    # New Database Instance
    db = Database()
    # get df of all data (DB)
    all_data = db.read_db(path=DATABASE_PATH)
    # get df filtering all data with columns and gruoup (country = Brazil)
    filtered = db.filter_db(all_data, by_columns=columns, GeoAreaName='Brazil')
    # get dict params with relevant data for analysis 
    relevant = db.filter_relevant(filtered, metric='SeriesDescription', corr=['Sex', 'Location', 'Age'])
    # get dict metada with (trends, value, period)
    metadata = db.get_metadata(filtered, relevant, values='Value', date='TimePeriod')
    print(metadata)

    #print(db.read_file(DATABASE_PATH + '/Goal01.xlsx'))
    #print(new_db.get_all())
    #print(new_db.get_data('Goal03'))