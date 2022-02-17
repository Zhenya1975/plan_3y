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
  '''График простоев по месяцам за три года'''
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

  return fig_downtime