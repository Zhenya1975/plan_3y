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
def fig_downtime_by_years(maintanance_jobs_df, theme_selector):
  
  # строим диаграмму по категориям, где категории - это виды работ. И отсортируем их еще по месяцам
 
  
  x_month_year = ['1_2023','2_2023','3_2023','4_2023','5_2023','6_2023','7_2023','8_2023','9_2023','10_2023','11_2023','12_2023','1_2024','2_2024','3_2024','4_2024','5_2024','6_2024','7_2024','8_2024','9_2024','10_2024','11_2024','12_2024','1_2025','2_2025','3_2025','4_2025','5_2025','6_2025','7_2025','8_2025','9_2025','10_2025','11_2025','12_2025']
  y_downtime = []
  text_list_downtime_month_year = []
  for month_year in x_month_year:
    downtime_month_year_df = maintanance_jobs_df.loc[maintanance_jobs_df['month_year']== month_year]
    downtime_month_year = downtime_month_year_df['dowtime_plan, hours'].sum()
    text = round(downtime_month_year, 0)
    y_downtime.append(downtime_month_year)
    text_list_downtime_month_year.append(text)
    
  '''График простоев по месяцам за три года'''
  #downtime_y = maintanance_jobs_df['dowtime_plan, hours']
  #dates_x = maintanance_jobs_df['maintanance_datetime']
  if theme_selector:
      graph_template = 'sandstone'
  # bootstrap

  else:
      graph_template = 'plotly_dark'

  fig_downtime = go.Figure()
  fig_downtime.add_trace(go.Bar(
    name="Простои",
    x=x_month_year, 
    y=y_downtime,
    # xperiod="M1",
    # xperiodalignment="middle",
    #textposition='auto'
    ))
  new_year_2022_2023 = pd.to_datetime('01.01.2024', format='%d.%m.%Y')
  new_year_2023_2024 = pd.to_datetime('01.01.2025', format='%d.%m.%Y')
  # fig_downtime.add_vline(x=new_year_2022_2023, line_width=3, line_color="green")
  # fig_downtime.add_vline(x=new_year_2023_2024, line_width=3, line_color="green")

  fig_downtime.update_xaxes(
    # showgrid=True, 
    # ticklabelmode="period"
  )
  fig_downtime.update_traces(
    text = text_list_downtime_month_year,
    textposition='auto'
  )
  fig_downtime.update_layout(
    title_text='Запланированный простой по месяцам за 3 года, час',
    template=graph_template,
    )

  return fig_downtime