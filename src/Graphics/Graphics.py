from Database.Database import Database
import matplotlib.pyplot as plt
import os

# Define a relative path (current code)
RELATIVE_PATH = os.path.dirname(os.path.abspath(__file__))
SAVE_FIG_PATH = os.path.abspath(os.path.join(RELATIVE_PATH, '../Assets/Graphs'))

class Graphics:
    def __init__(self, database:dict, relevants:dict, type=None, color='k') -> None:
        self.database = database
        self.relevants = relevants
        self.type = type
        self.color = color
    
    def plot(self):
        db = Database()
        for data in self.database:
            for relevant in self.relevants[data]:
                try:
                    data_df = db.filter_data(self.database[data], **relevant)
                    plt.figure(figsize=(15,8))
                    plt.plot(data_df['TimePeriod'], data_df['Value'], self.type, color=self.color)
                    plt.xticks(data_df['TimePeriod'])
                    plt.xlabel('Time')
                    plt.ylabel('Value')
                    title = data_df['SeriesDescription'].iloc[0]
                    plt.title(title)
                    title = title.replace('/','-')
                    plt.savefig(f'{SAVE_FIG_PATH}/{data}/{title}.png')
                    plt.close()
                except KeyError:
                    pass

    