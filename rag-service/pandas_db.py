import database_interface
import pandas as pd
import numpy as np

class PandasDatabase(database_interface.DataBase):
    
    def __init__(self, file):
        self.pd = pd.read_pickle(file)
    
    
    def add_new_data(self, embeds, answers):
        return super().add_new_data(embeds, answers)
    
    def find_mins(self, embed, metric, count_nearest=3):
        similarities = self.pd.vector.apply(lambda x: metric(embed, x)).sort_values()
        ordered = self.pd.loc[similarities.index, :].document
        res = [(ordered.values[i], similarities.values[i]) for i in range(0, count_nearest)]
        return res