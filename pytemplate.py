import plotly.io as pio
import plotly.graph_objects as go
import configparser
import dash_bootstrap_components as dbc
from dash import html

# CONFIG
CONFIG_PATH = "config.ini"
config = configparser.ConfigParser()
config.read(CONFIG_PATH)
MAPBOX_TOKEN = config["PLOTLY"]["MAPBOX_TOKEN"]
MAPBOX_TOKEN = None if MAPBOX_TOKEN == "" else MAPBOX_TOKEN

# CHANGE VAR HERE
SOURCE_IMAGE = (
    "https://raw.githubusercontent.com/hidrokit/"
    + "static-assets/main/logo_0.4.0-v1.1/hidrokit-hidrokit/400x100/"
    + "400x100transparent.png"
)
BASED_TEMPLATE = "plotly"
HEATMAP_COLOR = "Blackbody"  # Viridis, Blackbody, Plasma, Blues, Aggrnyl

# TEMPLATE BASED ON
hktemplate = pio.templates[BASED_TEMPLATE]

# GENERAL LAYOUT
hktemplate.layout.hovermode = "x"
hktemplate.layout.images = [
    dict(
        source=SOURCE_IMAGE,
        xref="paper",
        yref="paper",
        x=1,
        y=1.05,
        sizex=0.1,
        sizey=0.2,
        xanchor="right",
        yanchor="bottom",
        name="logo-hidrokit",
    )
]
hktemplate.layout.title = dict(
    xanchor="left",
    yanchor="top",
    x=0,
    y=1,
    xref="paper",
    yref="paper",
    font={"size": 20},
)
hktemplate.layout.margin = dict(l=0, r=0, b=0)
hktemplate.layout.mapbox = dict(
    bearing=0,
    style="stamen-watercolor",
    zoom=4.5,
    pitch=100,
    accesstoken=MAPBOX_TOKEN,
)
hktemplate.layout.height = 500  # only affects map
hktemplate.layout.showlegend = False
hktemplate.layout.font = {"family": "Neucha"}
hktemplate.layout.hoverlabel = {"font_family": "Neucha"}
hktemplate.layout.xaxis = {
    "showline": True,
    "linewidth": 2,
    "linecolor": "black",
    "mirror": True,
    "automargin": True,
    "gridcolor": "#bdbdbd",
    "spikecolor": "Dodgerblue",
    "spikethickness": 1,
    "spikemode": "across",
    "spikedash": "solid",
}
hktemplate.layout.yaxis = {
    "showline": True,
    "linewidth": 2,
    "linecolor": "black",
    "mirror": True,
    "automargin": True,
    "gridcolor": "#bdbdbd",
    "zerolinecolor": "#bdbdbd",
    "zerolinewidth": 2,
    "rangemode": "tozero",
    "spikecolor": "Dodgerblue",
    "spikethickness": 2,
    "spikedash": "solid",
}
hktemplate.layout.xaxis.title = {"font": {"size": 20}, "standoff": 15}
hktemplate.layout.yaxis.title = {"font": {"size": 15}, "standoff": 15}
hktemplate.layout.legend = {
    "yanchor": "top",
    "y": 1,
    "xanchor": "left",
    "x": 0,
    "orientation": "h",
    # "bgcolor": "rgba(0,0,0,0)",
    "bgcolor": "rgba(250, 240, 230, 0.5)",
    "font": {"size": 15},
}
hktemplate.layout.paper_bgcolor = "white"
hktemplate.layout.plot_bgcolor = "white"

# SPECIFIC PLOT
# SCATTERMAPBOX
hktemplate.data.scattermapbox = [
    go.Scattermapbox(
        mode="markers",
        # marker=go.scattermapbox.Marker(size=10, color="DodgerBlue"),
        marker={
            "size": 15,
            "color": "FireBrick",
            "opacity": 0.9,
        },
        hovertemplate="%{customdata} - %{text}<br>(%{lat:.5f}, %{lon:.5f})<extra></extra>",
        hoverlabel={
            "font_family": "Neucha",
            "bgcolor": "Tomato",
            "bordercolor": "FireBrick",
            "font": {"color": "white", "size": 15},
            "align": "right",
            "namelength": 5,
        },
        line={"width": 2, "color": "black"},
    )
]

# HEATMAP
hktemplate.data.heatmap = [
    go.Heatmap(
        colorscale=HEATMAP_COLOR,
        textfont={"family": "Neucha"},
        colorbar={
            "orientation": "v",
            "outlinecolor": "black",
            "outlinewidth": 2,
            "ticksuffix": "%",
            "x": 1,
            "xpad": 10,
            "y": 0.5,
            "ypad": 0,
            # "title": {
            #     "font": {"color": "black", "size": 20},
            #     "side": "top",
            #     "text": "💯",
            # },  # BUGGED
        },
        hovertemplate="📅: %{customdata}<br>🆔: %{y}<br>💯: %{z}%<extra></extra>",
        hoverlabel={"bordercolor": "black", "font": {"color": "white"}},
    )
]

hktemplate.data.scatter = [go.Scatter(mode="lines")]

emtpy_fig = go.Figure(
    data=[{"x": [], "y": []}],
    layout=go.Layout(
        template="none",
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        height=200,
    ),
)

MD_TUTORIAL = """
# ✍️ PETUNJUK PENGGUNAAN 🤔
- Buka 🧑‍💻 situs ini melalui komputer/laptop 💻.
- Navigasi 🧭 menggunakan 📊 plotly:
    - Gunakan 🖱️ berbagai opsi bar yang muncul di kanan 👉 atas ☝️ setiap grafik 📈. 
    - Klik ✌️ dua kali untuk mereset zoom 🔍 (saat opsi zoom/pan).
- Untuk memilih 🛖 bisa dengan: 
    - _Click_ 👆 atau _Box 📦 / Lasso 🪢 Select_ _marker_ yang ada di peta 🗺️. (Tahan Shift untuk memilih lebih dari satu)
    - Dari menu 📃 _dropdown_ pilih 🛖 atau ketik ⌨️ nama/id stasiun yang ingin dilihat 🙄.
- Pilih 🧮 parameter yang ingin dilihat 🙈.
- Klik tombol 🔳 "Tampilkan Grafik".
"""

ALERT_SOURCECODE = html.Div(
    dbc.Alert(
        [
            "source code aplikasi ini bisa dilihat di ".lower(),
            html.A(
                "repository taruma/dash-bmkg-data-explorer",
                href="https://github.com/taruma/dash-bmkg-data-explorer",
            ),
            ".",
        ],
        color="info",
        className="fw-bold text-center",
    ),
)

ALERT_IMNOTBMKG = html.Div(
    dbc.Alert(
        "Situs ini tidak terafiliasi dengan BMKG. Situs ini hanya untuk demonstrasi dashboard dan merupakan proyek hobi. Bukan untuk digunakan untuk pekerjaan/penelitian.".lower(),
        color="danger",
        className="fw-bold text-center",
    ),
)

ALERT_DEMO = html.Div(
    dbc.Alert(
        [
            "Situs 💻 ini merupakan 🪧 demonstrasi dash-🛹 untuk ✈️eksplorasi data ".lower(),
            html.Del(
                "meteorologi dan klimatologi", style={"text-decoration-style": "double"}
            ),
            " ❄️♨️🔥🍃🌧️🌞💨↗️🎐🎯 pada setiap 🛖",
        ],
        color="success",
        className="fw-bold fs-5 rounded text-center",
    )
)

HTML_INFO = html.Div(
    html.P(
        [
            "⚠️ Demonstrasi dengan dataset bmkg hanya tersedia pada tanggal 4 Mei 2022 - 6 Mei 2022 ⚠️".lower(),
            html.P(
                [
                    "🪧 kunjungi ",
                    dbc.Badge(
                        # html.A(
                        "video 📺 ini",
                        #     href="https://www.youtube.com/watch?v=IjDjnqQaYu8",
                        #     className="text-white",
                        # ),
                        color="info",
                        className="mb-1",
                        style={"text-decoration": "none"},
                        href="https://www.youtube.com/watch?v=IjDjnqQaYu8",
                        target="_blank",
                    ),
                    " untuk melihat demonstrasi dengan data bmkg dan tanpa kehebohan emoji 🤭 🪧",
                ]
            ),
        ],
        className="text-center rounded rounded-4 bg-danger text-white fw-bold",
        style={"letter-spacing": "2px"},
    ),
    # className="bg-warning",
)

HTML_FOOTER = html.Div(
    html.Footer(
        [
            html.Span("\u00A9"),
            " 2022-2024 ",
            html.A(
                "Taruma Sakti Megariansyah".lower(),
                href="https://github.com/taruma",
            ),
            ". MIT License. repository on 👉 ".lower(),
            dbc.Badge(
                "Github".lower(),
                href="https://github.com/taruma/dash-bmkg-data-explorer",
                color="secondary",
                class_name="text-uppercase fs-6",
                id="tooltip-github",
                target="_blank",
                style={"letter-spacing": "3px", "text-decoration": "none"},
            ),
            dbc.Tooltip(
                "👇 click me 👇", target="tooltip-github", placement="top", autohide=False
            ),
            " 👈.",
        ],
        className="text-center",
    ),
)

HTML_CREATEDBY = html.Div(
    [
        "📭 ",
        dbc.Badge(
            "✨ open-source ✨",
            color="success",
            style={"cursor": "pointer", "letter-spacing": "3px"},
            id="tooltip-created",
            className="text-uppercase",
        ),
        dbc.Tooltip(
            "link to repository at bottom page",
            target="tooltip-created",
            placement="bottom",
            className="fw-bold",
        ),
        " 🛠️ project by ",
        html.A("taruma", href="https://github.com/taruma"),
        " & 👨‍🚒 powered by ",
        html.A("hidrokit", href="https://github.com/hidrokit"),
    ],
    className="text-center fw-bolder mb-4 fs-5",
)
