#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 13:32:51 2023

@author: eveomett

Lab 3: MAUP and data.  See details on Canvas page

Make sure to say where/when you got your data!
"""
import pandas as pd
import geopandas as gpd
import maup
import time

from gerrychain_functions import *

maup.progress.enabled = True

start_time = time.time()

print("Starting graph load")
# la_graph = Graph.from_json("./LA/LA.geojson")  # node issue
la_graph = Graph.from_file("./LA/LA.shp")
print("Graph loaded")
initial_partition = init_partition(la_graph)
print("Initial partition initialized")
ideal_pop = calc_population(la_graph, 6, "TOTPOP")
print("Ideal population: ", ideal_pop)
rand_walk = init_markov_chain(la_graph, initial_partition, "TOTPOP", ideal_pop, 100)  # 2000
print("Markov Chain initialized")
cutedge_ensemble = []
lmaj_ensemble = []
dem_win_ensemble = []
cutedge_ensemble, lmaj_ensemble, dem_win_ensemble = walk_the_run(rand_walk, 6, "TOTPOP", cutedge_ensemble, lmaj_ensemble, dem_win_ensemble)

# Histograms
# 1. Cut edge
plot_histograms(cutedge_ensemble, "histograms/cutedge_ensemble.png")
# 2. Majority-Latino districts
plot_histograms(lmaj_ensemble, "histograms/lmaj_ensemble.png")
# 3. Democratic-won districts
plot_histograms(dem_win_ensemble, "histograms/dem_win_ensemble.png")
print("Histograms writen to files")

end_time = time.time()
print("The time of execution of above program is :",
      (end_time - start_time) / 60, "mins")
