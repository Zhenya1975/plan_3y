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

################# График КТГ по годам ###############################
def fig_ktg_by_years(maintanance_jobs_df, theme_selector, eo_calendar_fond_full):

  maintanance_jobs_df['year'] = maintanance_jobs_df['maintanance_datetime'].dt.year
  eo_calendar_fond_full['year'] = eo_calendar_fond_full['datetime'].dt.year
  # maintanance_jobs_df['year'].astype('str')
  # x_years = ['2023', '2024', '2025']
  x_years = [2023, 2024, 2025]
  y_ktg = []
  text_list = []
  for year in x_years:
    downtime_year_df = maintanance_jobs_df.loc[maintanance_jobs_df['year']==year]
    
    downtime_year = downtime_year_df['dowtime_plan, hours'].sum()
    calendar_fond_year_df = eo_calendar_fond_full.loc[eo_calendar_fond_full['year'] == year]
    
    calendar_fond = calendar_fond_year_df['calendar_fond'].sum()
    ktg_year = (calendar_fond - downtime_year) / calendar_fond
    text = round(ktg_year, 2)
    text_list.append(text)
    y_ktg.append(ktg_year)
  if theme_selector:
      graph_template = 'sandstone'
  # bootstrap

  else:
      graph_template = 'plotly_dark'
    
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
  return fig_ktg_by_years