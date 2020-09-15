import csv
import pathlib
from  networkx import networkx as nx  ,dijkstra_path_length as spw,floyd_warshall_numpy as mat ,neighbors
import matplotlib.pyplot as plt
import numpy as np
from networkx.algorithms.community import kernighan_lin_bisection, greedy_modularity_communities
from  networkx import networkx as nx
import networkx
from scipy.optimize import minimize
import numpy as np
import networkx.algorithms.community as nxac
from  networkx import networkx as nx  ,dijkstra_path_length as spw,floyd_warshall_numpy as mat ,neighbors
import pandas as pd
from dataclasses import dataclass
import string


@dataclass
class Line:
    num: int
    talker: string
    sub: string
    #num_of_words: int

@dataclass
class SingleSurface:
    x: []
    y: []
    name: string


def makeABandScriptSrt(MovieName):
    print(MovieName)
    '************************************PART 1 AB.CSV***************************************************'
    scriptFile = MovieName+".txt"
    subtitlesFile = MovieName+".srt"
    scriptText = open(scriptFile, encoding="utf8").read().splitlines()
    # Initilizg all the 3 lists
    response = []
    speakers = []
    speakersLineInTheText = []
    whatIsSaid = []
    'List of all the "forbidden" words or symbols etc...'
    forbidden = ['1', '2', '3', '4', '5', '(', '.', '6', '7', '8', '9', 'HISSES', 'ENTIRELY', '0', 'CHAMBER', 'POV',
                 'INQUIRY', 'SCENE', 'STRAIGHT', 'INT', 'CONTINUED', 'EXT', 'FADE', 'OMITTED', '"', '-', ':', 'VOICE',
                 '!', 'OMITTED', 'THE END', 'GASPS']
    # Stage 1 - finding the names of the speakers(and the line in the script where it happens)
    i = 0
    for line in scriptText:
        line = line.strip()
        if (line.isupper()):
            # Only for cleaning the look of it
            line = line.replace(' (O.S.)', '')
            line = line.replace(' (V.O.)', '')
            # Checking we dont have a forbidden word/symbol
            j = 0
            bad = 0
            for mistake in forbidden:
                if forbidden[j] in line:
                    bad = 1
                j += 1
            if bad == 0:
                # getting the line it the text
                speakersLineInTheText.append(i)
                #  Add the line to names array
                speakers.append(line)
        i = i + 1
    # Stage 2 - Getting the response number
    i = 1
    for name in speakers:
        if (i <= len(speakers)):
            response.append(i)
        i = i + 1
    # Stage 3 - What was said
    str = ""
    for i in range(len(speakers) - 1):
        speakerText = speakersLineInTheText[i] + 1

        # Stopping at the next speaker
        nextSpeaker = speakers[i + 1]

        # Getting all the lines of the speaker
        while (not nextSpeaker in scriptText[speakerText]):
            line = scriptText[speakerText].strip()
            if 'INT' in line or '(CONTINUED)' in line or line.isdigit() or '(' in line or ' 3/1/02' in line or 'FOOTSTEPS' in line or 'DISSOLVE' in line:
                break
            if 'EXT' in line or 'INSERT' in line or 'OPENS' in line or 'OMITTED' in line or 'CRASH!' in line or 'APPEARS' in line or 'LURCHES,' in line:
                break
            if 'DROPS' in line or 'EMBOSSED' in line or ' THE CHAMBER OF SECRETS' in line or 'OMITTED' in line or 'CRASH!' in line or 'APPEARS' in line or 'LURCHES,' in line:
                break
            str += line + ' '
            speakerText += 1

        whatIsSaid.append(str)
        str = ""

    # export the table to a CSV file
    i = 0
    size = len(response)
    with open(MovieName+' AB.csv', 'w',encoding='utf8') as csvfile:
        table_write = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        table_write.writerow(("Response", 'Speaker', 'What is said'))
        for line in range(0, size - 1):
            if (i <= len(response)):
                table_write.writerow((response[i], speakers[i], whatIsSaid[i]))
            i = i + 1
    '************************************PART D***************************************************'
    EnglishSubtitles = open(subtitlesFile, encoding="utf8").read()
    SubtitlesList = EnglishSubtitles.split('\n\n')
    # Initlizing the lists
    number = []
    beginTime = []
    endTime = []
    scriptText = []

    for singleSubtitle in SubtitlesList:
        if (singleSubtitle == ''):
            break
        subtitleParts = singleSubtitle.split('\n')
        # print(subtitleParts)
        times = subtitleParts[1].split(' --> ')
        number.append(subtitleParts[0])
        str = ''
        for i in range(2, len(subtitleParts)):
            str += ' '
            str += subtitleParts[i].replace('-', '')
        scriptText.append(str)
        beginTime.append(times[0])
        endTime.append(times[1])
    '************************************Merging***************************************************'
    subtitles = scriptText
    srtDictionary = {}
    set = []
    # Getting all the words that are "special" - have only one instance + their location in the subtitles order
    # a part of the set is word, its last location said, number of times
    # since we dont care for those words who has more than one time in the srt, the last location is good for us
    for i in range(len(subtitles)):
        words = subtitles[i].split(' ')     #A whole row to seperate words
        for word in words:
            # Cleaning the symbols
            word = word.replace('.', '').replace('!', '').replace(',', ' ').replace('"', '').replace('?', '').replace(
                ' ', '').replace("'s", '').lower()

            set.append(i + 1)       #Is set the words locations?
            # getting the information of the word
            if word in srtDictionary:
                # srtDictionary[word][1] = the number of the instances of the word
                set.append(srtDictionary[word][1] + 1)
            else:
                set.append(1)
            srtDictionary[word] = set
            set = []
    # print (srtDictionary)
    del (srtDictionary[''])
    # print (srtDictionary)

    # initilaing the names list with X| srt name is the speaker of the specific talker of the subtitle
    subtitleSpeaker = []
    for i in range(len(scriptText)+1):
        subtitleSpeaker.append('X')

    currentSpeaker = 'X'
    # Run for all the word in the dictionary
    for word in srtDictionary:
        # Deal only with words with 1 instance
        if srtDictionary[word][1] == 1:

            # search the specific word in the script
            for i in range(len(whatIsSaid)):
                if (word in whatIsSaid[i]):
                    # Finding the name of the speaker
                    currentSpeaker = speakers[i]
            # Put the name of the speaker in @srtName, srtDictionary[word][0] =the number of the subtitle
            subNumber = srtDictionary[word][0]
           #print(subNumber)
            subtitleSpeaker[subNumber] = currentSpeaker
            # print(word, srtDictionary[word],currentSpeaker)

    with open(MovieName+' srt-script.csv', 'w',encoding='utf8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(("Speaker", 'Begin time', 'End time', 'Text'))
        for i in range(0, len(number) - 1):
            writer.writerow((subtitleSpeaker[i], beginTime[i], endTime[i], scriptText[i]))

def getTheSpeakersNames(MovieName):
    print(MovieName)
    '************************************PART 1 AB.CSV***************************************************'
    scriptFile = MovieName+".txt"
    subtitlesFile = MovieName+".srt"
    scriptText = open(scriptFile, encoding="utf8").read().splitlines()
    # Initilizg all the 3 lists
    response = []
    speakers = []
    speakersLineInTheText = []
    whatIsSaid = []
    'List of all the "forbidden" words or symbols etc...'
    forbidden = ['1', '2', '3', '4', '5', '(', '.', '6', '7', '8', '9', 'HISSES', 'ENTIRELY', '0', 'CHAMBER', 'POV',
                 'INQUIRY', 'SCENE', 'STRAIGHT', 'INT', 'CONTINUED', 'EXT', 'FADE', 'OMITTED', '"', '-', ':', 'VOICE',
                 '!', 'OMITTED', 'THE END', 'GASPS']
    # Stage 1 - finding the names of the speakers(and the line in the script where it happens)
    i = 0
    for line in scriptText:
        line = line.strip()
        if (line.isupper()):
            # Only for cleaning the look of it
            line = line.replace(' (O.S.)', '')
            line = line.replace(' (V.O.)', '')
            # Checking we dont have a forbidden word/symbol
            j = 0
            bad = 0
            for mistake in forbidden:
                if forbidden[j] in line:
                    bad = 1
                j += 1
            if bad == 0:
                # getting the line it the text
                speakersLineInTheText.append(i)
                #  Add the line to names array
                speakers.append(line)
        i = i + 1
    return (speakers)

def buildGraphFromList(speakers):
    edges = []
    G = nx.Graph()
    for i in range(0, len(speakers) - 2):
        if(speakers[i]!=speakers[i+1]):
            if (G.has_edge(speakers[i], speakers[i + 1])):
                G[speakers[i]][speakers[i + 1]]['weight'] += 1

            else:
                G.add_edge(speakers[i], speakers[i + 1], weight=1)

    return G

def voronoi2(G,movie):
    global color_map
    G2 = nx.Graph()

    #Converting frequencies to distances
    for u, v, d in G.edges(data=True):
        G2.add_edge(u, v, weight=(1 / d['weight']))

    # Choosing 2 Ankers and as a result -> Dividing the Graph to 2 partitions
    if movie == 'Captain America - Civil War':
        anker1 = 'STEVE ROGERS'
        anker2 = ['TONY STARK', 'NATASHA ROMANOFF']
    else:
        anker1 = 'WAYNE'
        anker2 = ['BANE', 'SELINA']

    color_map = []
    for v in G2:
        # print('v=' +str(v)," to anker:",anker1,'|',spw(G2, v, anker1)," to anker:",anker2,'|',spw(G2, v, anker2))
        if (v == anker1):
            color_map.append('blue')
        elif (v in anker2):
            color_map.append('red')

        elif (spw(G2, v, anker1) < spw(G2, v, anker2[0]) and spw(G2, v, anker1) < spw(G2, v, anker2[1])):
            color_map.append('blue')
        else:
            color_map.append('red')
    return G2

def voting2(G, i, j,movieName):
    #(i,j) are vertixes we anchored
    #drawGraph(G,0)
    directedG = nx.Graph().to_directed()# from ex1 we already have directed graph
    sum = 0
    allEdgesWeight = {}

    #For each v we sum all the edges wehight
    for v in G:
        vNeighbors = neighbors(G, v)
        for u in vNeighbors:
            sum += G[v][u]['weight']
        allEdgesWeight[v] = sum
        sum = 0
    print('sum of all the edges from the specific vertex')
    print(allEdgesWeight)

    m = nx.convert_matrix.to_numpy_matrix(G)
    print('The graph converted to matrix')
    print(m)


#divide each directed egde in the sum of edges weight from vertex V  (- normelaize the matrix)
    for k in range(m.shape[0]):
        #print(m[k].sum())
        m[k]/=m[k].sum()

    print('Normalized M - directed(!) - weight of the edge is divided by the sum of the edge from this vertex')
    print(m)

    print('\n\n\n')
    #Setting Ankers  - "Eater Vertex"
    m[i]=0
    m[i,i]=1
    m[j] = 0
    m[j,j] = 1

    print('VOTING  - MATRIX WITH ANKORS!\n\n', m)


    print('Multipyng\n\n')
    for k in range (0,4):
        m=np.dot(m,m)
        print ('Mult -',k,'- :\n',m)
    list_for_return = list()
    ank1 = list()#anckor 1 full list with 0's
    ank2 = list()#anckor 2 full list with 0's
    ank1_list = list() # list without 0's
    ank2_list = list() # list without 0's
    for k in range (0,10):
        if m[k, i] >= m[k, j]:
            ank1.append(m[k, i])
            ank1_list.append(m[k, i])
            ank2.append(0)
        else:
            ank2.append(m[k, j])
            ank2_list.append(m[k, j])
            ank1.append(0)
    print('list of groups for the movie',movieName)
    print(ank1)
    print(ank2)

    #
    # for u, v, d in G.edges(data=True):
    #     directedG.add_edge(u, v, weight=d['weight'])
    #     directedG.add_edge(v, u, weight=d['weight'])
    #
    # for v in directedG:
    #     vSize = allEdgesWeight[v]
    #     for u in directedG:
    #         if(directedG.has_edge(v,u)):
    #             directedG[v][u]['weight'] = directedG[v][u]['weight']/vSize
    #
    list_for_return.append(directedG)
    list_for_return.append(ank1_list)
    list_for_return.append(ank2_list)
    list_for_return.append(ank1)
    list_for_return.append(ank2)
    return list_for_return

def drawGraph(G,color):
    position = nx.circular_layout(G)
    edge_labeld = nx.get_edge_attributes(G, 'weight')
    if color==1:
        nx.draw(G, pos=position, node_color=color_map)
    else:
        nx.draw(G, pos=position, node_color='green')
    nx.draw_networkx_labels(G, pos=position, font_size=15)
    nx.draw_networkx_edge_labels(G, pos=position, edge_labels=edge_labeld, font_size=10)
    plt.draw()
    plt.show()
    # nx.draw_circular(G, node_color=color_map, with_labels=True, edge_color='b')
    # plt.show()

def narrowGraphTo10MainCharacters(G, speakers):

    mainCharacters = []
    speakersDictionary = {}


   #Putting all the speakers in a dictionary
    for speaker in speakers:
        if speaker in speakersDictionary:
            speakersDictionary[speaker] = speakersDictionary[speaker] + 1
        else:
            speakersDictionary[speaker] = 1

    #sorting in order to get the main characters
    sortedSpeakers = sorted(speakersDictionary.items(), key=lambda kv: kv[1],reverse=True)
    mainCharactersNumber=10

    for i in range(mainCharactersNumber):
        mainCharacters.append(sortedSpeakers[i][0])

    print()

    G3 = nx.Graph()
    for u, v, d in G.edges(data=True):
        if (u in mainCharacters and v in mainCharacters):
            G3.add_edge(u, v, weight=d['weight'])
    return G3

def voronoi(movieName):
    speakers = getTheSpeakersNames(movieName)
    abGraph = buildGraphFromList(speakers)
    #drawGraph(abGraph, 0)
    smallABGraph = narrowGraphTo10MainCharacters(abGraph, speakers)
    smallGraphWithPartitions_Voronoi = voronoi2(smallABGraph,movieName)
    drawGraph(smallGraphWithPartitions_Voronoi, 1)

def voting(movieName):
    speakers = getTheSpeakersNames(movieName)
    abGraph = buildGraphFromList(speakers)
    #drawGraph(abGraph, 0)
    smallABGraph = narrowGraphTo10MainCharacters(abGraph, speakers)
    #drawGraph(smallABGraph, 0)
    if(movieName=='Dark Knight Rises'):
        voting2(smallABGraph,4,5,movieName) #wane (3), bane(5)  - accordinly34
    else:
        voting2(smallABGraph,1, 8, movieName)  # captain america(1), tony stark(8)


def otherAlgos(movieName):
    speakers = getTheSpeakersNames(movieName)
    abGraph = buildGraphFromList(speakers)
    #drawGraph(abGraph, 0)
    smallABGraph = narrowGraphTo10MainCharacters(abGraph, speakers)
    #drawGraph(smallABGraph, 0)

    print("modularity_communities")
    print(nxac.greedy_modularity_communities(smallABGraph))
    print(nxac.greedy_modularity_communities(abGraph))
    print("centrality")
    print(tuple(sorted(c) for c in next(nxac.centrality.girvan_newman(smallABGraph))))
    print(tuple(sorted(c) for c in next(nxac.centrality.girvan_newman(abGraph))))
    print("k_clique_communities")
    print(sorted(list(nxac.k_clique_communities(smallABGraph,5))))
    print(sorted(list(nxac.k_clique_communities(abGraph, 5))))
    print("hierarchy")
    print (networkx.algorithms.hierarchy.flow_hierarchy(smallABGraph.to_directed()))
    print(networkx.algorithms.hierarchy.flow_hierarchy(abGraph.to_directed()))


def collect_data_from_AB(movie):
    """
    Return: {'list_of_lines': list}
    """
    movie = movie + ' AB.csv'
    df = pd.read_csv(movie)
    list = []  #list of lineim
    counter = 0
    print(df)
    for line in range (0,len(df)):
        counter+=1
        list.append( Line(df['Response'][line], df['Speaker'][line], df['What is said'][line]))#, len(df['What is said'][line].replace('\t', '').replace('  ', '').replace('\n','').split(' '))))
    print(len(list))
    return list

def main_characters_steps(lines,names):
    """
    Return:[dict:mainCharacters]
    """
    mainCharacters = {}
    for i in range(0, 4):
        name = names[i]
        mainCharacters[name] = []
        c = 0
        for i in range(1, len(lines)):
            if name == lines[i].talker:
                c += 2
            mainCharacters[name].append(c)
    return mainCharacters


def print2DSurfaceCentralityGraph(movie, dict, names):

    """
    print2DSurfaceCentralityGraph
    :param movie:
    :param dict:
    :param names:
    :return: printing the 2d graph of the centraliy
    """
    plt.scatter(dict['0X'], dict['0Y'], c='b')
    plt.scatter(dict['1X'], dict['1Y'], c='g')
    plt.scatter(dict['2X'], dict['2Y'], c='r')
    plt.scatter(dict['3X'], dict['3Y'], c='y')
    plt.legend([names[0], names[1], names[2], names[3]])
    plt.title(movie+" -  Degree Centrality Plane  ")
    plt.xlabel("beginning time")
    plt.ylabel("end time")
    plt.show()

def WhoIsTheMax(beg,end,names,stepsFunctionDict):
    """
    WhoIsTheMax - for every point which one is the max
    :param beg: the beginning time in the clock
    :param end: the end time in the clock
    :param names: all the 4 names of the main characters
    :param stepsFunctionDict:
    :return: max's character's number in the names array
    """
    #print(end," ",beg)
    a0 = stepsFunctionDict[names[0]][end] - stepsFunctionDict[names[0]][beg]
    a1 = stepsFunctionDict[names[1]][end] - stepsFunctionDict[names[1]][beg]
    a2 = stepsFunctionDict[names[2]][end] - stepsFunctionDict[names[2]][beg]
    a3 = stepsFunctionDict[names[3]][end] - stepsFunctionDict[names[3]][beg]

    if max(a0,a1,a2,a3)==a0:
        return 0
    elif max(a0,a1,a2,a3)==a1:
        return 1
    elif max(a0,a1,a2,a3)==a2:
        return 2
    elif max(a0,a1,a2,a3)==a3:
        return 3

def WhoIsTheMin(beg,end,names,stepsFunctionDict):
    """
       WhoIsTheMin - for every point which one is the min
       :param beg: the beginning time in the clock
       :param end: the end time in the clock
       :param names: all the 4 names of the main characters
       :param stepsFunctionDict:
       :return: min's character's number in the names array
       """
    #print(end," ",beg)
    a0 = stepsFunctionDict[names[0]][beg]-stepsFunctionDict[names[0]][end]
    a1 = stepsFunctionDict[names[1]][beg] - stepsFunctionDict[names[1]][end]
    a2 = stepsFunctionDict[names[2]][beg] - stepsFunctionDict[names[2]][end]
    a3 = stepsFunctionDict[names[3]][beg] - stepsFunctionDict[names[3]][end]

    if min(a0,a1,a2,a3)==a0:
        return 0
    elif min(a0,a1,a2,a3)==a1:
        return 1
    elif min(a0,a1,a2,a3)==a2:
        return 2
    elif min(a0,a1,a2,a3)==a3:
        return 3

def surface_centrality(movie,names):
    """
    surface_centrality
    :param movie:
    :param names:
    :return: do not return anything, only printing the graph
    """
    lines = collect_data_from_AB(movie)
    stepsFunctionDict4all4characters = main_characters_steps(lines, names)
    # print(stepsFunctionDict4all4characters[names[0]],'\n')
    # print(stepsFunctionDict4all4characters[names[1]], '\n')
    # print(stepsFunctionDict4all4characters[names[2]], '\n')
    # print(stepsFunctionDict4all4characters[names[3]], '\n')

    #Creating room for all the points (2 arrays x,y for each of the characters)
    graphsXYdictionary = {}
    for i in range(0,4):
       graphsXYdictionary[str(i)+'X'] = []
       graphsXYdictionary[str(i)+'Y'] = []


    #Double loop for setting all the dots to be shown on the board
    for beg in range(1, len(lines)-1):
        for end in range(0, len(lines)-1):
            if (end > beg):  # left triangle
                TheNumberOfTheMax = WhoIsTheMax(beg, end, names, stepsFunctionDict4all4characters)
                graphsXYdictionary[str(TheNumberOfTheMax) + 'X'].append(beg)
                graphsXYdictionary[str(TheNumberOfTheMax) + 'Y'].append(end)
            elif (beg > end):   #right triangle
                TheNumberOfTheMax = WhoIsTheMin(beg, end, names, stepsFunctionDict4all4characters)
                graphsXYdictionary[str(TheNumberOfTheMax) + 'X'].append(beg)
                graphsXYdictionary[str(TheNumberOfTheMax) + 'Y'].append(end)

    print2DSurfaceCentralityGraph(movie, graphsXYdictionary, names)


