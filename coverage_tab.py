from dash import dcc, html
import dash_bootstrap_components as dbc
# import datetime
# import json
# Opening JSON file



def coverage_tab():
    settings_tab_block = dcc.Tab(
        label='Покрытие',
        value='coverage_tab',
        children=[
            dbc.Row([
                dbc.Col(width = 2, 
                    children=[
                       
                    ]),
              dbc.Col(width = 10,
                    children=[
                      ############################## РЯД С КАРТОЧКАМИ ###########################
                      html.P(), 
                      dbc.Row([
                        dbc.Col(width = 3,
                            children=[
                              dbc.Card(
                                dbc.CardBody(
                                  [
                                    html.H4("Модели ЕО в 3-Y плане", className="card-title"),
                                    #html.H6("Card subtitle", className="card-subtitle"),
                                    html.P(id = 'total_number_of_models_for_3y_plan'),
                                    html.P(id = 'number_of_eo_models_with_strategy'),
                                    # html.P(id = 'cal_fond_2023'),
                                  ]
                                ),
                                # style={"width": "18rem"},
                              ),
                              dcc.Graph(id='eo_models_in_plan_pie_chart', config={'displayModeBar': False}),
                            ]),
                        dbc.Col(width = 3,
                            children=[
                              dbc.Card(
                                dbc.CardBody(
                                  [
                                    html.H4("ЕО в 3-Y плане", className="card-title"),
                                    #html.H6("Card subtitle", className="card-subtitle"),
                                    html.P(id = 'total_number_of_eo_for_3y_plan'),
                                    html.P(),
                                    html.P(),
                                    html.P(id = 'number_of_eo_with_strategy'),
                                    # html.P(id = 'cal_fond_2023'),
                                  ]
                                ),
                                # style={"width": "18rem"},
                              ),
                              dcc.Graph(id='eo_in_plan_pie_chart', config={'displayModeBar': False}),
                            ]),
                       ]),

                      ##########################################################################
                      
                    ])
                ])

        ])
    return settings_tab_block