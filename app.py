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
import initial_values

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

first_day_of_selection = initial_values.first_day_of_selection
last_day_of_selection = initial_values.last_day_of_selection


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
    "sandstone"
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
                    ThemeSwitchAIO(
                      aio_id="theme", themes=[url_theme1, url_theme2],
                    ),

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


######################### ОСНОВНОЙ ОБРАБОТЧИК ДЛЯ ПОСТРОЕНИЯ ГРАФИКОВ ##############################
@app.callback([
    Output("checklist_eo", "value"),
    Output("checklist_eo", "options"),
    Output('be_title_id', 'children'),
    Output('planned_downtime', 'figure'),
    Output('ktg_by_years', 'figure'),
    Output('ktg_by_month', 'figure'),
    Output('ktg_by_weeks', 'figure'),
    Output('loading', 'parent_style'),
],
    [
        Input('checklist_level_1', 'value'),
        Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
        Input('checklist_eo', 'value'),
        # Input('checklist_eo_class', 'value'),
        # Input('checklist_main_eo_class', 'value'),
        # Input('checklist_level_upper', 'value'),
    ],
)
def maintanance(checklist_level_1, theme_selector, checklist_eo):
  # читаем список работ с простоями
  maintanance_jobs_full_df = pd.read_csv('data/maintanance_jobs_df.csv', dtype = str)
  maintanance_jobs_full_df = maintanance_jobs_full_df.astype({'dowtime_plan, hours': float, 'eo_code': str})
  # поле даты - в datetime
  maintanance_jobs_full_df['maintanance_datetime']= pd.to_datetime(maintanance_jobs_full_df['maintanance_datetime'])
  # режем выборку с начала периода отчета
  maintanance_jobs_full_df = maintanance_jobs_full_df.loc[maintanance_jobs_full_df['maintanance_datetime'] >= first_day_of_selection]
  
  # Список работ до фильтрации в фильтрах. Из этого списка берем options_list в фильтре по EO
  maintanance_jobs_df = maintanance_jobs_full_df
  ################### Фильтруем выборку фильтрами #############################
  eo_full_list = maintanance_jobs_full_df['eo_code'].unique()

  if checklist_eo == None:
    eo_filter_list = eo_full_list
  elif checklist_eo == []:
    eo_filter_list = eo_full_list
  else:
    eo_filter_list = checklist_eo
  


  # print('checklist_eo', checklist_eo)
  # print('eo_filter_list', eo_filter_list)
  # print('eo_full_list', eo_full_list)
  
  maintanance_jobs_df = maintanance_jobs_df.loc[maintanance_jobs_df['eo_code'].isin(eo_filter_list)]
  # print('длина maintanance_jobs_df', len(maintanance_jobs_df))
  
  # читаем календарный фонд
  eo_calendar_fond = pd.read_csv('data/eo_calendar_fond.csv', dtype = str)
  eo_calendar_fond = eo_calendar_fond.astype({'calendar_fond': float})
  # поле даты - в datetime
  eo_calendar_fond['datetime'] = pd.to_datetime(eo_calendar_fond['datetime'])
  # full_eo_list = pd.read_csv('data/full_eo_list.csv', dtype = str)
  
  # список ЕО, на которые есть календарный фонд
  eo_cal_fond = pd.DataFrame(eo_calendar_fond['eo_code'].unique(), columns = ['eo_code'], dtype = str)
  # список ЕО, на которые есть расчет простоев
  eo_downtime = pd.DataFrame(maintanance_jobs_df['eo_code'].unique(), columns = ['eo_code'], dtype = str)
  # делаем пересечение этих списков.
  eo_for_ktg = pd.merge(eo_cal_fond, eo_downtime, on = 'eo_code', how = 'inner')['eo_code'].unique()
  # print('eo_for_ktg', eo_for_ktg)
  # режем датафрейм с простоями по eo_for_ktg
  maintanance_jobs_df = maintanance_jobs_df.copy()
  
  maintanance_jobs_df = maintanance_jobs_df.loc[maintanance_jobs_df['eo_code'].isin(eo_for_ktg)]
  
  
  # режем датафрейм с календарным фондом  по eo_for_ktg
  maintanance_jobs_df = maintanance_jobs_df.copy()
  maintanance_jobs_df = maintanance_jobs_df.loc[maintanance_jobs_df['eo_code'].isin(eo_for_ktg)]

  ################# График простоев по месяцам ###############################
  downtime_y = maintanance_jobs_df['dowtime_plan, hours']
  dates_x = maintanance_jobs_df['maintanance_datetime']
  if theme_selector:
      graph_template = 'sandstone'
  # bootstrap

  else:
      graph_template = 'plotly_dark'

  # fig = go.Figure([go.Bar(x=dates_x, y=downtime_y)])
  fig_downtime = go.Figure()
  fig_downtime.add_trace(go.Bar(
    name="Простои",
    x=dates_x, y=downtime_y,
    xperiod="M1",
    # xperiodalignment="middle",
    textposition='auto'
    ))
  new_year_2022_2023 = pd.to_datetime('01.01.2024', format='%d.%m.%Y')
  new_year_2023_2024 = pd.to_datetime('01.01.2025', format='%d.%m.%Y')
  fig_downtime.add_vline(x=new_year_2022_2023, line_width=3, line_color="green")
  fig_downtime.add_vline(x=new_year_2023_2024, line_width=3, line_color="green")

  fig_downtime.update_xaxes(showgrid=True, ticklabelmode="period")
  #fig.update_traces(textposition='auto')
  fig_downtime.update_layout(
    title_text='Запланированный простой по месяцам за 3 года, час',
    template=graph_template,
    )

  ################# График КТГ по годам ###############################
  maintanance_jobs_df.to_csv('data/maintanance_jobs_df_delete.csv')
  maintanance_jobs_df['year'] = maintanance_jobs_df['maintanance_datetime'].dt.year
  eo_calendar_fond['year'] = eo_calendar_fond['datetime'].dt.year
  # maintanance_jobs_df['year'].astype('str')
  # x_years = ['2023', '2024', '2025']
  x_years = [2023, 2024, 2025]
  y_ktg = []
  text_list = []
  for year in x_years:
    downtime_year_df = maintanance_jobs_df.loc[maintanance_jobs_df['year']==year]
    downtime_year = downtime_year_df['dowtime_plan, hours'].sum()
    calendar_fond_year_df = eo_calendar_fond.loc[eo_calendar_fond['year'] == year]
    calendar_fond = calendar_fond_year_df['calendar_fond'].sum()
    ktg_year = (calendar_fond - downtime_year) / calendar_fond
    text = round(ktg_year, 2)
    text_list.append(text)
    y_ktg.append(ktg_year)
  
  fig_ktg_by_years = go.Figure()
  fig_ktg_by_years.add_trace(go.Bar(
    name="КТГ по годам за три года 2023-2025",
    x=x_years, 
    y=y_ktg,
    # xperiodalignment="middle",
    textposition='auto'
    ))
  fig_ktg_by_years.update_xaxes(type='category')
  fig_ktg_by_years.update_yaxes(range = [0.5,1])  
  fig_ktg_by_years.update_layout(
    
    title_text='КТГ по годам за три года 2023-2025',
    template=graph_template,
    )
  fig_ktg_by_years.update_traces(
    text = text_list,
    textposition='auto'
  )


  ################# График КТГ по месяцам ###############################
  maintanance_jobs_df['month'] = maintanance_jobs_df['maintanance_datetime'].dt.month
  maintanance_jobs_df['month_year'] = maintanance_jobs_df['month'].astype('str') + "_"+ maintanance_jobs_df['year'].astype('str')
  eo_calendar_fond['month'] = eo_calendar_fond['datetime'].dt.month
  eo_calendar_fond['month_year'] = eo_calendar_fond['month'].astype('str')  + "_" + eo_calendar_fond['year'].astype('str')

  x_month_year = ['1_2023','2_2023','3_2023','4_2023','5_2023','6_2023','7_2023','8_2023','9_2023','10_2023','11_2023','12_2023','1_2024','2_2024','3_2024','4_2024','5_2024','6_2024','7_2024','8_2024','9_2024','10_2024','11_2024','12_2024','1_2025','2_2025','3_2025','4_2025','5_2025','6_2025','7_2025','8_2025','9_2025','10_2025','11_2025','12_2025']
  y_ktg_month_year = []
  text_list_month_year = []
  for month_year in x_month_year:
    downtime_month_year_df = maintanance_jobs_df.loc[maintanance_jobs_df['month_year']== month_year]
   
    downtime_month_year = downtime_month_year_df['dowtime_plan, hours'].sum()
    
    calendar_fond_month_year_df = eo_calendar_fond.loc[eo_calendar_fond['month_year'] == month_year]
    calendar_fond_month_year = calendar_fond_month_year_df['calendar_fond'].sum()

    ktg_month_year = (calendar_fond_month_year - downtime_month_year) / calendar_fond_month_year

    text = round(ktg_month_year, 2)
    text_list_month_year.append(text)
    y_ktg_month_year.append(ktg_month_year)
    
  fig_ktg_by_month = go.Figure()
  fig_ktg_by_month.add_trace(go.Bar(
  name="КТГ",
  x=x_month_year, 
  y=y_ktg_month_year,
  # xperiodalignment="middle",
  textposition='auto'
  ))
  fig_ktg_by_month.update_xaxes(type='category')
  fig_ktg_by_month.update_yaxes(range = [0,1])  
  fig_ktg_by_month.update_layout(
    title_text='КТГ по месяцам за три года 2023-2025',
    template=graph_template,
    )
  fig_ktg_by_month.update_traces(
    text = text_list_month_year,
    textposition='auto'
  )


  ################# График КТГ по неделям 2023 ###############################
  maintanance_jobs_df_2023 = maintanance_jobs_df.loc[maintanance_jobs_df['year']==2023]
  maintanance_jobs_df_2023 = maintanance_jobs_df_2023.copy()
  maintanance_jobs_df_2023['week'] = maintanance_jobs_df_2023['maintanance_datetime'].dt.isocalendar().week
  
  eo_calendar_fond = eo_calendar_fond.copy()
  eo_calendar_fond['week'] = eo_calendar_fond['datetime'].dt.isocalendar().week
  eo_calendar_fond_2023 = eo_calendar_fond.loc[eo_calendar_fond['year']==2023]


  x_week = []
  for i in range(1,53):
    x_week.append(i)
  
  y_ktg_2023_week = []
  text_ktg_2023_week = []
  for week in x_week:
    downtime_2023_week_df = maintanance_jobs_df_2023.loc[maintanance_jobs_df_2023['week']== week]
    
    downtime_2023_week = downtime_2023_week_df['dowtime_plan, hours'].sum()
    eo_calendar_fond_week_df = eo_calendar_fond_2023.loc[eo_calendar_fond_2023['week'] == week]
    eo_calendar_fond_week = eo_calendar_fond_week_df['calendar_fond'].sum()

    ktg_week = (eo_calendar_fond_week - downtime_2023_week) / eo_calendar_fond_week

    text = round(ktg_week, 2)
    text_ktg_2023_week.append(text)
    y_ktg_2023_week.append(ktg_week)
    
  fig_ktg_by_weeks = go.Figure()
  fig_ktg_by_weeks.add_trace(go.Bar(
  name="КТГ по неделям 2023",
  x=x_week, 
  y=y_ktg_2023_week,
  # xperiodalignment="middle",
  textposition='auto'
  ))
  fig_ktg_by_weeks.update_xaxes(type='category')
  fig_ktg_by_weeks.update_yaxes(range = [0,1])  
  fig_ktg_by_weeks.update_layout(
    title_text='КТГ по неделям 2023',
    template=graph_template,
    )
  fig_ktg_by_weeks.update_traces(
    text = text_ktg_2023_week,
    textposition='auto'
  )

  ###################### данные для селектов фильтров по машинами ################
  # фильтр по машинам - пока это просто список maintanance_jobs_df 
  eo_list_value  = []
  if checklist_eo != None:
    eo_list_value = checklist_eo
  eo_list_options = functions.eo_checklist_data(maintanance_jobs_full_df)[0]

  ######################## титульный текст из КАКИХ БЕ машины в выборке #######################
  eo_list_with_filters_df = pd.DataFrame(maintanance_jobs_df['eo_code'].unique(), columns = ['eo_code'], dtype = str)
  
  # джойним со списком машин
  full_eo_list = pd.read_csv('data/full_eo_list.csv', dtype = str)
  eo_list_with_filters_data_df = pd.merge(eo_list_with_filters_df, full_eo_list, on='eo_code', how='left')
  # джойним с текстом наименований бизнес-единиц
  level_1 = pd.read_csv('data/level_1.csv', dtype = str)
  eo_list_with_filters_data_level_1_df = pd.merge(eo_list_with_filters_data_df, level_1, on = 'level_1', how = 'left')
  # print(eo_list_with_filters_data_level_1_df)
  # список бизнес единиц:
  be_list = eo_list_with_filters_data_level_1_df['level_1_description'].unique()
  # print(be_list)
  text_be= ''
  for word in be_list:
    text_be = text_be + word + ' '

  be_title = 'БЕ: {}'.format(text_be)
 
  new_loading_style = loading_style

  return eo_list_value, eo_list_options, be_title, fig_downtime, fig_ktg_by_years, fig_ktg_by_month, fig_ktg_by_weeks, new_loading_style


########## Настройки################
## обновляем дефолтную дату начала работ
# читаем файл с дефолтными значениями
# Opening JSON file
with open('default_values.json', 'r') as openfile:
  # Reading from json file
  default_values_dict = json.load(openfile)

default_to_start_date = default_values_dict['default_to_start_date']
#print(type(default_to_start_date))
default_to_start_date = datetime.datetime.strptime(default_to_start_date, '%Y-%m-%d')

@app.callback([
    Output('output-container-date-picker-single', 'children'),
    Output('default_maintanance_start_date_picker', 'date')
    ],
    Input('default_maintanance_start_date_picker', 'date'))
def update_output(date_value):
    
    string_prefix = 'Выбрана дата: '
    datapicker_value = default_to_start_date.date()
    text = ""
    if date_value is not None:
      default_values_dict['default_to_start_date'] = date_value
      
      # записываем в json
      with open("default_values.json", "w") as jsonFile:
        json.dump(default_values_dict, jsonFile)
      date_object = datetime.date.fromisoformat(date_value)
      date_string = date_object.strftime('%d.%m.%Y')
      text = string_prefix + date_string
      datapicker_value = date_value
    
    return text, datapicker_value 





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
    print('filename: ', filename)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xlsx' in filename and "maintanance_job_list_general" in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded),decimal=',')
            maintanance_job_list_general_df = functions.check_maintanance_job_list_general_file(df)
            functions.eo_job_catologue()
            maintanance_job_list_general_df.to_csv('data/maintanance_job_list_general.csv')
            # если мы загрузили список с работами, то надо подготовить данные для того чтобы вставить
            # даты начала расчета для ТО-шек
            # functions.maintanance_eo_list_start_date_df_prepare()

        elif 'xlsx' in filename and "eo_job_catologue" in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
            # values = {"last_maintanance_date": default_to_start_date.date()}
            # print('default_to_start_date: ', default_to_start_date)
            #print(df.loc[df['last_maintanance_date']])
            #df.fillna(value=values)
            # df.to_csv('data/df_delete.csv')
            # print(df.info())
            updated_eo_maintanance_job_code_last_date = df.loc[:, ['eo_maintanance_job_code', 'last_maintanance_date']]
            functions.maintanance_jobs_df_prepare()
            functions.fill_calendar_fond()
            functions.maintanance_matrix()
            functions.eo_job_catologue()
        
            updated_eo_maintanance_job_code_last_date.to_csv('data/eo_maintanance_job_code_last_date.csv')
            
            
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
def update_output_(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n) for c, n in zip(list_of_contents, list_of_names)]
        
        return children


# обработчик выгрузки "Выгрузить maintanance_job_list_general"
@app.callback(
    Output("download_maintanance_job_list_general", "data"),
    Input("btn_download_maintanance_job_list_general", "n_clicks"),
    prevent_initial_call=True,
)
def download_maintanance_job_list_general(n_clicks):
    if n_clicks:
      df = pd.read_csv('data/maintanance_job_list_general.csv', dtype=str)
      df = df.loc[:, ['maintanance_code_id', 'maintanance_code',	'maintanance_name',	'upper_level_tehmesto_code',	'upper_level_tehmesto_description',	'interval_motohours',	'downtime_planned',	'source']]

      df = df.astype({'downtime_planned': float, 'interval_motohours': float})
      return dcc.send_data_frame(df.to_excel, "maintanance_job_list_general.xlsx", index=False, sheet_name="maintanance_job_list_general")


# обработчик выгрузки "Выгрузить eo_job_catologue"
@app.callback(
    Output("download_eo_job_catologue", "data"),
    Input("btn_download_eo_job_catologue", "n_clicks"),
    prevent_initial_call=True,
)
def download_eo_job_catologue(n_clicks):
    if n_clicks:
      df_catalogue = pd.read_csv('data/eo_job_catologue.csv', dtype=str)
      df_dates = pd.read_csv('data/eo_maintanance_job_code_last_date.csv', dtype = str)
      df = pd.merge(df_catalogue, df_dates, on = 'eo_maintanance_job_code', how = 'left')
      # df = df.astype({'level_no': int})
      return dcc.send_data_frame(df.to_excel, "eo_job_catologue.xlsx", index=False, sheet_name="eo_job_catologue")

if __name__ == "__main__":
    # app.run_server(debug=True)
    app.run_server(host='0.0.0.0', debug=False)
