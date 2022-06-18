import panel as pn

pn.extension(sizing_mode="stretch_width")

OPTIONS = ["PyData", "PyScript", "Panel"]

def star_string(value):
    return "# " + "⭐"*value

def out(value):
    if value == "PyData":
        return "<img src='https://raw.githubusercontent.com/MarcSkovMadsen/pydata-london-2022/main/docs/pydata-london-2020-schedules-wordcloud.svg'/>"
    elif value == "Panel":
        stars = pn.widgets.IntSlider(value=5, start=0, end=5)
        istar_string=pn.bind(star_string, value=stars)
        return pn.Column(
            "# Panel is probably the most powerful data app framework in Python.",
            "# Panel works with the tools you know and love including PyScript.",
            stars, istar_string,
            "# This app is made with PyScript and Panel.",
            sizing_mode="stretch_width",
        )
    elif value == "PyScript":
        return pn.Column(
            "# PyScript is Python in the Browser.",
            "# PyScript will potentially solve some of Pythons deployment issues.",
            sizing_mode="stretch_width"
        )
    
    return value


selection = pn.widgets.RadioButtonGroup(options=OPTIONS, name="Select", margin=25)
iout = pn.bind(out, value=selection)

pn.Column(selection, iout, height=610, width=510, sizing_mode="fixed").servable(target="main");
