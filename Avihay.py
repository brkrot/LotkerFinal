import codecs
import re
import string
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


