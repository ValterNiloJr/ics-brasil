# Import aux modules
from Database.Database import Database
from Graphics.Graphics import Graphics
from Classifier.Classifier import SDG
# Import python libraries
import os
# Define a relative path (current code)
RELATIVE_PATH = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.abspath(os.path.join(RELATIVE_PATH, '../datasets/brazil'))

country = 'Brazil'

columns = ['Goal', 'Indicator', 'SeriesCode', 'SeriesDescription',
             'GeoAreaName', 'TimePeriod', 'Value', 'Sex', 'Location', 'Units', 'Age']

# New Database Instance
db = Database()
# get df of all data (DB)
all_data = db.read_db(path=DATABASE_PATH)
# get df filtering all data with columns and gruoup (country = Brazil)
filtered = db.filter_db(all_data, by_columns=columns, GeoAreaName=country)
# get dict params with relevant data for analysis 
relevant = db.filter_relevant(filtered, metric='SeriesDescription', corr=['Sex', 'Location', 'Age'])
# get dict metada with (trends, value, period)
metadata = db.get_metadata(filtered, relevant, values='Value', date='TimePeriod')
# new SDG Instance
sdg = SDG(metadata=metadata)
# get metada normalized and references by SDG
metadata_normilized, references = sdg.get_references()
# classifier data using trends method
classification = sdg.classifier_by_trend(metadata=metadata_normilized, references=references)
# finally, calculate the Sustainable Awareness Index (SAI)
sustainable_awareness_index = sdg.calculate_SAI(classification=classification)

print(f'The Sustainable Awareness Index (SAI) for {country} is: {sustainable_awareness_index:.2f}%')

Graphics(database=filtered, relevants=relevant, country=country, type='-o', color='r').plot()