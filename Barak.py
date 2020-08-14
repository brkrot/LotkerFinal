import csv
import pathlib
from  networkx import networkx as nx  ,dijkstra_path_length as spw,floyd_warshall_numpy as mat ,neighbors
import matplotlib.pyplot as plt
import numpy as np
import sys

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

def voronoi(G):
    global color_map
    G2 = nx.Graph()

    #Converting frequencies to distances
    for u, v, d in G.edges(data=True):
        G2.add_edge(u, v, weight=(1 / d['weight']))

    # Choosing 2 Ankers and as a result -> Dividing the Graph to 2 partitions
    anker1 = 'TONY STARK'
    anker2 = ['STEVE ROGERS','STEVE ROGERS']
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

def voting(G,i,j):
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
    print(allEdgesWeight)

    m = nx.convert_matrix.to_numpy_matrix(G)
    print(m)


#divide each directed egde in the sum of edges weight from vertex V  (- normelaize the matrix)
    for k in range(m.shape[0]):
        print(m[k].sum())
        m[k]/=m[k].sum()
    print(m)

    #Setting Ankers  - "Eater Vertex"
    m[i]=0
    m[i,i]=1
    m[j] = 0
    m[j,j] = 1

    print('VOTING  - MATRIX WITH ANKORS!\n',m)
    for k in range (0,4):
        m=np.dot(m,m)
        print ('Mult -',k,'- :\n',m)
    list_for_return = list()
    ank1 = list()#anckor 1 full list with 0's
    ank2 = list()#anckor 2 full list with 0's
    ank1_list = list() # list without 0's
    ank2_list = list() # list without 0's
    for k in range (0,8):
        if m[k, i] >= m[k, j]:
            ank1.append(m[k, i])
            ank1_list.append(m[k, i])
            ank2.append(0)
        else:
            ank2.append(m[k, j])
            ank2_list.append(m[k, j])
            ank1.append(0)

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

def narrowGraphTo8MainCharacters(G,speakers):

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

def VORONOI(movieName):
    speakers = getTheSpeakersNames(movieName)
    abGraph = buildGraphFromList(speakers)
    drawGraph(abGraph, 0)
    smallABGraph = narrowGraphTo8MainCharacters(abGraph,speakers)
    smallGraphWithPartitions_Voronoi = voronoi(smallABGraph)
    drawGraph(smallGraphWithPartitions_Voronoi, 1)
