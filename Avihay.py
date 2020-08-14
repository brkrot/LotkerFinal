import codecs
import re
import string
import csv
import networkx
import networkx as nx
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import numpy as np
from sympy import Symbol
import transitionMatrix as tm
import pandas
import sys

#AB_FilePath = movieName+' AB.csv'

def make_civilWar_script():
    look_for_ending_bracelet = False
    flag= True
    output_file = open("Captain America - Civil War - altered.txt", "w")
    with codecs.open("Captain_America_-_Civil_War.txt", encoding="utf-8") as in_file:
        while(flag):
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
    position = nx.circular_layout(G_direct_no_weights)
    edge_labeld = nx.get_edge_attributes(G_direct_no_weights, 'weight')
    nx.draw(G_direct_no_weights, pos=position, node_color='r', edge_color='b', arrowstyle='-|>')
    nx.draw_networkx_labels(G_direct_no_weights, pos=position, font_size=5)
    nx.draw_networkx_edge_labels(G_direct_no_weights, pos=position, edge_labels=edge_labeld, font_size=5)
    plt.draw()
    plt.show()

    l1 = sorted(dict_directed_talker_unweighted.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    print("\nDirected $ Unweighted graph 4 main character :\n", l1[0], l1[1], l1[2], l1[3])

    # *********directed graph weighted
    G_direct_weighted = nx.Graph().to_directed()
    for v in dict_directed:
        name = v.split("-&-")
        # print(v, "===", name[0], name[1])
        G_direct_weighted.add_edge(name[0], name[1], weight=int(dict_directed[v]))

        # printing Directed weighted graph
    position = nx.circular_layout(G_direct_weighted)
    edge_labeled = nx.get_edge_attributes(G_direct_weighted, 'weight')
    nx.draw(G_direct_weighted, pos=position, node_color='r', edge_color='b', arrowstyle='-|>')
    nx.draw_networkx_labels(G_direct_weighted, pos=position, font_size=5)
    nx.draw_networkx_edge_labels(G_direct_weighted, pos=position, edge_labels=edge_labeled, font_size=5)
    plt.draw()
    plt.show()

    l1 = sorted(dict_directed_talker_weighted.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    print("\nDirected $ weighted graph 4 main character :\n", l1[0], l1[1], l1[2], l1[3])
    # ******** undirected not weighted graph

    G_undircet_no_weights = nx.Graph()
    for v in dict_undirected:
        name = v.split("-&-")
        G_undircet_no_weights.add_edge(name[0], name[1], weight=1)

        # printing undirected unweighted graph
    position = nx.circular_layout(G_undircet_no_weights)
    edge_labeled = nx.get_edge_attributes(G_undircet_no_weights, 'weight')
    nx.draw(G_undircet_no_weights, pos=position, node_color='r', edge_color='b', arrowstyle='-|>')
    nx.draw_networkx_labels(G_undircet_no_weights, pos=position, font_size=5)
    nx.draw_networkx_edge_labels(G_undircet_no_weights, pos=position, edge_labels=edge_labeled, font_size=5)
    plt.draw()
    plt.show()

    l1 = sorted(dict_undirected_talker_unweighted.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    print("\nUn - Directed $ Unweighted graph 4 main character :\n", l1[0], l1[1], l1[2], l1[3])

    # undirected weighted graph

    G_undircet_weighted = nx.Graph()
    for v in dict_undirected:
        name = v.split("-&-")
        G_undircet_weighted.add_edge(name[0], name[1], weight=int(dict_undirected[v]))

        # printing undirected weighted graph
    position = nx.circular_layout(G_undircet_weighted)
    edge_labeled = nx.get_edge_attributes(G_undircet_weighted, 'weight')

    nx.draw(G_undircet_weighted, pos=position, node_color='r', edge_color='b', arrowstyle='-|>')
    nx.draw_networkx_labels(G_undircet_weighted, pos=position, font_size=5)
    nx.draw_networkx_edge_labels(G_undircet_weighted, pos=position, edge_labels=edge_labeled, font_size=5)
    plt.draw()
    plt.show()

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
    with open('C:\\Users\\DELL\\PycharmProjects\\untitled\\SocialCourse\\srt-English.csv') as csvFile:
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
    del speakersDictionary['i']
    del speakersDictionary['harry/ron']
    str1 = 'HARRY/RON/FRED/GEORGE'
    str1 = str1.lower()
    del speakersDictionary[str1]
    del speakersDictionary['professor']
    del speakersDictionary['harry/ron/hermione']
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
    G3 = nx.Graph().to_directed()
    G3.add_nodes_from(listOfTalkers)
    for y in range(len(listOfTalkers) - 1):
        if ((listOfTalkers[y] != listOfTalkers[y + 1])):
            if ((listOfTalkers[y], listOfTalkers[y + 1]) in G3.edges()):
                G3[listOfTalkers[y]][listOfTalkers[y + 1]]['weight'] += 1
            else:
                G3.add_edge(listOfTalkers[y], listOfTalkers[y + 1], weight=1)
    for i in range(0, 18):
        G3.add_edge(y, y, weight=1)
        y += 1
    # ******************************************************************************************************
    # the Optimization
    Gdw_srt_matrix = nx.to_numpy_matrix(G3)  # srt adjacency matrix
    Gdw_script_matrix = nx.to_numpy_matrix(G_direct_weighted)  # script adjacency matrix
    x = []
    Dx = []
    for i in range(1, 50):  # 49 vertexes
        x.append(Symbol('x' + str(i)))
        Dx.append(x[i - 1])

    def g(Dx):
        Dxdiag = np.diag(Dx)
        ABscript = Dxdiag * Gdw_script_matrix
        A = Gdw_srt_matrix - ABscript
        func = (A * np.transpose(A)).trace()
        return func[0]

    #res = minimize(g, [1] * 49)
    #print(res.x)
    return [G_direct_weighted, G_direct_no_weights, G_undircet_weighted, G_undircet_no_weights]

def main(*argv):
    make_civilWar_script()
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
    print(networkx.algorithms.hierarchy.flow_hierarchy(G_direct_weighted))


if __name__ == "__main__":
    main(sys.argv[1:])