import pandas as pd
# import numpy as np
from dash import Dash, dcc, html, Input, Output, callback_context, State, callback_context
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO
from dash_bootstrap_templates import load_figure_template
import datetime
import functions
import title_text
import fig_downtime_by_years
import fig_table_maintanance
import fig_ktg_by_years
import fig_planned_3y_ktg
import fig_piechart_downtime_by_categories
import ktg_by_month_models
import ktg_table_html

import maintanance_chart_tab
import settings_tab
import coverage_tab
import initial_values

from dash import dash_table
import base64
import io
import json
import plotly.graph_objects as go
import fig_coverage

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
    'height': '34px'
}



app.layout = dbc.Container(
    dbc.Row(        [
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
                                coverage_tab.coverage_tab(),
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
    fluid=True,
    
)


######################### ОСНОВНОЙ ОБРАБОТЧИК ДЛЯ ПОСТРОЕНИЯ ГРАФИКОВ ##############################
@app.callback([
    
    Output("checklist_main_eo_class", "value"),
    Output("checklist_main_eo_class", "options"),
  
    Output("checklist_eo", "value"),
    Output("checklist_eo", "options"),
  
    Output("maintanance_category_checklist", "value"),
    Output("maintanance_category_checklist", "options"),
  
    Output('be_title_id', 'children'),
    Output('level_upper_title_id', 'children'),
    Output('number_of_eo_title_id', 'children'),
    Output('downtime_2023', 'children'),
    Output('cal_fond_2023', 'children'),


    Output('planned_downtime', 'figure'),
    Output('planned_downtime_piechart', 'figure'),
    Output('ktg_by_years', 'figure'),
    Output('fig_ktg_3y_by_months_id', 'figure'),
    Output('loading', 'parent_style'),
    Output('ktg_by_month_table', 'children'),
],
    [
        Input('select_all_maintanance_category_checklist', 'n_clicks'),
        Input('release_all_maintanance_category_checklist', 'n_clicks'),
        Input('checklist_level_1', 'value'),
        Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
        Input('checklist_main_eo_class', 'value'),
        Input('checklist_eo', 'value'),
        Input('maintanance_category_checklist', 'value'),
        
    ],
)

def maintanance(select_all_maintanance_category_checklist, release_all_maintanance_category_checklist, checklist_level_1, theme_selector, checklist_main_eo_class, checklist_eo, maintanance_category_checklist):
  
  changed_id = [p['prop_id'] for p in callback_context.triggered][0]
  if theme_selector:
      graph_template = 'sandstone'
  # bootstrap

  else:
      graph_template = 'plotly_dark'
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
  level_upper_full_list_df = initial_values.full_eo_list.loc[:, ['eo_code', 'level_upper']]
  maintanance_jobs_df = maintanance_jobs_df.copy()
  maintanance_jobs_df = pd.merge(maintanance_jobs_df, level_upper_full_list_df, on = 'eo_code', how = 'left')
  level_upper_full_list = maintanance_jobs_df['level_upper'].unique()
  
  if checklist_main_eo_class == None:
    level_upper_filter_list = level_upper_full_list
  elif checklist_main_eo_class == []:
    level_upper_filter_list = level_upper_full_list
  else:
    level_upper_filter_list =  checklist_main_eo_class
  
  maintanance_jobs_full_for_eo_filter_df = maintanance_jobs_df.loc[maintanance_jobs_df['level_upper'].isin(level_upper_filter_list)]
    
  eo_full_list = maintanance_jobs_full_for_eo_filter_df['eo_code'].unique()
  if checklist_eo == None:
    eo_filter_list = eo_full_list
  elif checklist_eo == []:
    eo_filter_list = eo_full_list
  else:
    eo_filter_list = checklist_eo
  
  maintanance_jobs_df = maintanance_jobs_df.loc[maintanance_jobs_df['level_upper'].isin(level_upper_filter_list)&
  maintanance_jobs_df['eo_code'].isin(eo_filter_list)
  ]
  maintanance_jobs_df_before_maintanance_category_filter = maintanance_jobs_df

  
  # читаем календарный фонд
  eo_calendar_fond = pd.read_csv('data/eo_calendar_fond.csv', dtype = str)
  eo_calendar_fond = eo_calendar_fond.astype({'calendar_fond': float})
  # поле даты - в datetime
  eo_calendar_fond['datetime'] = pd.to_datetime(eo_calendar_fond['datetime'])
  # full_eo_list = pd.read_csv('data/full_eo_list.csv', dtype = str)
  
  # нужно порезать календарный фонд на те машины, которые есть в простоях
  # список машин который остался в простоях после фильтрации по бизнес-единицу, вышестоящему месту и ЕО
  # ниже maintanance_jobs_df ббудет порезан на категории работ. при этом это не коснется выборки по календарному фонду
  eo_list_in_maintanance_jobs_df = maintanance_jobs_df['eo_code'].unique()

  eo_calendar_fond = eo_calendar_fond.copy()
  eo_calendar_fond = eo_calendar_fond.loc[eo_calendar_fond['eo_code'].isin(eo_list_in_maintanance_jobs_df)]
  # eo_calendar_fond_full = eo_calendar_fond

  # список ЕО, на которые есть календарный фонд
  # eo_cal_fond = pd.DataFrame(eo_calendar_fond['eo_code'].unique(), columns = ['eo_code'], dtype = str)
  # список ЕО, на которые есть расчет простоев
  # eo_downtime = pd.DataFrame(maintanance_jobs_df['eo_code'].unique(), columns = ['eo_code'], dtype = str)
  # делаем пересечение этих списков.
  # eo_for_ktg = pd.merge(eo_cal_fond, eo_downtime, on = 'eo_code', how = 'inner')['eo_code'].unique()

  # режем датафрейм с простоями по eo_for_ktg
  # maintanance_jobs_df = maintanance_jobs_df.copy()
  
  # maintanance_jobs_df = maintanance_jobs_df.loc[maintanance_jobs_df['eo_code'].isin(eo_for_ktg)]
  
  
  # режем датафрейм с календарным фондом  по eo_for_ktg
  # maintanance_jobs_df = maintanance_jobs_df.copy()
  # maintanance_jobs_df = maintanance_jobs_df.loc[maintanance_jobs_df['eo_code'].isin(eo_for_ktg)]
 

  ###################### данные для селектов фильтров по _main_eo_class ################
  checklist_main_eo_class_value  = []
  if checklist_main_eo_class != None:
    checklist_main_eo_class_value = checklist_main_eo_class
  checklist_main_eo_class_options = functions.checklist_main_eo_class_options(maintanance_jobs_full_df)[0]

  ###################### данные для селектов фильтров по машинами ################
  # фильтр по машинам - пока это просто список maintanance_jobs_df 
  eo_list_value  = []
  if checklist_eo != None:
    eo_list_value = checklist_eo
  eo_list_options = functions.eo_checklist_data(maintanance_jobs_full_for_eo_filter_df)[0]

  ############## чек-лист для фильтра по типам работ ##################
  maintanance_category_checklist_data = functions.maintanance_category_filter(maintanance_jobs_full_df)[0]
    
  # maintanance_category_checklist - из инпута функции. Значение в селектах
  # если в чек-листе что-то выбрано, то значения равны выбору
  if maintanance_category_checklist != None:
    maint_category_list = maintanance_category_checklist
    '''maint_category_list - фильтр для фильтрации maintanance_jobs_df'''
    maint_category_list_value = maintanance_category_checklist
    '''maint_category_list_value - фильтр для Output основного колбэка'''
  elif maintanance_category_checklist == None:
    maint_category_list = functions.maintanance_category_filter(maintanance_jobs_df)[1]
    maint_category_list_value = functions.maintanance_category_filter(maintanance_jobs_df)[1]


  # Обработчик кнопок Снять / Выбрать
  id_select_all_maintanance_category = "select_all_maintanance_category_checklist"
  id_release_all_maintanance_category = "release_all_maintanance_category_checklist"

  if id_select_all_maintanance_category in changed_id:
    maint_category_list_value = functions.maintanance_category_filter(maintanance_jobs_full_df)[1]
    maint_category_list = functions.maintanance_category_filter(maintanance_jobs_full_df)[1]
  elif id_release_all_maintanance_category in changed_id:
 
    maint_category_list_value = []
    maint_category_list = []

  maintanance_jobs_df['year'] = maintanance_jobs_df['maintanance_datetime'].dt.year
  maintanance_jobs_df['month'] = maintanance_jobs_df['maintanance_datetime'].dt.month
  maintanance_jobs_df['month_year'] = maintanance_jobs_df['month'].astype('str') + "_"+ maintanance_jobs_df['year'].astype('str')

    
  # eo_filter_list - фильтр по машинам  
  # level_upper_filter_list - фильтр по Вышестоящему техместу
  level_upper = pd.read_csv('data/level_upper.csv')
  
  # джойним с level_upper
  maintanance_jobs_df = pd.merge(maintanance_jobs_df, level_upper, on = 'level_upper', how = 'left')
  # создаем поле-ключ teh-mesto-month-year 
  maintanance_jobs_df['teh_mesto_month_year'] = maintanance_jobs_df['level_upper'] + '_' + maintanance_jobs_df['month_year']
  
  maintanance_jobs__for_zero_dowtime = maintanance_jobs_df.loc[:, ['teh_mesto_month_year', 'level_upper', 'Название технического места', 'month_year', 'year']]
  maintanance_jobs__for_zero_dowtime['dowtime_plan, hours'] = 0
  maintanance_jobs__for_zero_dowtime_groupped = maintanance_jobs__for_zero_dowtime.groupby(['teh_mesto_month_year', 'level_upper', 'Название технического места', 'month_year', 'year'], as_index=False)['dowtime_plan, hours'].sum()
  
  maintanance_jobs_df = maintanance_jobs_df.loc[maintanance_jobs_df['eo_code'].isin(eo_filter_list) &
  maintanance_jobs_df['level_upper'].isin(level_upper_filter_list) &
  maintanance_jobs_df['maintanance_category_id'].isin(maint_category_list)
  ]
  

  maint_category_list_options = maintanance_category_checklist_data

  ######################## титульный текст из КАКИХ БЕ машины в выборке #######################
  be_title = title_text.title_text(maintanance_jobs_df)[0]
  ######################## титульный текст level_upper в выборке #######################
  level_upper_title =  title_text.title_text(maintanance_jobs_df)[1]
  ######################## титульный текст кол-во машин в выборке #######################
  number_of_eo_title = title_text.title_text(maintanance_jobs_df)[2]

  ######################## Карточка за 2023 год #######################
  maintanance_jobs_df['year'] = maintanance_jobs_df['maintanance_datetime'].dt.year

  downtime_2023 = int(maintanance_jobs_df.loc[maintanance_jobs_df['year'] == 2023]['dowtime_plan, hours'].sum())

  downtime_2023 = 'Общий простой ,час: {}'.format(downtime_2023)

  eo_calendar_fond['year'] = eo_calendar_fond['datetime'].dt.year
  cal_fond_2023_sum = int(eo_calendar_fond.loc[eo_calendar_fond['year']==2023]['calendar_fond'].sum())

  cal_fond_2023 = 'Общий календарный фонд ,час: {}'.format(cal_fond_2023_sum)

  ################# ГРАФИК С ПРОСТОЯМИ ЗА 3 ГОДА #######################################
  fig_downtime = fig_downtime_by_years.fig_downtime_by_years(maintanance_jobs_df, theme_selector)

  ################# ГРАФИК КТГ ПО МЕСЯЦАМ ЗА ТРИ ГОДА ##################################
  fig_ktg_3y_by_months = fig_planned_3y_ktg.fig_downtime_planned_3y_ktg(maintanance_jobs_df, eo_calendar_fond, theme_selector)


  ############# PIECHART ПРОСТОИ ПО КАТЕГОРИЯМ #####################
  planned_downtime_piechart = fig_piechart_downtime_by_categories.fig_piechart_downtime_by_categories(maintanance_jobs_df, theme_selector)

  
  ################ ГРАФИК КТГ ПО ГОДАМ ЗА 3 ГОДА #######################################
  fig_ktg_by_yrs = fig_ktg_by_years.fig_ktg_by_years(maintanance_jobs_df, theme_selector, eo_calendar_fond)

  
  new_loading_style = loading_style

  # подготовка файла для выгрузки excel с простоями
  fig_table_maintanance.fig_table_maintanance(maintanance_jobs_df)

  # выполнение скрипта подготовки таблицы ктг-месяц-модель-машины
  
  ktg_df = ktg_by_month_models.ktg_by_month_models(maintanance_jobs_df, eo_calendar_fond, maintanance_jobs__for_zero_dowtime_groupped, 2023)
  

  
  ktg_by_month_table = ktg_table_html.ktg_table(ktg_df)
  # ktg_by_month_table = html.Div()
  
  return checklist_main_eo_class_value, checklist_main_eo_class_options, eo_list_value, eo_list_options, maint_category_list_value, maint_category_list_options, be_title, level_upper_title, number_of_eo_title, downtime_2023, cal_fond_2023, fig_downtime, planned_downtime_piechart, fig_ktg_by_yrs, fig_ktg_3y_by_months, new_loading_style, ktg_by_month_table



################### ВКЛАДКА ПОКРЫТИЕ ##################################
@app.callback([
  Output("total_number_of_models_for_3y_plan", "children"),
  Output("number_of_eo_models_with_strategy", "children"),
  Output("eo_models_in_plan_pie_chart", "figure"),
  Output("eo_in_plan_pie_chart", "figure"),
  
  Output("total_number_of_eo_for_3y_plan", "children"),
  Output("number_of_eo_with_strategy", "children"),
  
  
],
[
  Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
    ],
)

def coverage_tab(theme_selector):

  ########################### общее кол-во моделей ЕО которые должны быть покрыты планом #########################
  # читаем полный список оборудования
  full_eo_list_actual = pd.read_csv('data/full_eo_list_actual.csv')
  full_eo_list = pd.read_csv('data/full_eo_list.csv')
  # берем строки, у которых в поле eo_model_id значение не равно no_data
  total_number_of_models_for_3y_plan = len(full_eo_list_actual.loc[full_eo_list_actual['eo_model_id'] != 'no_data']['eo_model_id'].unique())
  total_model_number_of_models_for_3y_plan_string = 'Общее кол-во моделей ЕО для 3-Y плана: {}'.format(total_number_of_models_for_3y_plan)
  
  ########################### кол-во моделей ЕО которые фактически планом #########################
  number_of_eo_models_with_strategy = len(full_eo_list_actual.loc[full_eo_list_actual['strategy_id'] != 0]['eo_model_id'].unique())
  number_of_eo_models_with_strategy_string = 'Кол-во моделей EO со стратегией: {}'.format(number_of_eo_models_with_strategy)

  eo_models_in_plan_pie_chart_fig =   fig_coverage.fig_eo_models_in_plan_pie_chart(total_number_of_models_for_3y_plan,number_of_eo_models_with_strategy, theme_selector)

  
  
  ########################### общее кол-во ЕО которые должны быть покрыты планом #########################
  total_number_of_eo_for_3y_plan = len(full_eo_list_actual.loc[full_eo_list_actual['eo_model_id'] != 'no_data']['eo_code'].unique())
  total_number_of_eo_for_3y_plan_string = 'Общее кол-во ЕО для 3-Y плана: {}'.format(total_number_of_eo_for_3y_plan)

  ########################### кол-во ЕО которые фактически покрыты планом #########################
  number_of_eo_with_strategy = len(full_eo_list.loc[full_eo_list['strategy_id'] != 0]['eo_code'].unique())
  number_of_eo_with_strategy_string = 'Кол-во EO со стратегией: {}'.format(number_of_eo_with_strategy)

  eo_in_plan_pie_chart_fig = fig_coverage.fig_eo_in_plan_pie_chart(total_number_of_eo_for_3y_plan,number_of_eo_with_strategy, theme_selector)
  
  return [total_model_number_of_models_for_3y_plan_string, number_of_eo_models_with_strategy_string, eo_models_in_plan_pie_chart_fig, eo_in_plan_pie_chart_fig, total_number_of_eo_for_3y_plan_string, number_of_eo_with_strategy_string]

  
  
  
  ######################################################################### 


  
########## Настройки################


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xlsx' in filename and "maintanance_job_list_general" in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded),decimal=',')
            

            # проверяем, что в файле есть нужные колонки 
            list_of_columns_in_uploaded_df = df.columns.tolist()
            check_column_list = ['maintanance_code_id', 'maintanance_code', 'maintanance_category_id','upper_level_tehmesto_code', 'maintanance_name', 'interval_motohours', 'downtime_planned', 'pass_interval', 'source']
            control_value = 1
            
            for column in check_column_list:
              if column in list_of_columns_in_uploaded_df:
                continue
              else:
                control_value = 0
          
                break
     
            if control_value == 1:
       
              df.to_csv('data/maintanance_job_list_general.csv')
              functions.pass_interval_fill()
              functions.maintanance_category_prep()
              functions.eo_job_catologue()
            else:
              print('не хватает колонок')
            
            # если мы загрузили список с работами, то надо подготовить данные для того чтобы вставить
            # даты начала расчета для ТО-шек
            

        elif 'xlsx' in filename and "eo_job_catologue" in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
            # values = {"last_maintanance_date": default_to_start_date.date()}

            #df.fillna(value=values)
  
            updated_eo_maintanance_job_code_last_date = df.loc[:, ['eo_maintanance_job_code', 'last_maintanance_date']]
            
            functions.fill_calendar_fond()
            #functions.maintanance_matrix()
            functions.eo_job_catologue()
            functions.maintanance_jobs_df_prepare()
        
            updated_eo_maintanance_job_code_last_date.to_csv('data/eo_maintanance_job_code_last_date.csv')

        # загружаем список eo - в ответ получаем список для перепроверки даты ввода в эксплуатацию, даты списания, среднесуточной наработки
        elif 'xlsx' in filename and "eo_request_data" in filename:
          # Assume that the user uploaded an excel file
          df_eo_request_list = pd.read_excel(io.BytesIO(decoded), dtype=str)
          # объединяем с full_eo_list
          eo_list = pd.read_csv('data/full_eo_list_actual.csv', dtype=str)
          eo_list_data = pd.merge(df_eo_request_list, eo_list, on = 'eo_code', how = 'left')
          # объединяем с level_1
          level_1 = pd.read_csv('data/level_1.csv')
          eo_list_data = pd.merge(eo_list_data, level_1, on = 'level_1', how = 'left')
          # объединяем с level_upper
          level_upper = pd.read_csv('data/level_upper.csv', dtype=str)
          eo_list_data = pd.merge(eo_list_data, level_upper, on = 'level_upper', how = 'left')
          # объединяем с level_2
          level_2 = pd.read_csv('data/level_2_list.csv', dtype=str)
          eo_list_data = pd.merge(eo_list_data, level_2, on = 'level_2_path', how = 'left')
          date_columns = ["operation_start_date", "operation_finish_date"]
          # Колонку со строкой - в дату
          for column in date_columns:
            eo_list_data[column] =  eo_list_data[column].astype("datetime64[ns]")
            # колонку  с datetime - в строку
            eo_list_data[column] = eo_list_data[column].dt.strftime("%d.%m.%Y")
          
          eo_list_data = eo_list_data.loc[:, ['level_1_description', 'Название технического места', 'eo_code', 'eo_description', 'mvz', 'level_2_description', 'operation_start_date','operation_finish_date', 'avearage_day_operation_hours']]
          eo_list_data.to_csv('data/eo_list_data_temp.csv', index = False)
          
          # print(df_eo_request_list)
          df = df_eo_request_list
          
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

######################## ОБРАБОТЧИК ВЫГГРУЗКИ EO_LIST #####################################
@app.callback(
    Output("download_eo_list", "data"),
    Input("btn_download_eo_list", "n_clicks"),
    prevent_initial_call=True,
)
def download_eo_list(n_clicks):
  if n_clicks:
    eo_list = pd.read_csv('data/full_eo_list.csv', dtype=str)
    # объединяем с level_1
    level_1 = pd.read_csv('data/level_1.csv')
    eo_list_upload = pd.merge(eo_list, level_1, on = 'level_1', how = 'left')
    # объединяем с level_upper
    level_upper = pd.read_csv('data/level_upper.csv', dtype=str)
    eo_list_upload = pd.merge(eo_list_upload, level_upper, on = 'level_upper', how = 'left')
    # объединяем с level_2
    level_2 = pd.read_csv('data/level_2_list.csv', dtype=str)
    eo_list_upload = pd.merge(eo_list_upload, level_2, on = 'level_2_path', how = 'left')
    date_columns = ["operation_start_date", "operation_finish_date"]
    # Колонку со строкой - в дату
    for column in date_columns:
      eo_list_upload[column] =  eo_list_upload[column].astype("datetime64[ns]")
      # колонку  с datetime - в строку
      eo_list_upload[column] = eo_list_upload[column].dt.strftime("%d.%m.%Y")
    
    eo_list_upload = eo_list_upload.loc[:, ['level_1_description', 'Название технического места', 'eo_code', 'eo_description', 'mvz', 'level_2_description', 'operation_start_date','operation_finish_date', 'avearage_day_operation_hours']]
    eo_list_upload.to_csv('data/eo_list_upload_delete.csv', index = False)
    
    #  df = df.loc[:, ['maintanance_code_id', 'maintanance_code',	'maintanance_category_id','maintanance_name',	'upper_level_tehmesto_code',	'upper_level_tehmesto_description',	'interval_motohours',	'downtime_planned','pass_interval',	'source']]

    # eo_list_upload = eo_list_upload.astype({'downtime_planned': float, 'interval_motohours': float})
    return dcc.send_data_frame(eo_list_upload.to_excel, "eo_data.xlsx", index=False, sheet_name="eo_data")


#########################      


      
# обработчик выгрузки "Выгрузить maintanance_job_list_general"
@app.callback(
    Output("download_maintanance_job_list_general", "data"),
    Input("btn_download_maintanance_job_list_general", "n_clicks"),
    prevent_initial_call=True,
)
def download_maintanance_job_list_general(n_clicks):
    if n_clicks:
      df = pd.read_csv('data/maintanance_job_list_general.csv', dtype=str)
      df = df.loc[:, ['maintanance_code_id', 'maintanance_code',	'maintanance_category_id','maintanance_name',	'upper_level_tehmesto_code',	'upper_level_tehmesto_description',	'interval_motohours',	'downtime_planned','pass_interval',	'source']]

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
      eo_job_catologue_df = pd.read_csv('data/eo_job_catologue.csv', dtype=str)

      return dcc.send_data_frame(eo_job_catologue_df.to_excel, "eo_job_catologue.xlsx", index=False, sheet_name="eo_job_catologue")

# Обработчик кнопки выгрузки в эксель таблицы с простоями
@app.callback(
    Output("download_excel_downtime_table", "data"),
    Input("btn_download_downtime_table", "n_clicks"),
    prevent_initial_call=True,)
def funct(n_clicks_downtime_table):
  df = pd.read_csv('data/downtime_data_table.csv')
  if n_clicks_downtime_table:
    return dcc.send_data_frame(df.to_excel, "данные о простоях.xlsx", index=False, sheet_name="данные о простоях")
  
# Обработчик кнопки выгрузки в эксель таблицы с ктг
@app.callback(
    Output("download_ktg_table", "data"),
    Input("btn_download_ktg_table", "n_clicks"),
    prevent_initial_call=True,)
def funct(n_clicks_ktg_table):
  df = pd.read_csv('data/ktg_by_months.csv')
  if n_clicks_ktg_table:
    return dcc.send_data_frame(df.to_excel, "ктг по месяцам.xlsx", index=False, sheet_name="ктг по месяцам")

if __name__ == "__main__":
    # app.run_server(debug=True)
    app.run_server(host='0.0.0.0', debug=True)
