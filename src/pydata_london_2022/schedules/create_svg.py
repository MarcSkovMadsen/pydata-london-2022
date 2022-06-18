import json
import pathlib

from wordcloud import STOPWORDS as BASE_STOPWORDS
from wordcloud import WordCloud

ROOT = pathlib.Path(__file__).parent
# Source: "https://london2022.pydata.org/cfp/schedule/export/schedule.json"
SCHEDULE = ROOT/"schedule.json"
HEIGHT = 500
WIDTH = 500
STOPWORDS = set(BASE_STOPWORDS)
STOPWORDS.update(("will", "talk", "using", "base", "using", "min", "based"))

def to_event_list(schedule=SCHEDULE):
    f = open(schedule, encoding="utf-8")
    data = json.load(f)

    event_list = []

    for day in data["schedule"]["conference"]["days"]:
        for _, events in day["rooms"].items():
            for event in events:
                event_list.append(event)
    return event_list

EVENT_LIST = to_event_list()
def to_word_cloud(event_list=EVENT_LIST, height=HEIGHT, width=WIDTH, stopwords=STOPWORDS):
    text = ". ".join([item["description"] for item in event_list])


    wordcloud = WordCloud(stopwords=stopwords, background_color="transparent", width=width, height=height, colormap="autumn").generate(text)
    svg = wordcloud.to_svg().replace("Droid Sans Mono", "Roboto")
    return svg

SVG = to_word_cloud()
# (ROOT / "pydata-london-2020-schedules-wordcloud.svg").write_text(SVG)


if __name__.startswith("bokeh"):
    import panel as pn
    pn.config.raw_css.append("""
    body {
        background: blue;
    }
    """)
    pn.extension()
    pn.pane.HTML(SVG, height=HEIGHT, width=WIDTH).servable(target="main")
