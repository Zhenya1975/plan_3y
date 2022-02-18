import plotly.graph_objects as go
import pandas as pd
from dash_bootstrap_templates import ThemeSwitchAIO
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc


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

################# График простоев по месяцам за три года ###############################
def fig_downtime_planned_3y_ktg(maintanance_jobs_df, eo_calendar_fond, theme_selector):

  
  maintanance_jobs_df = maintanance_jobs_df
  eo_calendar_fond = eo_calendar_fond
  maintanance_jobs_df['year'] = maintanance_jobs_df['maintanance_datetime'].dt.year
  eo_calendar_fond['year'] = eo_calendar_fond['datetime'].dt.year
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
  
  
  '''График простоев по месяцам за три года'''
  #downtime_y = maintanance_jobs_df['dowtime_plan, hours']
  #dates_x = maintanance_jobs_df['maintanance_datetime']
  if theme_selector:
      graph_template = 'sandstone'
  else:
      graph_template = 'plotly_dark'
  
  fig_ktg_by_month = go.Figure()
  fig_ktg_by_month.add_trace(go.Bar(
  name="КТГ",
  x=x_month_year, 
  y=y_ktg_month_year,
  # xperiodalignment="middle",
  # textposition='auto'
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
  return fig_ktg_by_month

 