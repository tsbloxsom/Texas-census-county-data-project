# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 12:49:27 2020

@author: tsbloxsom
"""

ts_df = pd.read_csv("time_series_plotly.csv").drop("Unnamed: 0", axis = 1)
county_loc = pd.read_csv("Texas_Counties_Centroid_Map.csv")