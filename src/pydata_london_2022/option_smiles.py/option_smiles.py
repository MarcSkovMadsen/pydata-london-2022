"""
PyData London 2022 - Man Group Charting Competition

Source: https://github.com/man-group/pydata2022

```bash
pip install pandas pyarrow panel hvplot holoviews 
```
"""
import pandas as pd
import panel as pn
import hvplot.pandas
import holoviews as hv
from io import StringIO

pn.config.raw_css.append(
    """
  .bk-root {
    height: calc( 100vh - 150px ) !important;
  }
  """
)

pn.extension(sizing_mode="stretch_width", template="fast")
SITE = "Man-Group"
TITLE = "Options Analytics"
LOGO = "https://pydata.org/london2022/wp-content/uploads/2022/02/PyData_logo.png"

SOURCE_DATA = "https://github.com/man-group/pydata2022/raw/main/option_chain_data.parquet"
LOCAL_DATA = "option_chain_data.parquet"

COLUMNS = [
    "type",
    "strike",
    "inTheMoney",
    "impliedVolatility",
    "lastPrice",
    "lastTradeDate",
    "volume",
    "openInterest",
    "bid",
    "ask",
    "spread",
    "change",
    "percentChange",
    "contractSymbol",
]

HOVER_COLS = [
    "strike",
    "impliedVolatility",
    "lastPrice",
    "volume",
    "openInterest",
    "bid",
    "ask",
    "spread",
    "contractSymbol",
]


def extract():
    try:
        return pd.read_parquet(LOCAL_DATA)
    except FileNotFoundError:
        data = pd.read_parquet(SOURCE_DATA)
        data.to_parquet(LOCAL_DATA)
        return data


source_data = extract()


def transform(data: pd.DataFrame) -> pd.DataFrame:
    data["date"] = data["date"].astype("datetime64[ns]")
    data["inTheMoney"] = data["inTheMoney"].astype("bool")

    data["spread"] = data["ask"] - data["bid"]
    return data[COLUMNS]


data = transform(source_data)


def get_plots(data: pd.DataFrame):
    call_data = data[data["type"] == "Call"]
    put_data = data[data["type"] == "Put"]
    plots = [
        call_data.hvplot(
            x="strike",
            y="impliedVolatility",
            responsive=True,
            min_height=300,
            ylabel="Implied Volatility",
            title="Call",
            hover_cols=HOVER_COLS,
        ),
        put_data.hvplot(
            x="strike",
            y="impliedVolatility",
            responsive=True,
            min_height=300,
            ylabel="Implied Volatility",
            title="Put",
            hover_cols=HOVER_COLS,
        ),
        call_data.hvplot(
            x="strike",
            y="openInterest",
            responsive=True,
            height=200,
            ylabel="Open Interest",
            hover_cols=HOVER_COLS,
        ),
        put_data.hvplot(
            x="strike",
            y="openInterest",
            responsive=True,
            height=200,
            ylabel="Open Interest",
            hover_cols=HOVER_COLS,
        ),
        call_data.hvplot(
            x="strike",
            y="spread",
            responsive=True,
            height=200,
            ylabel="Spread",
            hover_cols=HOVER_COLS,
        ),
        put_data.hvplot(
            x="strike",
            y="spread",
            responsive=True,
            height=200,
            ylabel="Spread",
            hover_cols=HOVER_COLS,
        ),
    ]
    layout = hv.Layout(plots).cols(2)
    return layout


plots = get_plots(data)


def get_stringio(data: pd.DataFrame) -> StringIO:
    sio = StringIO()
    data.to_csv(sio)
    sio.seek(0)
    return sio


sio_to_download = get_stringio(data)

stock_selector = pn.widgets.Select(options=["Google"], name="Name", max_width=300)
download_button = pn.widgets.FileDownload(
    sio_to_download,
    embed=True,
    filename="google.csv",
    sizing_mode="fixed",
    width=150,
    height=52,
    name="Download",
    label="google.csv"
)

plot_pane = pn.pane.HoloViews(plots, sizing_mode="stretch_both")
pivot_pane = pn.pane.Perspective(data, sizing_mode="stretch_both")
doc_pane = pn.pane.Markdown("""
# Option Chain Visualization

The *Option Analytics* tool was developed as a part of the PyData London 2022 chart visualization competition by **Man-Group**. 

The data is *option chain data*. See [Investopedia - Option Chain](https://www.investopedia.com/terms/o/optionchain.asp#:~:text=An%20options%20chain%2C%20also%20known,within%20a%20given%20maturity%20period).

Source: [man-group/pydata2022](https://github.com/man-group/pydata2022)
""", name="🎓 Docs")
tab_layout = pn.Tabs(("📈 Plot", plot_pane), ("🛠️ Pivot", pivot_pane), doc_pane, margin=10)
tool_layout = pn.Column(
    pn.Row(stock_selector, download_button, margin=(10,0,20,0)),
    tab_layout,
).servable()

template = pn.state.template
template.param.update(
    site="Man-Group Viz Competition",
    title=TITLE,
    logo=LOGO,
)
if template.theme == pn.template.DarkTheme:
    pivot_pane.theme = "material-dark"
