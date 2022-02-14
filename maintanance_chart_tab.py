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
                       html.P(),
                       dcc.Graph(id='planned_downtime', config={'displayModeBar': False}),
                       html.Hr(),
                       html.P(),
                       dcc.Graph(id='ktg_by_years', config={'displayModeBar': False}),
                       html.Hr(),
                       html.P(),
                       dcc.Graph(id='ktg_by_month', config={'displayModeBar': False}),
                       html.Hr(),
                       html.P(),
                       dcc.Graph(id='ktg_by_weeks', config={'displayModeBar': False}),
                    ]),
                
            ]),
            #dbc.Row([
                
            #]),
        
        ]
    )
    return maintanance_chart_tab_block