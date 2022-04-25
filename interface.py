# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
#test
import dash
from dash import dcc
from dash import html
import plotly.express as px
import plotly
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output, State
from scripts.script1 import getData, getStatus
from scripts.script1 import getMonitors

import numpy
import json

json_file = getMonitors()

# external JavaScript files
external_scripts = [
    {
        'src': 'https://code.jquery.com/jquery-3.3.1.slim.min.js',
        'integrity': 'sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo',
        'crossorigin': 'anonymous'
    },
    {
        'src': 'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js',
        'integrity': 'sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1',
        'crossorigin': 'anonymous'
    },
    {
        'src': 'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js',
        'integrity': 'sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM',
        'crossorigin': 'anonymous'
    }
]

# external CSS stylesheets
external_stylesheets = [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T',
        'crossorigin': 'anonymous'
    },
    {
        'href': './assets/style.css',
        'rel': 'stylesheet'
    }
]
#data = getData(getMonitors()["monitorme1"])
data = [0,0,[["-","-"]],"-","-",0,0]
app = dash.Dash(__name__,
                external_scripts=external_scripts,
                external_stylesheets=external_stylesheets
)

app.enable_dev_tools(
    dev_tools_ui=False,
    dev_tools_serve_dev_bundles=False,
    )

app.title = "Monitor Manager"
# Dash CSS
app.css.config.serve_locally = False

# Loading screen CSS
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/brPBPO.css"})

XH = list()

YH = list()
hdd = list()
hdd = dict(
            data=[
                dict(
                    x=[],
                    y=[],
                    name='% of Disk use',
                    marker=dict(
                        color='rgb(55, 83, 109)'
                    )
                )
            ],
            layout=dict(
                title='Disk(%)',
                showlegend=True,
                legend=dict(
                    x=0,
                    y=1.0
                ),
                margin=dict(l=40, r=0, t=40, b=30)
            )
        )
X = list()

Y = list()
cpu = list()
cpu = dict(
            data=[
                dict(
                    x=[],
                    y=[],
                    name='% of CPU use',
                    marker=dict(
                        color='rgb(26, 118, 255)'
                    )
                )
            ],
            layout=dict(
                title='CPU(%)',
                showlegend=True,
                legend=dict(
                    x=0,
                    y=1.0
                ),
                margin=dict(l=40, r=0, t=40, b=30)
            )
        )
data_c = list()
data_h = list()

app.layout = html.Div(className="main-container", children=[
    html.Nav(className="navbar sticky-top navbar-light bg-light", children=[
    html.Div(className='navbar-brand', id="navb",children=[
        html.H1(className="h1-logo",
            children=[html.Img(className="logo",src='https://www.freeiconspng.com/thumbs/dashboard-icon/dashboard-icon-3.png'),'Dashboard']
        ),
        dcc.Dropdown(
            id='monitor-dropdown',
            options=[
                 {'label':monitor, 'value': monitor} for monitor in json_file
            ],
            value='Overview',
            clearable=False,
            searchable=False
        ),
        ])
    ]),
    html.Div(className="container content", id="monitor-overview", children=[
        html.H3(style={"textAlign": "center"}, children="Overview"),
        html.Div(className="row card" , children=[
            html.H4(className="card-header", children=("My monitors")),
            html.Div(className="card-body",children=(
                            html.Div(className="number-row",id="monitor-content")
            ))]
        )
    ]),
    html.Div(className="container content",id="monitor-view", children=[
        dcc.Loading(
            id="loading-1",
            type="default",
            fullscreen=True
        ),
        html.H3(id="name", children="Monitor : monitorme1"),
        #ONE ROW
        html.Div(className="row card" , children=[
            html.H4(className="card-header", children=("Données")),
            html.Div(className="card-body", children=(
                html.Div(className="number-row", children=[
                html.Div(className="col-sm number-data", style={'color': 'red'}, children=[
                    html.Span(className="number-field", id="live_error", children=(data[3])),
                    html.Span(className="number-type", children="Erreurs")
                ]),
                html.Div(className="col-sm number-data", style={'color': 'green'}, children=[
                    html.Span(className="number-field", id="live_ip",children=(data[4])),
                    html.Span(className="number-type", children="Adresses IP uniques")
                ]),
                html.Div(className="col-sm number-data", style={'color': 'black'}, children=[
                    html.Span(className="number-field", id="live_delay", children=(round(data[5],0))),
                    html.Span(className="number-type", children="Délai de réponse (en us)")
                ])
                ])
                )
            )]
        ),
        #ONE ROW
        html.Div(className="row card" , children=[
            html.H4(className="card-header", children=("Performance")),
            html.Div(className="card-body", children=(
                html.Div(className="number-row", children=[
                html.Div(className="col-sm number-data", style={'color': 'red'}, children=(
                    html.Div([
                        dcc.Graph(
                            figure = cpu,
                            style={'height': 400},
                            id='cpu',
                            animate=True
                        )
                    ])
                )),
                html.Div(className="col-sm number-data", style={'color': 'black'}, children=(
                    html.Div([
                        dcc.Graph(
                            figure = hdd,
                            style={'height': 400},
                            id='hdd',
                            animate=True
                        )
                    ])
                ))
                ])
                )
            )]
        ),
        #ONE ROW
        html.Div(className="row card" , children=[
            html.H4(className="card-header", children=("Pages visitées")),
            html.Div(className="card-body", children=(
                html.Div(className="number-row", children=(
                    html.Table(className="table", style={"textAlign": "center"},children=[
                        html.Thead(children=(
                            html.Tr(children=[
                                html.Th(children=("Page")),
                                html.Th(children=("Nombre de visites"))
                            ])
                        )),
                        html.Tbody(id="tbody")
                    ])
                ))
                )
            )]
        ),
    ]),
    html.Footer(className="bg-light text-center text-lg-start", children=(
        html.Div(className="text-center p-3", children=("Monitor Manager - Développé par le groupe 8"))
    )),
    dcc.Interval(
        id='interval-component',
        interval=30*1000, # in milliseconds
        n_intervals=0
    )
])
last_monitor = "monitorme1"
@app.callback(
    Output('monitor-view', 'style'),
    Output('monitor-overview', 'style'),
    Output('monitor-content', 'children'),
    Input('monitor-dropdown', 'value'))
def callback_view(monitor):
    monitor_list = []
    if monitor == "Overview":
        for monitor in json_file:
            if monitor != "Overview":
                status = getStatus(monitor)
                if status[0] == "Offline":
                    status_img = html.Span(className="dot offline")
                else :
                    status_img = html.Span(className="dot online")

                item = html.Div(className="col-sm number-data", children=[
                        html.Span(className="number-field monitor-name", children=(monitor)),
                        html.Span(className="number-type status-row", children=[status_img,status[0]])
                    ])
                monitor_list.append(item)

        return {'display' : 'none'},{'display' : 'block'}, monitor_list
    else:
        return {'display' : 'block'},{'display' : 'none'}, monitor_list
@app.callback(
    Output('live_error', 'children'),
    Output('live_ip', 'children'),
    Output('live_delay', 'children'),
    Output('cpu', 'figure'),
    Output('hdd', 'figure'),
    Output('tbody', 'children'),
    Output('name', 'children'),
    Input('interval-component', 'n_intervals'),
    Input('monitor-dropdown', 'value'))
def callback(n,monitor):
    global last_monitor,X,Y,XH,YH,data_c,data_h
    if monitor == "Overview":
        monitor_info = "monitorme1"
    else:
        monitor_info = monitor

    if last_monitor != monitor_info:
        X =[0]
        Y=[]
        XH=[0]
        YH=[]
        last_monitor=monitor_info
    data = getData(monitor_info)
    data_table = []
    for item in data[2]:
        t_item = html.Tr(children=[
            html.Td(children=(item[0])),
            html.Td(children=(item[1]))

        ])
        data_table.append(t_item)

    X.append(len(X))
    Y.append(data[0])
    data_c = plotly.graph_objs.Scatter(
        x=list(X),
        y=list(Y),
        name="* of CPU use",
        mode='lines+markers'
    )
    XH.append(len(XH))
    YH.append(data[1])
    data_h = plotly.graph_objs.Scatter(
        x=list(XH),
        y=list(YH),
        name="% of Disk use",
        mode='lines+markers'
    )
    data_cpu = {'data': [data_c],
                'layout':go.Layout(xaxis=dict(range=[0,max(X)]),yaxis=dict(range=[0,numpy.amax(numpy.array(Y).astype(float))+10]))}
    data_hdd = {'data': [data_h],
                'layout':go.Layout(xaxis=dict(range=[0,max(XH)]),yaxis=dict(range=[0,numpy.amax(numpy.array(YH).astype(float))+10]))}
    name = "Monitor : " + monitor_info

    return data[3], data[4],round(data[5],0), data_cpu, data_hdd,data_table,name

if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0", port=8050)
