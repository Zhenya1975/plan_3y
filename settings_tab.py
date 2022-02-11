from dash import dcc, html
import dash_bootstrap_components as dbc
# import datetime
# import json
# Opening JSON file



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

                        html.Div([
                            html.P(),
                            
                            html.P(),
                            dbc.Button("Выгрузить eo_job_catologue.xlsx", id="btn_download_eo_job_catologue", size="sm",
                                       style={'marginBottom': '3px',
                                              'marginTop': '3px',
                                              'backgroundColor': '#232632'}, ),
                            dcc.Download(id="download_eo_job_catologue")
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

                            # html.P("В файле 'eo_maintanance_plan_update_start_date' вместо пустых ячеек в поле 'последняя проведенная форма' подставляем дату по умолчанию"),
                            
                            
                            #dcc.DatePickerSingle(
                            #  id='default_maintanance_start_date_picker',
                            #  display_format='DD.MM.YYYY',
                              # min_date_allowed=date(1995, 8, 5),
                              # max_date_allowed=date(2017, 9, 19),
                            #  first_day_of_week=1,
                              # initial_visible_month= datetime.date(2022, 12, 31),
                              # date= default_to_start_date
                          #),
                            html.Div(id='output-container-date-picker-single'),
                            html.P(),

                            
                            html.A(dbc.Button("Reload", id="reload", size="sm",
                                       style={'marginBottom': '3px',
                                              'marginTop': '3px',
                                              'backgroundColor': '#232632'}, ),href='/'),
                            html.Hr(),                  
                            html.Div(id='output-data-upload'),
                        ]),


                    ])
                ])

        ])
    return settings_tab_block