import pandas as pd
# import numpy as np
from dash import Dash, dcc, html, Input, Output, callback_context, State
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO
from dash_bootstrap_templates import load_figure_template
import datetime
import functions


import maintanance_chart_tab
import settings_tab

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
                                # 'width': '50%',
                                # 'font-size': '200%',
                                'height':'10vh'
                            },
                            value='ktg',
                            # parent_className='custom-tabs',
                            # className='custom-tabs-container',
                            children=[
                                maintanance_chart_tab.maintanance_chart_tab(),
                                # messages_orders_tab.messages_orders_tab(),
                                # orders_moved_tab.orders_moved_tab(),
                                settings_tab.settings_tab()

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
        Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
        # Input('checklist_eo_class', 'value'),
        # Input('checklist_main_eo_class', 'value'),
        # Input('checklist_level_upper', 'value'),
    ],
)
def maintanance(checklist_level_1, theme_selector):
  maintanance_jobs_df = pd.read_csv('data/maintanance_jobs_df.csv')
  downtime_y = maintanance_jobs_df['dowtime_plan, hours']
  dates_x = maintanance_jobs_df['maintanance_datetime']
  if theme_selector:
      graph_template = 'bootstrap'
  else:
      graph_template = 'plotly_dark'

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
  fig.update_layout(
    title_text='Запланированный простой по месяцам, час',
    template=graph_template,
    )

  return [fig]


########## Настройки################
@app.callback(
    Output("download_template", "data"),
    Input("btn_download_template", "n_clicks"),
    prevent_initial_call=True,
)
def func_1(n_clicks):
    if n_clicks:
        df = pd.read_csv('data/selected_items.csv', dtype=str)
        df = df.astype({'level_no': int})
        return dcc.send_data_frame(df.to_excel, "шаблон фильтров.xlsx", index=False, sheet_name="шаблон фильтров")


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xlsx' in filename and "maintanance_job_list_general" in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
            df.to_csv('data/maintanance_job_list_general.csv')
        
            
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),


        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            filter_action='native',
            style_header={
                # 'backgroundColor': 'white',
                'fontWeight': 'bold'
            },
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
            },
            style_cell={'textAlign': 'left'},

        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        # html.Div('Raw Content'),
        # html.Pre(contents[0:200] + '...', style={
        #     'whiteSpace': 'pre-wrap',
        #     'wordBreak': 'break-all'
        # })
    ])

@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              )
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n) for c, n in zip(list_of_contents, list_of_names)]
        
        return children





if __name__ == "__main__":
    # app.run_server(debug=True)
    app.run_server(host='0.0.0.0', debug=False)
