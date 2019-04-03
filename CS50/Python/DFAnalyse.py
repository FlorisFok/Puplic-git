import pandas
import sys

class Analyse(object):

    def __init__(self, df):
        self.df = df
        self.keys = list(df)
        self.length = len(df)
    
    def get_keys(self):
        return self.keys
    
    def get_len(self):
        return self.length
    
    def get_type(self, key):
        return type(self.df[key][0])
    
    def col_list(self, key):
        return list(self.df[key])
    
    def select_equal(self, col, quant):
        self.df = df.loc[df[col] == quant]
        self.length = len(self.df)
    
    def select_more_less(self, col, quant, more_than = True):
        if more_than:
            self.df = df.loc[df[col] > quant]
        else:
            self.df = df.loc[df[col] <= quant]
        self.length = len(self.df)
    
    def select_list(self, col, list_quant):
        self.df = self.df.loc[df[col].isin(list_quant)]
        self.length = len(self.df)
    
    def avg(self, col):
        the_list = list(self.df[col])
        return (sum(the_list)/len(the_list))
    
    def of_each(self, itter, height, avg = False):
        units = set(list(df[itter]))
        heights = []
        for unit in units:
            bar = df.loc[df[itter] == unit]
            bar = bar[height]
            if avg:
                bar = sum(bar)/len(bar)
            else:
                bar = sum(bar)
            heights.append(bar)
        return heights, units
    
    def genre_count(self):
        genres = {}
        for movie in self.df["genre"]:
            for gen in movie:
                if gen in genres:
                    genres[gen] += 1
                else:
                    genres[gen] = 1
        return genres

    def genre_avg(self, key='rating'):
        first_dict = {}
        for genre_str, other in zip(list(self.df['genre']),list(self.df[key])):
            gsplit = genre_str.split(",")
            for singleg in gsplit:
                singleg = singleg.strip()
                if singleg in d:
                    first_dict[singleg][0] += other
                    first_dict[singleg][1] += 1
                else:
                    first_dict[singleg] = [other, 1]
        second_dict = first_dict
        for genre in second_dict:
            second_dict[genre] = [second_dict[genre][0]/second_dict[genre][1], second_dict[genre][1]]
        
        return first_dict, second_dict