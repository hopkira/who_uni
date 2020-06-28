import untangle
import wikitextparser as wtp
from wikitextparser import remove_markup, parse

wiki_file = "./Wikipedia.xml"

wiki_obj = untangle.parse(wiki_file)

stories = wiki_obj.mediawiki.page

#wiki_page = wtp.parse(stories[1].revision.text.cdata)

for story in stories:
    print("========= STORY =============")
    story_text = wtp.parse(story.revision.text.cdata)
    sec_num = 0
    for section in story_text.sections:
        title = str(section.title).strip()
        if title == "Plot" or title == "Synopsis":
            sub_sec_num = 0
            for sub_section in section.sections:
                sub_title = str(sub_section.title).strip()
                if title == "Plot" or title == "Synopsis":
                    pass
                else:
                    #print("I'm deleting " + story_text.sections.section.sub_section.title)
                    del story_text.sections[sec_num][sub_sec_num]
            sub_sec_num = sub_sec_num + 1
        else:
            #print("I'm deleting " + story_text.sections.section.title)
            del story_text.sections[sec_num]
        sec_num = sec_num + 1
    print(story_text)