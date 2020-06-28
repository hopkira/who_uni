import wikitextparser as wtp
from wikitextparser import remove_markup, parse

file = open("./part_cleaned.mw")

string = file.read()

story_text = wtp.parse(string)

for section in story_text.sections:
    title = str(section.title).strip()
    if title == "Plot":
        print(section.string)