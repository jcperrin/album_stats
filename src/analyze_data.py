#!/usr/bin/env python3

import pandas as pd
import seaborn as sns

def import_spreadsheet():
    """ Reads raw data from some source """
    return pd.read_csv("../data/2019_bestAlbums.csv")

def clean_spreadsheet(df):
    """ Takes care of cleaning up the raw data into a more useable form"""
    return (df.rename(columns = {'JCP Rating' : 'jcp', 
                         'Chris Rating' : 'chris',
                         ':) Rating': 'ally'})
        .drop(df.tail(2).index)
        )

def plot_histograms(df):
    """ Creates a histogram of our rating distributions"""
    view = (df[['jcp', 'chris', 'ally']]
                #.fillna(0)
                .melt()
                )
    return sns.countplot(x="value", hue="variable", data=view)

def main():
    sns.set(context="talk", style="white")
    sns.set_palette("husl", 3)
    df = import_spreadsheet()
    df = clean_spreadsheet(df)
    g = plot_histograms(df)
    sns.despine()
    g.figure.savefig("../results/score_distribution.png", dpi=300, transparent=True)
    
if __name__ == '__main__':
    main()