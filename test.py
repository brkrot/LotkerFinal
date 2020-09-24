import collections

import Barak as b
import matplotlib.pyplot as plt

movie1 = 'Dark Knight Rises'
movie2 = 'Captain America - Civil War'

b.surface_centrality(movie1,['WAYNE', 'BLAKE', 'BANE', 'GORDON'])
b.surface_centrality(movie2,['TONY STARK', 'STEVE ROGERS', 'NATASHA ROMANOFF', 'PETER PARKER'])

