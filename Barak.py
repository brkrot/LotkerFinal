import csv
import pathlib


def abCSV():
    '************************************PART 1.D --> AB.CSV***************************************************'
    scriptFile = "Dark Knight Rises.txt"
    subtitlesFile = "Dark Knight Rises.srt"
    text = open(scriptFile, encoding="utf8").read().splitlines()
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
    for line in text:
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
        while (not nextSpeaker in text[speakerText]):
            line = text[speakerText].strip()
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
    # print("whatIsSaid")
    # print(whatIsSaid)
    # export the table to a CSV file
    i = 0
    size = len(response)
    with open('AB.csv', 'w') as csvfile:
        table_write = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        table_write.writerow(("Response", 'Speaker', 'What is said'))
        for line in range(0, size - 1):
            if (i <= len(response)):
                table_write.writerow((response[i], speakers[i], whatIsSaid[i]))
            i = i + 1
    '************************************PART D***************************************************'


abCSV()
