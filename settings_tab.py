from dash import dcc, html
import dash_bootstrap_components as dbc
import datetime

def settings_tab():
    settings_tab_block = dcc.Tab(
        label='Настройки',
        value='tab_settings',
        children=[
            dbc.Row([
                dbc.Col(
                    children=[

                        
                        html.Div([
                            html.P(),
                            
                            html.P(),
                            dbc.Button("Выгрузить maintanance_job_list_general.xlsx", id="btn_download_maintanance_job_list_general", size="sm",
                                       style={'marginBottom': '3px',
                                              'marginTop': '3px',
                                              'backgroundColor': '#232632'}, ),
                            dcc.Download(id="download_maintanance_job_list_general")
                        ]),

                        html.P(),
                        

                        html.Div([
                            dcc.Upload(
                                id='upload-data',
                                children=html.Div([
                                    'Перетащи или ',
                                    html.A('выбери файл')
                                ]),
                                style={
                                    'width': '100%',
                                    'height': '60px',
                                    'lineHeight': '60px',
                                    'borderWidth': '1px',
                                    'borderStyle': 'dashed',
                                    'borderRadius': '5px',
                                    'textAlign': 'center',
                                    'margin': '10px'
                                },
                                # Allow multiple files to be uploaded
                                multiple=True
                            ),
                            html.Div(id='output-data-upload'),
                        ]),


                    ])
                ])

        ])
    return settings_tab_block