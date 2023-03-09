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
                    sai += ((float(params['value'][:-1]) / weights[key]) / n_indicators)

                elif params['trend_classification'] == 'N':
                    sai -= ((float(params['value'][:-1]) / weights[key]) / n_indicators)

        return sai 