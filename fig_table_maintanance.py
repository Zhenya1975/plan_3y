import pandas as pd
import plotly.graph_objects as go
import pandas as pd
from dash_bootstrap_templates import ThemeSwitchAIO
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc

import initial_values

# select the Bootstrap stylesheet2 and figure template2 for the theme toggle here:
# template_theme1 = "sketchy"
template_theme1 = "flatly"
template_theme2 = "darkly"
# url_theme1 = dbc.themes.SKETCHY
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.DARKLY

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

############ подготовка таблицы со списком работ ####################
def fig_table_maintanance(maintanance_jobs_df, theme_selector):
  # выбираем поля из full_eo_list
  eo_list_df = initial_values.full_eo_list.loc[:, ['eo_code', 'eo_description', 'level_upper', 'operation_start_date', 'avearage_day_operation_hours']]
  # джойним maintanance_jobs_df с eo_list
  maintanance_jobs_df_ = pd.merge(maintanance_jobs_df, eo_list_df, on = 'eo_code', how = 'left')
  maintanance_jobs_df = maintanance_jobs_df_
  
  maintanance_jobs_df = maintanance_jobs_df.astype({'interval_motohours': float})
  maintanance_jobs_df = maintanance_jobs_df.astype({'interval_motohours': int})
  
  result_table = maintanance_jobs_df.loc[:, ['maintanance_datetime', 'maintanance_name','dowtime_plan, hours','interval_motohours', 'eo_description', 'maint_interval', 'go_interval_list', 'days_between_maintanance', 'next_maintanance_datetime']]  
  result_table['Дата'] = result_table['maintanance_datetime'].dt.strftime('%d.%m.%Y')
  
  # result_table['next_maintanance_datetime'] = result_table['next_maintanance_datetime'].dt.strftime('%d.%m.%Y')

  
  # result_table = result_table.astype({'days_between_maintanance': int})

  result_table.rename(columns = {'maintanance_name': 'Категория работ', 'dowtime_plan, hours': 'Запланированный простой, час', 'interval_motohours': 'Межсервисная наработка, час', 'eo_description':'Наименование ЕО', 'maint_interval':'Межсервисный интервал', 'go_interval_list': 'Список форм с учетом поглащения', 'days_between_maintanance': 'Кол-во дней между формами','next_maintanance_datetime':'Дата следующей формы'}, inplace = True)
  
  result_table = result_table.loc[:, ['Дата', 'Категория работ','Запланированный простой, час', 'Межсервисная наработка, час', 'Наименование ЕО', 'Межсервисный интервал', 'Список форм с учетом поглащения', 'Кол-во дней между формами', 'Дата следующей формы']]

  
  result_table.to_csv('data/result_table_delete.csv')
  
  # print(result_table)
