import untangle
import wikitextparser as wtp
from wikitextparser import remove_markup, parse

wiki_file = "./Wikipedia.xml"

wiki_obj = untangle.parse(wiki_file)

stories = wiki_obj.mediawiki.page

#wiki_page = wtp.parse(stories[1].revision.text.cdata)

for story in stories:
    story_text = wtp.parse(story.revision.text.cdata)
    plain_text = ""
    for section in story_text.sections:
        title = str(section.title).strip()
        #print("+"+title+"+")
        if title == "Plot" or title == "Synopsis":
            try:
                plain_text = remove_markup(section.string)

            except:
                pass
    print(plain_text)