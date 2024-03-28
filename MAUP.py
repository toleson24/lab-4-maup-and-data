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

from RedistrictingMarkovChain import *

maup.progress.enabled = True

start_time = time.time()

print("Starting graph load")
# la_graph = Graph.from_json("./LA/LA.geojson")  # node issue
la_graph = Graph.from_file("./LA/LA.shp")
print("Graph loaded")
la_markov_chain = RedistrictingMarkovChain(la_graph,
                                           6,
                                           "CD",
                                           "PRES20",
                                           "G20PRED",
                                           "G20PRER",
                                           "TOTPOP",
                                           "HISP")
la_markov_chain.init_partition()
la_markov_chain.init_markov_chain(steps=1000)
cutedge_ensemble, lmaj_ensemble, dem_win_ensemble = la_markov_chain.walk_the_run()

# Histograms
# 1. Cut edge
plot_histograms(cutedge_ensemble, "histograms/cutedge_ensemble.png")
# 2. Majority-Latino districts
plot_histograms(lmaj_ensemble, "histograms/lmaj_ensemble.png")
# 3. Democratic-won districts
plot_histograms(dem_win_ensemble, "histograms/dem_win_ensemble.png")

end_time = time.time()
print("The time of execution of above program is :",
      (end_time - start_time) / 60, "mins")
