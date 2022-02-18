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


############# PIECHART ПРОСТОИ ПО КАТЕГОРИЯМ #####################
def fig_piechart_downtime_by_categories(maintanance_jobs_df, theme_selector):  
  maint_categ = maintanance_jobs_df.groupby('maintanance_category_id', as_index=False)['dowtime_plan, hours'].sum()
  
  labels = list(maint_categ['maintanance_category_id'])
  values = list(maint_categ['dowtime_plan, hours'])
  if theme_selector:
      graph_template = 'sandstone'
  else:
      graph_template = 'plotly_dark'
  planned_downtime_piechart = go.Figure(data=[go.Pie(labels=labels, values=values)])
  planned_downtime_piechart.update_layout(
    title_text='Простой по видам работ',
    template=graph_template,
    )
  return planned_downtime_piechart