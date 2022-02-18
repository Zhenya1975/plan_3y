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