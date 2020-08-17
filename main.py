import Barak as b
import Avihay
from LotkerFinal import Barak as b
from LotkerFinal import Avihay as a
import networkx as nx

movie1 = 'Dark Knight Rises'
movie2 = 'Captain America - Civil War'


'---------------------------------------Question 2-------------------------------------'
#Part A
#This functions is making ab.csv table and srt-script file for each one of the movies
#b.makeABandScriptSrt(movie1)
#b.makeABandScriptSrt(movie2)

                            #   Part B      #
G1 = a.make_all_graphs(movie1)
G2 = a.make_all_graphs(movie2)
                            #   Part C & D  #
a.four_main_characters(movie1, G1, movie2, G2)


'---------------------------------------Question 3-------------------------------------'

#b.VORONOI(movie2)


'---------------------------------------Question 4-------------------------------------'