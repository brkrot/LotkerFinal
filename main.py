import collections

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
#collecting the data from the AB
#movie_data =
#         'Dark Knight Rises'             =>     'Graph' || 'list_of_lines'    =>  the graph || line
#         'Captain America - Civil War'   =>     'Graph' || 'list_of_lines'    =>  the graph || line
#
movie_data = {movie1: a.collect_data_from_AB(movie1,G1)}
movie_data[movie2] = a.collect_data_from_AB(movie2,G2)
#print(movie_data[movie1],'\n\n@@@@\n\n',movie_data[movie2])

#creating the EVENTS-CLOCK (Ce)
[movie_data[movie1]['Ce'],movie_data[movie1]['Ce_norm']] = a.make_clock_events(movie_data[movie1]['list_of_lines'])
[movie_data[movie2]['Ce'],movie_data[movie2]['Ce_norm']] = a.make_clock_events(movie_data[movie2]['list_of_lines'])
#print(movie_data[movie1]['Ce'],'\n',movie_data[movie1]['Ce_norm'],'\n',movie_data[movie2]['Ce'],'\n',movie_data[movie2]['Ce_norm'])
#Creating the WORDS-CLOCK (Cw)
[movie_data[movie1]['Cw'],movie_data[movie1]['Cw_norm']] = a.make_clock_words(movie_data[movie1]['list_of_lines'])
[movie_data[movie2]['Cw'],movie_data[movie2]['Cw_norm']] = a.make_clock_words(movie_data[movie2]['list_of_lines'])
#print(movie_data[movie1]['Cw'],'\n',movie_data[movie1]['Cw_norm'],'\n',movie_data[movie2]['Cw'],'\n',movie_data[movie2]['Cw_norm'])
movie_data[movie1]['M'] = a.M_algo(movie_data[movie1]['Ce_norm'],movie_data[movie1]['Cw_norm'])
movie_data[movie2]['M'] = a.M_algo(movie_data[movie2]['Ce_norm'],movie_data[movie2]['Cw_norm'])
#print(movie_data[movie1]['M'],'\n',movie_data[movie2]['M'])
movie_data[movie1]['full_sub'] = a.convert_sub_to_string_and_filteration(movie_data[movie1]['list_of_lines'])
movie_data[movie2]['full_sub'] = a.convert_sub_to_string_and_filteration(movie_data[movie2]['list_of_lines'])
print(movie_data[movie1]['full_sub'], '\n\n', movie_data[movie2]['full_sub'])
#Todo: print the graphs
#TODO:count the words apperences' can be don simply using dictionary

count = collections.Counter(movie_data[movie1]['full_sub'])
movie_data[movie1]['most_common_20'] = count.most_common(20)
print('Most common words:\n',movie_data[movie1]['most_common_20'])

count = collections.Counter(movie_data[movie2]['full_sub'])
movie_data[movie2]['most_common_20'] = count.most_common(20)
print('Most common words:\n',movie_data[movie2]['most_common_20'])

"""# List of all words across tweets
all_words_no_urls = list(itertools.chain(*words_in_tweet))

# Create counter
counts_no_urls = collections.Counter(all_words_no_urls)

cou"""
