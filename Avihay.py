import codecs
import csv
import networkx
import networkx as nx
import matplotlib.pyplot as plt
from nltk.corpus.europarl_raw import english
from sympy import Symbol
import sys
import string
import pandas as pd
from dataclasses import dataclass
import nltk
import re
import numpy as np
import pandas as pd
from pprint import pprint
from nltk.corpus import stopwords
# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
# spacy for lemmatization
import nltk
# Plotting tools
import pyLDAvis
import pyLDAvis.gensim  # don't skip this
import matplotlib.pyplot as plt
from nltk.stem import PorterStemmer
# Enable logging for gensim - optional
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)

import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)
#AB_FilePath = movieName+' AB.csv'


@dataclass
class Line:
    num: int
    talker: string
    sub: string
    num_of_words: int


def make_civilwar_script():
    look_for_ending_bracelet = False
    flag = True
    output_file = open("Captain America - Civil War - altered.txt", "w")
    with codecs.open("Captain_America_-_Civil_War.txt", encoding="utf-8") as in_file:
        while flag:
            try:
                line = in_file.readline()
                new_line = line.replace('\n', '').replace("[", "@*").replace(']', '$@').split('@')
                for part in new_line:
                    if "End of Captain America: Civil War" in part:
                        flag = False
                        output_file.write('End of the script !!!!!!!!!')
                        break
                    elif '*' in part:
                        look_for_ending_bracelet = True
                        if '$' in part:
                            look_for_ending_bracelet = False
                    elif look_for_ending_bracelet:
                        if '$' in part:
                            look_for_ending_bracelet = False
                        else:
                            print(part)
                    elif not look_for_ending_bracelet:
                        output_file.write(part.replace('\n', ''))
                        output_file.write('\n')
            except:
                output_file.write("unrecognized languedge:\n")
    output_file.close()


def make_all_graphs(movieName):
    AB_FilePath = movieName + ' AB.csv'
    srt_script = movieName + ' srt-script.csv'
    thisdict = {}
    with open(AB_FilePath) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        # making new dic

        for row in readCSV:
            if len(row) > 0:
                name = row[1]
                if name in thisdict:
                    thisdict[name] += 1
                else:
                    thisdict[name] = 1

        # read name
        for x in thisdict:
            print(x, thisdict[x])
    print(thisdict)
    l = sorted(thisdict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    print(sorted(thisdict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True))
    print(l[0], l[1], l[2], l[3])

    # making graph nodes and weights - directed
    dict_directed = {}
    dict_directed_talker_unweighted = {}
    dict_directed_talker_weighted = {}
    with open(AB_FilePath) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')

        name1 = " "
        for row in readCSV:
            if len(row) > 0:
                name2 = row[1]
                name3 = name1 + "-&-" + name2
                # print(name1, "+", name2, "==", name3)
                # name4 = name2+"&"+name1
                if name3 in dict_directed:
                    dict_directed[name3] += 1
                    if name1 in dict_directed_talker_weighted:
                        dict_directed_talker_weighted[name1] += 1
                    else:
                        dict_directed_talker_weighted[name1] = 1
                else:  # elif name4 in this dict
                    dict_directed[name3] = 1
                    if name1 in dict_directed_talker_unweighted:
                        dict_directed_talker_unweighted[name1] += 1
                        dict_directed_talker_weighted[name1] += 1
                    else:
                        dict_directed_talker_unweighted[name1] = 1
                        dict_directed_talker_weighted[name1] = 1

                name1 = name2
        # print(graphdict1)

    print("********** directed graph******", "\n ******")
    l1 = sorted(dict_directed.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    print(sorted(dict_directed.items(), key=lambda kv: (kv[1], kv[0]), reverse=True))
    print(l1[0], l1[1], l1[2], l1[3])

    # making graph nodes and weights - undirected
    dict_undirected = {}
    dict_undirected_talker_unweighted = {}
    dict_undirected_talker_weighted = {}
    with open(AB_FilePath) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')

        name1 = " "
        for row in readCSV:
            if len(row) > 0:
                name2 = row[1]
                name3 = name2 + "-&-" + name1
                # print(name1, "+", name2, "==", name3)
                name4 = name1 + "-&-" + name2
                if name3 in dict_undirected:
                    dict_undirected[name3] += 1
                    if name2 in dict_undirected_talker_weighted:
                        dict_undirected_talker_weighted[name2] += 1
                elif name4 in dict_undirected:
                    dict_undirected[name4] += 1
                    if name1 in dict_undirected_talker_weighted:
                        dict_undirected_talker_weighted[name1] += 1

                else:
                    dict_undirected[name4] = 1
                    if name1 in dict_undirected_talker_unweighted:
                        dict_undirected_talker_unweighted[name1] += 1
                        dict_undirected_talker_weighted[name1] += 1
                    else:
                        dict_undirected_talker_unweighted[name1] = 1
                        dict_undirected_talker_weighted[name1] = 1
                name1 = name2

    print("********** undirected graph******", "\n ******")
    l2 = sorted(dict_undirected.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    print(sorted(dict_undirected.items(), key=lambda kv: (kv[1], kv[0]), reverse=True))
    print(l2[0], l2[1], l2[2], l2[3])

    #
    # paint the graphs
    #
    #
    # ********directed graph no weight

    G_direct_no_weights = nx.Graph().to_directed()
    for v in dict_directed:
        name = v.split("-&-")
        G_direct_no_weights.add_edge(name[0], name[1], weight=1)

        # printing no weight graph
    draw_AB_graph(G_direct_no_weights,True)

    l1 = sorted(dict_directed_talker_unweighted.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    print("\nDirected $ Unweighted graph 4 main character :\n", l1[0], l1[1], l1[2], l1[3])

    # *********directed graph weighted
    G_direct_weighted = nx.DiGraph()
    for v in dict_directed:
        name = v.split("-&-")
        # print(v, "===", name[0], name[1])
        G_direct_weighted.add_edge(name[0], name[1], weight=int(dict_directed[v]))

        # printing Directed weighted graph
    draw_AB_graph(G_direct_weighted,True)

    l1 = sorted(dict_directed_talker_weighted.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    print("\nDirected $ weighted graph 4 main character :\n", l1[0], l1[1], l1[2], l1[3])
    # ******** undirected not weighted graph

    G_undircet_no_weights = nx.Graph()
    for v in dict_undirected:
        name = v.split("-&-")
        G_undircet_no_weights.add_edge(name[0], name[1], weight=1)

        # printing undirected unweighted graph
    draw_AB_graph(G_undircet_no_weights,False)

    l1 = sorted(dict_undirected_talker_unweighted.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    print("\nUn - Directed $ Unweighted graph 4 main character :\n", l1[0], l1[1], l1[2], l1[3])

    # undirected weighted graph

    G_undircet_weighted = nx.Graph()
    for v in dict_undirected:
        name = v.split("-&-")
        G_undircet_weighted.add_edge(name[0], name[1], weight=int(dict_undirected[v]))

        # printing undirected weighted graph
    draw_AB_graph(G_undircet_weighted,False)

    l1 = sorted(dict_undirected_talker_weighted.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    print("\nUn - Directed $ Weighted graph 4 main character :\n", l1[0], l1[1], l1[2], l1[3])

    # Page ranking clculating
    Gdnw = nx.pagerank(G_direct_no_weights)
    Gdw = nx.pagerank(G_direct_weighted)
    Gndw = nx.pagerank(G_undircet_weighted)
    Gndnw = nx.pagerank(G_undircet_no_weights)

    l1 = sorted(Gdnw.items(), key=lambda x: x[1], reverse=True)
    l2 = sorted(Gdw.items(), key=lambda x: x[1], reverse=True)
    l3 = sorted(Gndw.items(), key=lambda x: x[1], reverse=True)
    l4 = sorted(Gndnw.items(), key=lambda x: x[1], reverse=True)
    print("\nPange - Ranking :")
    print("\nDirected $ Un-Weighted graph 4 main character :\n", l1[0], l1[1], l1[2], l1[3])
    print("\nDirected $ Weighted graph 4 main character :\n", l2[0], l2[1], l2[2], l2[3])
    print("\nUn - Directed $ Weighted graph 4 main character :\n", l3[0], l3[1], l3[2], l3[3])
    print("\nUn - Directed $ Un-Weighted graph 4 main character :\n", l4[0], l4[1], l4[2], l4[3])
    print("\n Optimization:\n\tNumber of vertex from script : \t", nx.number_of_nodes(G_direct_weighted))

    # Optimization Sheela 3

    # making ab directed and weighted graph from the subtitle srt file
    # specially for the optimization

    '******************Getting the speakers list from the script:AB.csv**************************'
    speakers = []
    with open(AB_FilePath) as csvFile:
        # Works if the file is in the same folder,
        # Otherwise include the full path
        reader = csv.DictReader(csvFile)
        for row in reader:
            speakers.append(row['Speaker'])
    '******************Getting the text of the subtitles from the srt-English.csv**************************'
    text = []
    with open(srt_script) as csvFile:
        # Works if the file is in the same folder,
        # Otherwise include the full path
        reader = csv.DictReader(csvFile)
        for row in reader:
            text.append(row['Text'])

    '**********************Getting all the names with duplicants*****************************************'
    speakersDictionary = {}
    for speaker in speakers:
        # Downcasing
        speaker = speaker.lower()
        if speaker in speakersDictionary:
            speakersDictionary[speaker] = speakersDictionary[speaker] + 1
        else:
            speakersDictionary[speaker] = 1

    # Eraasing wrong names
   # del speakersDictionary['i']
   # del speakersDictionary['harry/ron']
    str1 = 'HARRY/RON/FRED/GEORGE'
    str1 = str1.lower()
   # del speakersDictionary[str1]
   # del speakersDictionary['professor']
   # del speakersDictionary['harry/ron/hermione']
    # print(speakersDictionary)

    'creaintg list of all the names in the subtitles 1 after the other'
    listOfTalkers = []
    for line in text:
        line = line.lower()
        for name in speakersDictionary:
            if (name in line):
                listOfTalkers.append(name)
    print(listOfTalkers)

    '******************3, directed weighted graph***************'
    G3 = nx.DiGraph()
    G3.add_nodes_from(listOfTalkers)
    for y in range(len(listOfTalkers) - 1):
        if ((listOfTalkers[y] != listOfTalkers[y + 1])):
            if ((listOfTalkers[y], listOfTalkers[y + 1]) in G3.edges()):
                G3[listOfTalkers[y]][listOfTalkers[y + 1]]['weight'] += 1
            else:
                G3.add_edge(listOfTalkers[y], listOfTalkers[y + 1], weight=1)
    #for i in range(0, 18):
     #   G3.add_edge(y, y, weight=1)
      #  y += 1
    # ******************************************************************************************************

    return [G_direct_weighted, G_direct_no_weights, G_undircet_weighted, G_undircet_no_weights]


def four_main_characters(movie1, G1, movie2, G2):
    G1_direct_weighted = G1[0]
    G1_direct_no_weights = G1[1]
    G1_undircet_weighted = G1[2]
    G1_undircet_no_weights = G1[3]
    #
    G2_direct_weighted = G2[0]
    G2_direct_no_weights = G2[1]
    G2_undircet_weighted = G2[2]
    G2_undircet_no_weights = G2[3]

    # Part C
    print(movie1, ' Nodes:\n', G1_direct_weighted.number_of_nodes(), '\n')
    print(movie1, ' Edges:\n', G1_direct_weighted.number_of_edges(), '\n')
    print(movie2, ' Nodes:\n', G2_direct_weighted.number_of_nodes(), '\n')
    print(movie2, ' Edges:\n', G2_direct_weighted.number_of_edges(), '\n')

    # Part D         - First Movie -
    # page Rank - made in b                 #1
    # katz - works on directed only         #2
    print(movie1, 'Direct_no_weights - Katz:\n',
          (sorted((nx.katz_centrality(G1_direct_no_weights).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)),
          '\n')
    print(movie1, 'Direct_weighted - Katz:\n',
          (sorted((nx.katz_centrality(G1_direct_weighted).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)), '\n')

    # DegreeCentrality                      #3
    print(movie1, '- Direct_no_weights - degree_centrality:\n',
          (sorted((nx.degree_centrality(G1_direct_no_weights).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)),
          '\n')
    print(movie1, '- Direct_weighted - degree_centrality:\n',
          (sorted((nx.degree_centrality(G1_direct_weighted).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)),
          '\n')
    print(movie1, '- Undircet_no_weights - degree_centrality:\n',
          (sorted((nx.degree_centrality(G1_undircet_no_weights).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)),
          '\n')
    print(movie1, '- Undircet_weighted - degree_centrality:\n',
          (sorted((nx.degree_centrality(G1_undircet_weighted).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)),
          '\n')
    # ClosenessCentrality                   #4
    print(movie1, '- Direct_no_weights - Closeness Centrality:\n', (
        sorted((nx.closeness_centrality(G1_direct_no_weights).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)),
          '\n')
    print(movie1, '- Direct_weighted - Closeness Centrality:\n',
          (sorted((nx.closeness_centrality(G1_direct_weighted).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)),
          '\n')
    print(movie1, '- Undircet_no_weights - Closeness Centrality:\n', (
        sorted((nx.closeness_centrality(G1_undircet_no_weights).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)),
          '\n')
    print(movie1, '- Undircet_weighted - Closeness Centrality:\n', (
        sorted((nx.closeness_centrality(G1_undircet_weighted).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)),
          '\n')
    # Load Centrality                         #5
    nx.load_centrality(G1_direct_no_weights)
    print(movie1, '- Direct_no_weights - Load Centrality:\n',
          (sorted((nx.load_centrality(G1_direct_no_weights).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)),
          '\n')
    print(movie1, '- Direct_weighted - Load Centrality:\n',
          (sorted((nx.load_centrality(G1_direct_weighted).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)), '\n')
    print(movie1, '- Undircet_no_weights - Load Centrality:\n',
          (sorted((nx.load_centrality(G1_undircet_no_weights).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)),
          '\n')
    print(movie1, '- Undircet_weighted - Load Centrality:\n',
          (sorted((nx.load_centrality(G1_undircet_weighted).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)),
          '\n')
    #eigenvector_centrality
    print(movie1, '- dircet_weighted - eigenvector_centrality:\n',
          (sorted((nx.eigenvector_centrality(G1_direct_weighted).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)),'\n')
    print(movie1, '- dircet_unweighted - eigenvector_centrality:\n',
          (sorted((nx.eigenvector_centrality(G1_direct_no_weights).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)),'\n')
    print(movie1, '- undircet_weighted - eigenvector_centrality:\n',
          (sorted((nx.eigenvector_centrality(G1_undircet_weighted).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)),'\n')
    print(movie1, '- undircet_unweighted - eigenvector_centrality:\n',
          (sorted((nx.eigenvector_centrality(G1_undircet_no_weights).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)),'\n')
    # BetweennessCentrality
    print(movie1, '- dircet_weighted - betweenness_centrality:\n',
          (sorted((nx.betweenness_centrality(G1_direct_weighted).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)),'\n')
    print(movie1, '- dircet_unweighted - betweenness_centrality:\n',
          (sorted((nx.betweenness_centrality(G1_direct_no_weights).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)),'\n')
    print(movie1, '- undircet_weighted - betweenness_centrality:\n',
          (sorted((nx.betweenness_centrality(G1_undircet_weighted).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)),'\n')
    print(movie1, '- undircet_unweighted - betweenness_centrality:\n',
          (sorted((nx.betweenness_centrality(G1_undircet_no_weights).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)),'\n')

    #           -   Second Movie    -
    # page Rank - made in b                 #1
    # katz - works on directed only         #2
    #print(movie2, 'Direct_no_weights - Katz:\n', (sorted((nx.katz_centrality(G2_direct_no_weights).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)), '\n')
    #print(movie2, 'Direct_weighted - Katz:\n', (sorted((nx.katz_centrality(G2_undircet_weighted).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)), '\n')
    # DegreeCentrality                      #3
    print(movie2, '- Direct_no_weights - degree_centrality:\n',
          (sorted((nx.degree_centrality(G2_direct_no_weights).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)),
          '\n')
    print(movie2, '- Direct_weighted - degree_centrality:\n',
          (sorted((nx.degree_centrality(G2_direct_weighted).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)),
          '\n')
    print(movie2, '- Undircet_no_weights - degree_centrality:\n',
          (sorted((nx.degree_centrality(G2_undircet_no_weights).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)),
          '\n')
    print(movie2, '- Undircet_weighted - degree_centrality:\n',
          (sorted((nx.degree_centrality(G2_undircet_weighted).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)),
          '\n')
    # ClosenessCentrality                   #4
    print(movie2, '- Direct_no_weights - Closeness Centrality:\n', (
        sorted((nx.closeness_centrality(G2_direct_no_weights).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)),
          '\n')
    print(movie2, '- Direct_weighted - Closeness Centrality:\n',
          (sorted((nx.closeness_centrality(G2_direct_weighted).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)),
          '\n')
    print(movie2, '- Undircet_no_weights - Closeness Centrality:\n', (
        sorted((nx.closeness_centrality(G2_undircet_no_weights).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)),
          '\n')
    print(movie2, '- Undircet_weighted - Closeness Centrality:\n', (
        sorted((nx.closeness_centrality(G2_undircet_weighted).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)),
          '\n')
    # Load Centrality                         #5
    print(movie2, '- Direct_no_weights - Load Centrality:\n',
          (sorted((nx.load_centrality(G2_direct_no_weights).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)),
          '\n')
    print(movie2, '- Direct_weighted - Load Centrality:\n',
          (sorted((nx.load_centrality(G2_direct_weighted).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)), '\n')
    print(movie2, '- Undircet_no_weights - Load Centrality:\n',
          (sorted((nx.load_centrality(G2_undircet_no_weights).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)),
          '\n')
    print(movie2, '- Undircet_weighted - Load Centrality:\n',
          (sorted((nx.load_centrality(G2_undircet_weighted).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)),
          '\n')
    # eigenvector_centrality
    print(movie2, '- dircet_weighted - eigenvector_centrality:\n',
          (sorted((nx.eigenvector_centrality(G2_direct_weighted).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)),'\n')
    print(movie2, '- dircet_unweighted - eigenvector_centrality:\n',
          (sorted((nx.eigenvector_centrality(G2_direct_no_weights).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)),'\n')
    print(movie2, '- undircet_weighted - eigenvector_centrality:\n',
          (sorted((nx.eigenvector_centrality(G2_undircet_weighted).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)),'\n')
    print(movie2, '- undircet_unweighted - eigenvector_centrality:\n',
          (sorted((nx.eigenvector_centrality(G2_undircet_no_weights).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)),'\n')
    # BetweennessCentrality
    print(movie2, '- dircet_weighted - betweenness_centrality:\n',
          (sorted((nx.betweenness_centrality(G2_direct_weighted).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)),'\n')
    print(movie2, '- dircet_unweighted - betweenness_centrality:\n',
          (sorted((nx.betweenness_centrality(G2_direct_no_weights).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)),'\n')
    print(movie2, '- undircet_weighted - betweenness_centrality:\n',
          (sorted((nx.betweenness_centrality(G2_undircet_weighted).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)),'\n')
    print(movie2, '- undircet_unweighted - betweenness_centrality:\n',
          (sorted((nx.betweenness_centrality(G2_undircet_no_weights).items()), key=lambda kv: (kv[1], kv[0]), reverse=True)),'\n')


def collect_data_from_AB(movie, G):
    """
    Return: {'Graph':G, 'list_of_lines': list}
    """
    movie = movie + ' AB.csv'
    df = pd.read_csv(movie)
    list = [] #list of lineim
    counter = 0
    print(df)
    for line in range (0,len(df)):
        if not (type(df['What is said'][line]) == float):
            counter+=1
            #print(df['Speaker'][line], '\t', df['What is said'][line])
            list.append( Line(counter, df['Speaker'][line], df['What is said'][line], len(df['What is said'][line].replace('\t', '').replace('  ', '').replace('\n','').split(' '))))
    print(len(list))
    return{'Graph':G, 'list_of_lines': list}


def make_clock_events(lines):
    """
    Return:[Ce,Ce_norm]
    """
    Ce = []
    Ce_norm = []
    max_num_of_events = 0
    for line in lines:
        #print(line)
        Ce.append(line.num)
        if line.num >max_num_of_events:
            max_num_of_events = line.num
    #normCe
    for x in Ce:
        Ce_norm.append(float(x/max_num_of_events))
    return [Ce,Ce_norm]


def make_clock_words(lines):
    """
    Return: [Cw,Cw_norm]
    """
    Cw = []
    Cw_norm = []
    sum_of_words = 0
    for line in lines:
        #print(line)
        sum_of_words += line.num_of_words
        Cw.append(sum_of_words)
    #normCe
    for x in Cw:
        Cw_norm.append(float(x/sum_of_words))
    return [Cw,Cw_norm]


def M_algo(Ce_norm, Cw_norm):
    """
    Return M - array
    """
    M = []
    for i in range(len(Ce_norm)):
        M.append(Cw_norm[i] - Ce_norm[i])
    return M


def convert_sub_to_string_and_filteration(lines):
    """
    collect all words, filering connection words and /'?!,
    Return: full_sub_filtered

    """
    full_sub = ''
    full_sub_filtered = ''
    stopWords = set(stopwords.words('english'))
    ps = PorterStemmer()
    #making full text
    for line in lines:
        full_sub += line.sub
    #striping from סימני פיסוק
    full_sub = full_sub.replace('.', ' ').replace('\\', '').replace('?', ' ').replace('\'','').replace('!', '').replace(',', '').replace(
        '-', '').lower().split()
    #stripping from conjunctions
    for word in full_sub:
        if  word not in stopWords:
            full_sub_filtered+= ' ' + word
    #stripping from linguistic biases
    full_sub= full_sub_filtered
    full_sub = word_tokenize(full_sub_filtered)
    full_sub_filtered = ''
    #print(full_sub)
    for word in full_sub:
            #print(word)
            full_sub_filtered += ' ' + ps.stem(word=word)

    full_sub_filtered = full_sub_filtered.split()
    print(full_sub)
    print(full_sub_filtered)
    return full_sub_filtered


def make_axis_graph(x1,y1,x2,y2,x_label, y_label,first_graph_symbol,second_graph_symbol,title):
    plt.plot(x1, y1, x2, y2)
    plt.legend([first_graph_symbol, second_graph_symbol])
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.grid(True)
    plt.show()


def draw_AB_graph(G, is_it_directed):
    arrowstyl = ''
    if is_it_directed:
        arrowstyl = '-|>'

    position = nx.circular_layout(G)
    edge_labeld = nx.get_edge_attributes(G, 'weight')
    nx.draw(G, pos=position, title='G_direct_no_weights', node_color='r', edge_color='b', arrowstyle=arrowstyl)
    nx.draw_networkx_labels(G, pos=position, font_size=5)
    nx.draw_networkx_edge_labels(G, pos=position, edge_labels=edge_labeld, font_size=5)
    plt.draw()
    plt.show()

def find_maxs_and_mins(list,list_of_time,split_list_for):
    maxlist = {}
    minlist = {}
    x=0
    size_of_part = int(len(list_of_time)/split_list_for)
    reminder_size = len(list_of_time)%split_list_for
    for i in range(0,split_list_for):
        local_max = 0
        local_max_location = 0
        local_min = 99999
        local_min_location = 0
        for j in range(x,x+size_of_part):
            if(list[j]>local_max):
                local_max= list[j]
                local_max_location = j
            elif list[j]<local_min:
                local_min = list[j]
                local_min_location = j
        maxlist[local_max_location] = local_max
        minlist[local_min_location] = local_min
        x += size_of_part
    if reminder_size !=0:
        for j in range(x,x+reminder_size):
            if(list[j]>local_max):
                local_max= list[j]
                local_max_location = j
            elif list[j]<local_min:
                local_min = list[j]
                local_min_location = j
        maxlist[local_max_location] = local_max
        minlist[local_min_location] = local_min
    print('Max_List:',maxlist)
    print('Min_list:', minlist)
    return {'max':maxlist, 'min': minlist}

def main(*argv):

    #make_civilwar_script()

    G = make_all_graphs()

    G_direct_weighted = G[0]
    G_direct_no_weights = G[1]
    G_undircet_weighted = G[2]
    G_undircet_no_weights = G[3]
    G_undircet_no_weights.adjacency()
    G_direct_weighted.adjacency()
    mat = nx.to_numpy_matrix(G_direct_weighted, nodelist=list(G_direct_weighted.nodes))
    mat1 = nx.adjacency_matrix(G_direct_weighted)
    mat2 = nx.to_scipy_sparse_matrix(G_direct_weighted)
    mat3 = nx.to_dict_of_dicts(G_direct_weighted)

    """Best way of conversion"""
    mat4 = nx.to_numpy_array(G_direct_weighted)  # best way of convertion """
    print('new:\n', G_undircet_no_weights.degree(), '\n', mat)
    np.set_printoptions(threshold=np.inf)

    print('matrix after alteration with lowest distances:', mat4)
    print('networkx.algorithms.hierarchy.flow_hierarchy(G_direct_weighted):\n', networkx.algorithms.hierarchy.flow_hierarchy(G_direct_weighted))


if __name__ == "__main__":
    main(sys.argv[1:])
