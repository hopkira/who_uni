import wikitextparser as wtp
from wikitextparser import remove_markup, parse


file = open("./clean.mw")

string = file.read()

story_text = wtp.parse(string)

num=0

for section in story_text.sections:
    string = section.string
    string = string.replace('== Plot ==','')
    filename = "story" + str(num) + ".txt"
    text_file = open(filename, "w")
    text_file.write(string)
    text_file.close()
    num=num+1