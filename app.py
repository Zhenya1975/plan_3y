import pandas as pd
# import numpy as np
from dash import Dash, dcc, html, Input, Output, callback_context, State
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO
from dash_bootstrap_templates import load_figure_template
import datetime
import functions


import maintanance_chart_tab
# import settings_tab

from dash import dash_table
import base64
import io
import json
import plotly.graph_objects as go

# select the Bootstrap stylesheet2 and figure template2 for the theme toggle here:
# template_theme1 = "sketchy"
template_theme1 = "flatly"
template_theme2 = "darkly"
# url_theme1 = dbc.themes.SKETCHY
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.DARKLY


loading_style = {
    # 'position': 'absolute',
                 # 'align-self': 'center'
                 }

templates = [
    "bootstrap",
    "minty",
    "pulse",
    "flatly",
    "quartz",
    "cyborg",
    "darkly",
    "vapor",
]

load_figure_template(templates)

dbc_css = (
    "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.1/dbc.min.css"
)
app = Dash(__name__, external_stylesheets=[url_theme1, dbc_css])

"""
===============================================================================
Layout
"""

tabs_styles = {
    'height': '44px'
}

app.layout = dbc.Container(
    dbc.Row(
        [
            dbc.Col(
                [
                    html.H4("КТГ 2023-2025"),
                    ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2], ),

                    html.Div([
                        dcc.Tabs(
                            id="tabs-all",
                            style={
                                'width': '50%',
                                # 'font-size': '200%',
                                'height':'5vh'
                            },
                            value='ktg',
                            # parent_className='custom-tabs',
                            # className='custom-tabs-container',
                            children=[
                                maintanance_chart_tab.maintanance_chart_tab(),
                                # messages_orders_tab.messages_orders_tab(),
                                # orders_moved_tab.orders_moved_tab(),
                                # settings_tab.settings_tab()

                                # tab2(),
                                # tab3(),
                            ]
                        ),
                    ]),

                ]
            )
        ]
    ),
    className="m-4 dbc",
    # fluid=True,
)


@app.callback([
    Output('planned_downtime', 'figure'),
],
    [
        Input('checklist_level_1', 'value'),
        # Input('checklist_eo_class', 'value'),
        # Input('checklist_main_eo_class', 'value'),
        # Input('checklist_level_upper', 'value'),
    ],
)
def maintanance(checklist_level_1):
  maintanance_jobs_df = pd.read_csv('data/maintanance_jobs_df.csv')
  downtime_y = maintanance_jobs_df['dowtime_plan, hours']
  dates_x = maintanance_jobs_df['maintanance_datetime']
  
  # fig = go.Figure([go.Bar(x=dates_x, y=downtime_y)])
  fig = go.Figure()
  fig.add_trace(go.Bar(
    name="Простои",
    x=dates_x, y=downtime_y,
    xperiod="M1",
    # xperiodalignment="middle",
    textposition='auto'
    ))
  fig.update_xaxes(showgrid=True, ticklabelmode="period")
  #fig.update_traces(textposition='auto')
  fig.update_layout(title_text='Запланированный простой по месяцам, час',)

  return [fig]

if __name__ == "__main__":
    # app.run_server(debug=True)
    app.run_server(host='0.0.0.0', debug=False)
