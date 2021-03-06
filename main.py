#new try
import collections
import matplotlib.pyplot as plt
import Barak as b
import Avihay as a

#for later, making it modular
movie = ['Dark Knight Rises', 'Captain America - Civil War']
#
movie1 = 'Dark Knight Rises'
movie2 = 'Captain America - Civil War'
main_char_m1 = ['WAYNE', 'BLAKE', 'BANE', 'GORDON']
main_char_m2 = ['TONY STARK', 'STEVE ROGERS', 'NATASHA ROMANOFF', 'PETER PARKER']

'---------------------------------------Question 2-------------------------------------'
#Part A
#This functions is making ab.csv table and srt-script file for each one of the movies
#b.makeABandScriptSrt(movie1) #we made some hand work becouse of codacs probleme
#b.makeABandScriptSrt(movie2) #we made some hand work becouse of codacs probleme

                            #   Part B      #
G1 = a.make_all_graphs(movie1)
G2 = a.make_all_graphs(movie2)
                            #   Part C & D  #
a.four_main_characters(movie1, G1, movie2, G2)


'---------------------------------------Question 3-------------------------------------'
b.voronoi(movie1)
b.voronoi(movie2)
b.voting(movie1)
b.voting(movie2)
b.otherAlgos(movie1)
b.otherAlgos(movie2)
'---------------------------------------Question 4-------------------------------------'
#collecting the data from the AB
#movie_data =       'first-tag'                             'second-tag'
#         'Dark Knight Rises'             =>     'Graph','list_of_lines','Ce','Cw',M,'fullsub'  =>  the graph || line
#         'Captain America - Civil War'   =>     'Graph','list_of_lines','Ce','Cw',M,'fullsub'   =>  the graph || line
#
movie_data = {movie1: a.collect_data_from_AB(movie1, G1)}
movie_data[movie2] = a.collect_data_from_AB(movie2, G2)
#print(movie_data[movie1],'\n\n@@@@\n\n',movie_data[movie2])

#creating the EVENTS-CLOCK (Ce)
[movie_data[movie1]['Ce'], movie_data[movie1]['Ce_norm'],movie_data[movie1]['Ce_norm_value']] = a.make_clock_events(movie_data[movie1]['list_of_lines'])
[movie_data[movie2]['Ce'], movie_data[movie2]['Ce_norm'],movie_data[movie2]['Ce_norm_value']] = a.make_clock_events(movie_data[movie2]['list_of_lines'])
#print(movie_data[movie1]['Ce'],'\n',movie_data[movie1]['Ce_norm'],'\n',movie_data[movie2]['Ce'],'\n',movie_data[movie2]['Ce_norm'])
#Creating the WORDS-CLOCK (Cw)
[movie_data[movie1]['Cw'], movie_data[movie1]['Cw_norm'],movie_data[movie1]['Cw_norm_value']] = a.make_clock_words(movie_data[movie1]['list_of_lines'])
[movie_data[movie2]['Cw'], movie_data[movie2]['Cw_norm'],movie_data[movie2]['Cw_norm_value']] = a.make_clock_words(movie_data[movie2]['list_of_lines'])
#print(movie_data[movie1]['Cw'],'\n',movie_data[movie1]['Cw_norm'],'\n',movie_data[movie2]['Cw'],'\n',movie_data[movie2]['Cw_norm'])
movie_data[movie1]['M'] = a.M_algo(movie_data[movie1]['Ce_norm'], movie_data[movie1]['Cw_norm'])
movie_data[movie2]['M'] = a.M_algo(movie_data[movie2]['Ce_norm'], movie_data[movie2]['Cw_norm'])
#                               -----------printing----------
#printing graphs for the story
a.make_axis_graph(movie_data[movie1]['Ce'], movie_data[movie1]['Cw'], movie_data[movie1]['Ce'], movie_data[movie1]['Ce']
                  , 'Time', 'Clock', 'Cw', 'Ce', 'clock for '+movie1)
a.make_axis_graph(movie_data[movie2]['Ce'], movie_data[movie2]['Cw'], movie_data[movie2]['Ce'], movie_data[movie2]['Ce']
                  , 'Time', 'Clock', 'Cw', 'Ce', 'clock for '+movie2)
a.make_axis_graph(movie_data[movie1]['Ce_norm'], movie_data[movie1]['Cw_norm'], movie_data[movie1]['Ce_norm'],
                  movie_data[movie1]['Ce_norm'],
                  'Time_norm', 'Clock_norm', 'Cw_norm', 'Ce_norm', 'Normalized clock for '+movie1)
a.make_axis_graph(movie_data[movie2]['Ce_norm'], movie_data[movie2]['Cw_norm'], movie_data[movie2]['Ce_norm'],
                  movie_data[movie2]['Ce_norm'],
                  'Time_norm', 'Clock_norm', 'Cw_norm', 'Ce_norm', 'Normalized clock for'+movie2)
a.make_axis_graph(movie_data[movie1]['Ce_norm'], movie_data[movie1]['M'], movie_data[movie1]['Ce_norm'],
                  movie_data[movie1]['M'],
                  'Time_norm','Cw-Ce','M','M','M - Algo for '+movie1)
a.make_axis_graph(movie_data[movie2]['Ce_norm'], movie_data[movie2]['M'], movie_data[movie2]['Ce_norm'],
                  movie_data[movie2]['M'],
                  'Time_norm', 'Cw-Ce', 'M', 'M', 'M - Algo for ' + movie2)

# Finding the 4 maxes and 4 mins of M
print('Min-Max events for:', movie1)
[movie_data[movie1]['M_max'], movie_data[movie1]['M_min']] = a.find_maxs_and_mins(movie_data[movie1]['M'], movie_data[movie1]['Ce'], 4)
print('Min-Max events for:', movie2)
[movie_data[movie2]['M_max'], movie_data[movie2]['M_min']] = a.find_maxs_and_mins(movie_data[movie2]['M'], movie_data[movie2]['Ce'], 4)
# Printing the max and min lines
a.print_lines_from_AB(movie_data[movie1]['list_of_lines'], movie_data[movie1]['M_max'].keys(), movie1 + ':\nMAX LINES:')
a.print_lines_from_AB(movie_data[movie1]['list_of_lines'], movie_data[movie1]['M_min'].keys(), 'Min lines:')
a.print_lines_from_AB(movie_data[movie2]['list_of_lines'], movie_data[movie2]['M_max'].keys(), movie2 + ':\nMAX LINES:')
a.print_lines_from_AB(movie_data[movie2]['list_of_lines'], movie_data[movie2]['M_min'].keys(), 'Min lines:')

#making X_v & M(t,Xv)

movie_data[movie1]['Xv'] = a.norm_for_Xv(b.main_characters_steps(movie_data[movie1]['list_of_lines'], main_char_m1[0:2]))
movie_data[movie2]['Xv'] = a.norm_for_Xv(b.main_characters_steps(movie_data[movie2]['list_of_lines'], main_char_m2[0:2]))
movie_data[movie1]['M(t,Xv)1'] = a.M_algo(movie_data[movie1]['Ce_norm'],movie_data[movie1]['Xv'][main_char_m1[0]])
movie_data[movie1]['M(t,Xv)2'] = a.M_algo(movie_data[movie1]['Ce_norm'],movie_data[movie1]['Xv'][main_char_m1[1]])
movie_data[movie2]['M(t,Xv)1'] = a.M_algo(movie_data[movie2]['Ce_norm'],movie_data[movie2]['Xv'][main_char_m2[0]])
movie_data[movie2]['M(t,Xv)2'] = a.M_algo(movie_data[movie2]['Ce_norm'],movie_data[movie2]['Xv'][main_char_m2[1]])
a.make_axis_graph(movie_data[movie1]['Ce_norm'],movie_data[movie1]['M(t,Xv)1'],movie_data[movie1]['Ce_norm'],movie_data[movie1]['M(t,Xv)2'],
                  'Time_norm','Xv-Ce',main_char_m1[0],main_char_m1[1],'M(t,Xv) - Algo for '+movie1)
a.make_axis_graph(movie_data[movie2]['Ce_norm'], movie_data[movie2]['M(t,Xv)1'], movie_data[movie2]['Ce_norm'],
                  movie_data[movie2]['M(t,Xv)2'],
                  'Time_norm','Xv-Ce',main_char_m2[0],main_char_m2[1],'M(t,Xv) - Algo for '+movie2)
[movie_data[movie1]['Mxv1_max'], movie_data[movie1]['Mxv1_min']] =a.find_maxs_and_mins(movie_data[movie1]['M(t,Xv)1'],movie_data[movie1]['Ce'],2)
[movie_data[movie1]['Mxv2_max'], movie_data[movie1]['Mxv2_min']] =a.find_maxs_and_mins(movie_data[movie1]['M(t,Xv)2'],movie_data[movie1]['Ce'],2)
[movie_data[movie2]['Mxv1_max'], movie_data[movie2]['Mxv1_min']] =a.find_maxs_and_mins(movie_data[movie2]['M(t,Xv)1'],movie_data[movie2]['Ce'],2)
[movie_data[movie2]['Mxv2_max'], movie_data[movie2]['Mxv2_min']] =a.find_maxs_and_mins(movie_data[movie2]['M(t,Xv)2'],movie_data[movie2]['Ce'],2)
a.print_lines_from_AB(movie_data[movie1]['list_of_lines'], movie_data[movie1]['Mxv1_max'].keys(), movie1 + ':\nMAX LINES:')
a.print_lines_from_AB(movie_data[movie1]['list_of_lines'], movie_data[movie1]['Mxv1_min'].keys(), 'Min lines:')
a.print_lines_from_AB(movie_data[movie1]['list_of_lines'], movie_data[movie1]['Mxv2_max'].keys(), movie1 + ':\nMAX LINES:')
a.print_lines_from_AB(movie_data[movie1]['list_of_lines'], movie_data[movie1]['Mxv2_min'].keys(), 'Min lines:')
a.print_lines_from_AB(movie_data[movie2]['list_of_lines'], movie_data[movie2]['Mxv1_max'].keys(), movie2 + ':\nMAX LINES:')
a.print_lines_from_AB(movie_data[movie2]['list_of_lines'], movie_data[movie2]['Mxv1_min'].keys(), 'Min lines:')
a.print_lines_from_AB(movie_data[movie2]['list_of_lines'], movie_data[movie2]['Mxv2_max'].keys(), movie2 + ':\nMAX LINES:')
a.print_lines_from_AB(movie_data[movie2]['list_of_lines'], movie_data[movie2]['Mxv2_min'].keys(), 'Min lines:')



# Most common 20 words
movie_data[movie1]['full_sub'] = a.convert_sub_to_string_and_filteration(movie_data[movie1]['list_of_lines'])
movie_data[movie2]['full_sub'] = a.convert_sub_to_string_and_filteration(movie_data[movie2]['list_of_lines'])
#print(movie_data[movie1]['full_sub'], '\n\n', movie_data[movie2]['full_sub'])
count = collections.Counter(movie_data[movie1]['full_sub'])
movie_data[movie1]['most_common_20_words'] = count.most_common(20)
print('Most common words:\n', movie_data[movie1]['most_common_20_words'])

count = collections.Counter(movie_data[movie2]['full_sub'])
movie_data[movie2]['most_common_20_words'] = count.most_common(20)
print('Most common words:\n', movie_data[movie2]['most_common_20_words'])
#making 2 kinds of Cl
print(movie_data[movie1]['most_common_20_words'][1])
[movie_data[movie1]['Cl_vecs'],movie_data[movie1]['Cl_vecs_norm'],
 movie_data[movie1]['Cl_all_together'],movie_data[movie1]['Cl_all_together_norm']]\
    = a.make_clock_Cl(movie_data[movie1])
[movie_data[movie2]['Cl_vecs'],movie_data[movie2]['Cl_vecs_norm'],
 movie_data[movie2]['Cl_all_together'],movie_data[movie2]['Cl_all_together_norm']]\
    = a.make_clock_Cl(movie_data[movie2])
#printing Cl for all words
a.make_axis_graph(movie_data[movie1]['Ce_norm'],movie_data[movie1]['Cl_all_together_norm'], movie_data[movie2]['Ce_norm'],movie_data[movie2]['Cl_all_together_norm'],'Time_norm','Cl_norm',movie1,movie2,'Clock Of Common Words (t,Cl)')
#making M(Ce,CL)
movie_data[movie1]['M_CL']=a.M_algo(movie_data[movie1]['Ce_norm'],movie_data[movie1]['Cl_all_together_norm'])
movie_data[movie2]['M_CL']=a.M_algo(movie_data[movie2]['Ce_norm'],movie_data[movie2]['Cl_all_together_norm'])
#print M(Ce,CL)
a.make_axis_graph(movie_data[movie1]['Ce_norm'],movie_data[movie1]['M_CL'],movie_data[movie2]['Ce_norm'],movie_data[movie2]['M_CL'],
                  'Time_norm','CL-Ce',movie1,movie2,'M(Ce,CL) - Algo for most common 20 words ')
[movie_data[movie1]['Mcl_max'], movie_data[movie1]['Mcl_min']] =a.find_maxs_and_mins(movie_data[movie1]['M_CL'],movie_data[movie1]['Ce'],4)
[movie_data[movie2]['Mcl_max'], movie_data[movie2]['Mcl_min']] =a.find_maxs_and_mins(movie_data[movie2]['M_CL'],movie_data[movie2]['Ce'],4)
a.print_lines_from_AB(movie_data[movie1]['list_of_lines'], movie_data[movie1]['Mcl_max'].keys(), movie1 + ':\nMAX LINES:')
a.print_lines_from_AB(movie_data[movie1]['list_of_lines'], movie_data[movie1]['Mcl_min'].keys(), 'Min lines:')
a.print_lines_from_AB(movie_data[movie2]['list_of_lines'], movie_data[movie2]['Mcl_max'].keys(), movie2 + ':\nMAX LINES:')
a.print_lines_from_AB(movie_data[movie2]['list_of_lines'], movie_data[movie2]['Mcl_min'].keys(), 'Min lines:')

#comperation of the two Words clocks, Cw
#sizing movie 2
Cw2_interputaled=a.interpulation(movie_data[movie2]['Cw_norm'],len(movie_data[movie1]['Cw_norm'])-len(movie_data[movie2]['Cw_norm']))
M_Cw1_vs_Cw2 = a.M_algo(movie_data[movie1]['Cw_norm'],Cw2_interputaled)
a.make_axis_graph(movie_data[movie1]['Ce_norm'],M_Cw1_vs_Cw2,movie_data[movie1]['Ce_norm'],M_Cw1_vs_Cw2,
                  'Time_norm','Cw2-Cw1','Cw2-Cw1','Cw2-Cw1','M(Ce,Cw2-Cw1) ')
a.find_maxs_and_mins(M_Cw1_vs_Cw2,movie_data[movie1]['Ce'],2)

print("This may take a while. about few minuts\nThanks for the patience :)")
'---------------------------------------Question 5-------------------------------------'
b.surface_centrality(movie1,main_char_m1)
b.surface_centrality(movie2,main_char_m2)