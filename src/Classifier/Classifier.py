from Database.Database import Database

import numpy as np
import os

# Define a relative path (current code)
RELATIVE_PATH = os.path.dirname(os.path.abspath(__file__))

class Classifier:
    def __init__(self) -> None:
        pass

    def classifier_by_trend(self, metadata:dict, references:dict) -> dict:
        if metadata.keys() == references.keys():
            classification = metadata.copy()
            for meta, ref in zip(metadata, references):
                for data in metadata[meta]:
                    if metadata[meta][data]['trend'] == 'increasing' and references[ref][data] == 'increase':
                        classification[meta][data].update({'trend_classification': 'Y'})
                    elif metadata[meta][data]['trend'] == 'decreasing' and references[ref][data] == 'decrease':
                        classification[meta][data].update({'trend_classification': 'Y'})
                    else:
                        classification[meta][data].update({'trend_classification': 'N'})
        
        return classification

    def classifier_by_severity(self, metadata:dict, references:dict) -> dict:
        pass

    def classifier_by_impact(self, metadata:dict, references:dict) -> dict:
        pass

# Representative Class SDG Classifier (Crawler, Neural Network, ML methods ...)
class SDG(Classifier):
    def __init__(self, metadata:dict) -> None:
        super().__init__()
        
        self.metadata = metadata.copy()

    def get_references(self) -> dict:
        # 1. Get all references needed to 
        # 2. Analyse metadata
        # 3. Normalize all data

        references = {}
        params = {}
        
        DATABASE_PATH = RELATIVE_PATH + '/reference'
        db = Database().read_db(path=DATABASE_PATH)

        for key, data in zip(db.keys(), db.values()):
            for metric, reference in zip(data['Metric'], data['Reference']):
                params.update({metric.strip(): reference})

            references.update({key : {**params}})
            params = {}

        # Normilize metadata
        values = []
        values_normalized = []
        for data in self.metadata.values():
            for params in data.values():
                values.append(params['value'])
            if len(values) > 1:
                arr = np.array(values)
                
                mean = np.mean(arr)
                
                std = np.std(arr)

                # normalize with Z-score in array
                arr_normalized = (arr - mean) / std
            else:
                arr_normalized = [0]
            values_normalized.append(arr_normalized)

            values = []

        i = 0
        j = 0

        for data in self.metadata:
            for params in self.metadata[data]:
                self.metadata[data][params].update({'value_normalized':values_normalized[i][j]})
                j += 1
            i += 1
            j = 0

        return self.metadata, references
    
    # --> Calculate Sustainable Awareness Index (SAI)
    def calculate_SAI(self, classification) -> str:
        sai = 0
        n_sdg = 17
        n_indicators = len(classification.keys())
        weights = {key:len(classification[key]) for key in classification}
        weights_sum = sum([int(i) for i in weights.values()])

        # SAI calculation
        for key in classification:
            for params in classification[key].values():
                if params['trend_classification'] == 'Y':
                    sai += ((params['value_normalized'] / weights[key]))

                elif params['trend_classification'] == 'N':
                    sai -= ((params['value_normalized'] / weights[key]))
        
        # for all SDG
        sai = (sai * n_indicators) / n_sdg
        
        # return percentage
        return sai * 100