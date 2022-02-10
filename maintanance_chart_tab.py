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
                      "Техместа. Уровень 1",
                      dcc.Dropdown(id="checklist_level_1", multi=True),
                  ]),


                    html.P(),
                    html.Div([
                      "EO Основной Класс",
                      dcc.Dropdown(id="checklist_main_eo_class", multi=True),
                  ]),
                    
                    html.P(),
                    html.Div([
                      "EO Класс",
                      dcc.Dropdown(id="checklist_eo_class", multi=True),
                  ]),
                    
                    
                    
                    html.P(),
                    html.Div([
                      "Техместа. Уровень 2",
                      dcc.Dropdown(id="checklist_level_2", multi=True),
                  ]),

                  #html.P(),
                  #  html.Div([
                  #    "Уровень 3",
                  #    dcc.Dropdown(id="checklist_level_3", multi=True),
                  #]),

                  # html.P(),
                  #  html.Div([
                  #    "Уровень 4",
                  #    dcc.Dropdown(id="checklist_level_4", multi=True),
                  #]),

                  #html.P(),
                  #  html.Div([
                  #    "Уровень 5",
                  #    dcc.Dropdown(id="checklist_level_5", multi=True),
                  #]),

                  html.P(),
                    html.Div([
                      "Уровень Вышестоящее техместо",
                      dcc.Dropdown(id="checklist_level_upper", multi=True),
                  ]),
                  ]
                ),
                dbc.Col(width=9,
                    children=[
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