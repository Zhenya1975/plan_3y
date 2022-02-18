from dash import dcc, html
import dash_bootstrap_components as dbc
loading_style = {
    # 'position': 'absolute',
    # 'align-self': 'center'
                 }
def maintanance_chart_tab():
    maintanance_chart_tab_block = dcc.Tab(
        label='КТГ',
        value='ktg',
        children=[
           
          dcc.Loading(id='loading', parent_style=loading_style),
            
            
            dbc.Row([
                # колонка с фильтрами
                dbc.Col(width=3,
                  children=[
                    
                    html.P(),
                    html.Div([
                      "Бизнес единица",
                      dcc.Dropdown(id="checklist_level_1", multi=True),
                  ]),


                    html.P(),
                    html.Div([
                      "Техместо вышестоящее",
                      dcc.Dropdown(id="checklist_main_eo_class", multi=True),
                  ]),
                    
                  
                  html.P(),
                    html.Div([
                      "ЕО",
                      dcc.Dropdown(id="checklist_eo", multi=True),
                  ]),
                    html.Hr(),
                    html.P('Категории работ'),
                    html.Div(style={'marginLeft': '3px'},
                                     children=[
                                         dbc.Button("Выбрать все", size="sm",
                                                    id="select_all_maintanance_category_checklist",
                                                    style={'marginBottom': '3px',
                                                           'marginTop': '3px',
                                                           'backgroundColor': '#232632'}
                                                    ),
                                         dbc.Button("Снять выбор", color="secondary",
                                                    size="sm",
                                                    style={'marginBottom': '3px',
                                                           'marginTop': '3px',
                                                           'backgroundColor': '#232632'},
                                                    id="release_all_maintanance_category_checklist"),

                                         html.P(),
                                         dcc.Checklist(
                                             id='maintanance_category_checklist',
                                             # options=regions,
                                             # value=regions_list,
                                             labelStyle=dict(display='block')),
                                         html.Hr(className="hr"),
                                     ]
                               ),
                  ]
                ),
                dbc.Col(width=9,
                    children=[
                            dbc.Row([
                              dbc.Col(
                                children = [
                                  html.H5(id = 'be_title_id'),
                                  # html.P(),
                                  html.H5(id = 'level_upper_title_id'),
                                  html.H5(id = 'number_of_eo_title_id')

                                ]
                                
                          )
                        ]),
                        dbc.Row([
                              dbc.Col(width = 4,
                                children = [
                                  dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.H4("2023 год", className="card-title"),
                                            #html.H6("Card subtitle", className="card-subtitle"),
                                            html.P(id = 'downtime_2023'),
                                            html.P(id = 'cal_fond_2023'),

                                           
                                        ]
                                    ),
                                    style={"width": "18rem"},

                                  )

                                ],
                 
                              ),
                              dbc.Col(width = 4,
                              
                              ),
                              dbc.Col(width = 4,
                              
                              )
                        ]),
                      html.Hr(),
                      ###################### ряд с кнопками выгрузки таблиц в эксель ####################
                      html.Div(
                        dbc.Row([
                      
                          dbc.Col(width=2,
                                  children=[
                                    html.Div([
                                      dbc.Button("Выгрузить простои xlsx", id="btn_download_downtime_table", size="sm",
                                                 style={'marginBottom': '3px',
                                                        'marginTop': '3px',
                                                        'backgroundColor': '#232632'},),
                                      dcc.Download(id="download_excel_downtime_table")
                                    ])
                                  ]
                                 )
                        ])
                      ),

                      #######################################################
                      html.Div(
                        dbc.Row([
                      
                          dbc.Col(width=7,
                            children=[
                              html.P(),
                              dcc.Graph(id='planned_downtime', config={'displayModeBar': False}),
                            ]),
                         dbc.Col(width=5,
                            children=[
                              html.P(),
                              dcc.Graph(id='planned_downtime_piechart', config={'displayModeBar': False}),
                            ])
                       ]),
                      # style={"background-color": "#ABBAEA"},
                      ), 
                      #############################################################
                      html.Div(
                        dbc.Row([
                      
                          dbc.Col(width=7,
                            children=[
                              html.P(),
                              dcc.Graph(id='fig_ktg_3y_by_months_id', config={'displayModeBar': False}),
                            ]),
                         
                       ]),
                      # style={"background-color": "#ABBAEA"},
                      ), 



                      #############################################################
                       
                       html.Hr(),
                       html.P(),
                       dcc.Graph(id='ktg_by_years', config={'displayModeBar': False}),
                       html.Hr(),
                       html.Div(
                        dbc.Row([
                      
                          dbc.Col(width=12,
                            children=[
                              html.Div([
                                html.P(),
                                
                                html.P(),
                                dbc.Button("Выгрузить ктг.xlsx", id="btn_download_ktg_table", size="sm",
                                           style={'marginBottom': '3px',
                                                  'marginTop': '3px',
                                                  'backgroundColor': '#232632'}, ),
                                dcc.Download(id="download_ktg_table")
                        ]),
                              
                            ]),
                         
                       ]),
                      # style={"background-color": "#ABBAEA"},
                      ),
                       html.Div(id='ktg_by_month_table'), 




                      
                      # html.P(),
                       # dcc.Graph(id='ktg_by_month', config={'displayModeBar': False}),
                       # html.Hr(),
                       # html.P(),
                       # dcc.Graph(id='ktg_by_weeks', config={'displayModeBar': False}),
                    ]),
                
            ]),
            #dbc.Row([
                
            #]),
        
       
          ]
    )
    return maintanance_chart_tab_block