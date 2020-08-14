import csv
import pathlib


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

