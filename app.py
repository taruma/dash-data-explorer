# -*- coding: utf-8 -*-

import configparser
import dash
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import pytemplate
from dash import dcc, html, Input, Output, State
from pathlib import Path

# FUNCTION NOT GRAPH
def clean_table(df):
    """Replace 8888 and 9999 values to np.nan"""
    df[df == 8888] = np.nan
    df[df == 9999] = np.nan


# PARSE CONFIG
CONFIG_PATH = "config.ini"
config = configparser.ConfigParser()
config.read(CONFIG_PATH)

# DATABASE CONFIGURATION/VARS
FOLDER_BMKG = Path(config["PATH BMKG DATABASE"]["FOLDER_BMKG"])
FILE_NAME_BMKG = config["PATH BMKG DATABASE"]["FILE_NAME_BMKG"]
FILE_NAME_BMKG_COMPLETENESS = config["PATH BMKG DATABASE"][
    "FILE_NAME_BMKG_COMPLETENESS"
]

# PLOTLY CONFIGURATION/VARS
EMPTY_FIG = pytemplate.emtpy_fig
SELECTED_MAX = int(config["PLOTLY"]["SELECTED_MAX"])

# DASH CONFIGURATION/VARS
CONFIG_DCC_GRAPH = {"modeBarButtonsToRemove": ["toImage"]}
DEBUG = int(config["DASH"]["DEBUG"])
BOOTSTRAP_THEME = config["BOOTSTRAP"]["THEME"]
APP_TITLE = "BMKG Data Explorer".lower()
APP_UPDATE_TITLE = "Perbarui...".lower()

# SETUP PLOTLY TEMPLATE
pio.templates.default = pytemplate.hktemplate

# PATH DATABASE
FILE_BMKG = FOLDER_BMKG / FILE_NAME_BMKG
FILE_COMPLETENESS = FOLDER_BMKG / FILE_NAME_BMKG_COMPLETENESS

# READ METADATA DATABASE
with pd.HDFStore(FILE_BMKG, mode="r") as store:
    metadata_files = store.get("/metadata/files")

# PLOTLY OPTIONS
# DROPDOWN STATIONS
options_stations = [
    {"label": f"{stat_id} - {stat_name}".lower(), "value": stat_id}
    for stat_id, stat_name in zip(metadata_files.index, metadata_files["Nama Stasiun"])
]

# DROPDOWN PARAMETER
LABEL_PARAMETER_ABBR = "Tn Tx Tavg RH_avg RR ss ff_x ddd_x ff_avg ddd_car".split()
LABEL_PARAMETER_NAME = (
    (
        "❄️ Temperatur minimum (°C),♨️ Temperatur maksimum (°C),🔥 Temperatur rata-rata (°C),"
        + "🍃 Kelembapan rata-rata (%),🌧️ Curah hujan (mm),🌞 Lamanya penyinaran matahari (jam),💨 Kecepatan angin maksimum (m/s)"
        + ",↗️ Arah angin saat kecepatan maksimum (°),🎐 Kecepatan angin rata-rata (m/s),🎯 Arah angin terbanyak (°)"
    )
    .lower()
    .split(",")
)
label_parameter = dict(zip(LABEL_PARAMETER_ABBR, LABEL_PARAMETER_NAME))
options_parameter = [
    {"label": par_name, "value": par_abbr}
    for par_abbr, par_name in label_parameter.items()
]

# FIGURE GENERATOR
# GRAPH MAP
def figure_map():
    data_map = [
        # go.Scattermapbox(
        #     lat=metadata_files.Lintang,
        #     lon=metadata_files.Bujur,
        #     hoverinfo="none",
        #     marker=go.scattermapbox.Marker(size=12, color="black", opacity=1),
        # ),
        go.Scattermapbox(
            lat=metadata_files.Lintang,
            lon=metadata_files.Bujur,
            text=metadata_files["Nama Stasiun"].str.lower(),
            customdata=metadata_files.index,
            name="stasiun",
        ),
    ]
    layout_map = go.Layout(
        clickmode="event+select",
        title=dict(
            text="<b>🔎 Lokasi Stasiun BMKG</b>".lower(),
            pad=dict(t=-35),
            font=dict(size=30),
        ),
        margin=dict(t=80),
        mapbox=dict(
            center=dict(
                lat=metadata_files.Lintang.mean(),
                lon=metadata_files.Bujur.mean(),
            ),
        ),
        dragmode="pan",
    )
    return go.Figure(data_map, layout_map)


# FIGURE SCATTER PARAMETER
def figure_with_parameter(stations, parameter):
    data = []
    for stat_id in stations:
        with pd.HDFStore(FILE_BMKG, mode="r") as store:
            table = store.get(f"/stations/sta{stat_id}")
            clean_table(table)
        name = f'{stat_id} - {metadata_files.loc[stat_id, "Nama Stasiun"]}'.lower()
        emoji = label_parameter[parameter].split()[0]
        data.append(
            go.Scatter(
                x=table.index,
                y=table.loc[:, parameter],
                name=name,
                hovertemplate=f"{emoji}: %{{y}}",
            )
        )

    title = f"<b>📈 Grafik {label_parameter[parameter].split('(')[0]}</b>".lower()

    layout = go.Layout(
        hovermode="x",
        title=dict(
            text=title,
            pad=dict(t=-25),
        ),
        height=300,
        xaxis=dict(title="<b>📅 tanggal</b>"),
        yaxis=dict(title=f"<b>{label_parameter[parameter]}</b>"),
        margin=dict(t=65),
        dragmode="zoom",
        showlegend=True,
    )

    fig = go.Figure(data, layout)

    return fig


# FIGURE COMPLETENESS
def figure_completeness(stations, parameter):
    table_percent = []
    for stat_id in stations:
        with pd.HDFStore(FILE_COMPLETENESS, mode="r") as store:
            table = store.get(f"/stations/sta{stat_id}")
            table = table[[parameter]].round(3) * 100
            table.columns = [f"{stat_id}"]
            table_percent.append(table)

    table_percent = pd.concat(table_percent, axis=1).T.iloc[::-1]
    table_percent_date = table_percent.copy()
    table_percent_date[:] = table_percent_date.columns.strftime("%B %Y").str.lower()

    data = go.Heatmap(
        z=table_percent.to_numpy(),
        x=table_percent.columns,
        y=[
            f'{stat_id} - {metadata_files.at[int(stat_id), "Nama Stasiun"]}'.lower()
            for stat_id in table_percent.index
        ],
        zmin=0,
        zmax=100,
        customdata=table_percent_date.to_numpy(),
    )

    layout = go.Layout(
        title=dict(
            text=f"<b>💯 Kelengkapan Data {label_parameter[parameter].split('(')[0]}</b>".lower(),
            pad=dict(t=-25),
        ),
        height=300,
        xaxis=dict(title={"text": "<b>📅 tanggal</b>"}),
        yaxis=dict(
            title={"text": "<b>🆔 ID Stasiun</b>".lower()},
            tickmode="array",
            tickvals=[
                f'{stat_id} - {metadata_files.at[int(stat_id), "Nama Stasiun"]}'.lower()
                for stat_id in table_percent.index
            ],
            ticktext=table_percent.index,
            tickangle=-90,
        ),
        margin=dict(t=65),
        dragmode="zoom",
    )

    return go.Figure(data, layout)


# DASH APPLICATION
app = dash.Dash(
    APP_TITLE,
    title=APP_TITLE,
    update_title=APP_UPDATE_TITLE,
    external_stylesheets=[getattr(dbc.themes, BOOTSTRAP_THEME)],
)

app.layout = dbc.Container(
    [
        dbc.Container(
            [
                html.H1(
                    APP_TITLE,
                    className="text-center fw-bold fs-1 p-0",
                    style={"cursor": "pointer"},
                    id="tooltip-target",
                ),
                dbc.Tooltip(
                    "Open Source Edition (Offline)".lower(), target="tooltip-target"
                ),
                dcc.Markdown(
                    """
                created by [taruma](https://github.com/taruma) & powered by [hidrokit](https://github.com/hidrokit)
                """,
                    className="text-center fw-bolder fs-8",
                ),
                dcc.Markdown(pytemplate.MD_TUTORIAL.lower()),
            ],
        ),
        dcc.Graph(id="map-fig", figure=figure_map(), config=CONFIG_DCC_GRAPH),
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.P("🛖 stasiun", className="fs-2"),
                                dcc.Dropdown(
                                    options=options_stations,
                                    value=[96783],
                                    multi=True,
                                    clearable=False,
                                    id="stat-picker",
                                ),
                            ]
                        ),
                        html.Div(
                            [
                                html.P("🧮 parameter", className="fs-2"),
                                dcc.Dropdown(
                                    options=options_parameter,
                                    value="RR",
                                    multi=False,
                                    clearable=False,
                                    id="parameter-picker",
                                ),
                            ],
                            className="col-4",
                        ),
                    ],
                    className="mt-3",
                ),
                dbc.Row(
                    [
                        html.Div(className="col"),
                        html.Div(
                            dbc.Button(
                                "Tampilkan Grafik".lower(),
                                id="button-main",
                                color="primary",
                                className="float-end",
                            ),
                            className="col-4 mt-2",
                        ),
                    ],
                ),
            ],
        ),
        html.Hr(),
        dcc.Loading(
            [
                dcc.Graph(
                    id="graph-all",
                    figure=EMPTY_FIG,
                    config=CONFIG_DCC_GRAPH,
                )
            ]
        ),
        html.Hr(),
        dcc.Loading(
            dcc.Graph(
                id="graph-completeness",
                figure=EMPTY_FIG,
                config=CONFIG_DCC_GRAPH,
            )
        ),
        html.Hr(),
        dcc.Markdown(
            "made with [Dash+Plotly](https://plotly.com)".lower(),
            className="fs-4 text-center",
        ),
        html.Footer(
            [
                html.Span("\u00A9"),
                " 2022 ",
                html.A(
                    "Taruma Sakti Megariansyah".lower(),
                    href="https://github.com/taruma",
                ),
                ". MIT License. Visit this repository on ".lower(),
                html.A(
                    "Github".lower(),
                    href="https://github.com/taruma/dash-bmkg-data-explorer",
                ),
                ".",
            ],
            className="text-center",
        ),
    ],
    className="p-3",
)


@app.callback(
    [
        Output("stat-picker", "value"),
        Output("graph-all", "figure"),
        Output("graph-completeness", "figure"),
    ],
    [
        Input("button-main", "n_clicks"),
        Input("map-fig", "selectedData"),
        State("parameter-picker", "value"),
        Input("stat-picker", "value"),
    ],
    prevent_initial_call=True,
)
def create_graph(_, selectedData, parameter, dropdownval):
    ctx = dash.callback_context

    fig_par = EMPTY_FIG
    fig_com = EMPTY_FIG

    if selectedData is not None:
        stations = [point["customdata"] for point in selectedData["points"]]
        stations = stations[:SELECTED_MAX] if len(stations) > SELECTED_MAX else stations

    stations = dropdownval if selectedData is None else stations

    if ctx.triggered[0]["prop_id"] == "button-main.n_clicks":
        stations = stations[:SELECTED_MAX] if len(stations) > SELECTED_MAX else stations

        fig_par = figure_with_parameter(stations, parameter)
        fig_com = figure_completeness(stations, parameter)

    return [
        stations,
        fig_par,
        fig_com,
    ]


if __name__ == "__main__":
    app.run_server(debug=DEBUG)
