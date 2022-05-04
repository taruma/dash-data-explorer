import plotly.io as pio
import plotly.graph_objects as go
import configparser

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
)
hktemplate.layout.margin = dict(l=0, r=0, b=0)
hktemplate.layout.mapbox = dict(
    bearing=0, style="carto-positron", zoom=4, pitch=0, accesstoken=MAPBOX_TOKEN
)
hktemplate.layout.height = 500  # only affects map
hktemplate.layout.showlegend = False

# SPECIFIC PLOT
# SCATTERMAPBOX
hktemplate.data.scattermapbox = [
    go.Scattermapbox(mode="markers", marker=go.scattermapbox.Marker(size=10))
]

# HEATMAP
hktemplate.data.heatmap = [go.Heatmap(colorscale=HEATMAP_COLOR)]

emtpy_fig = go.Figure(
    data=[{"x": [], "y": []}],
    layout=go.Layout(
        template="none",
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        height=200,
    ),
)
