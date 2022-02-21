import pandas as pd
import initial_values

def ktg_by_month_models(maintanance_jobs_df,eo_calendar_fond, maintanance_jobs__for_zero_dowtime_groupped, year):
  '''Расчет таблицы КТГ по месяцам'''  
  # Если есть хотя бы одна строка с простоями, то берем таблицу с простоями
  if len(maintanance_jobs_df) != 0:
    maintanance_jobs_df = maintanance_jobs_df
  # Если на вход получили пустую таблицу, то вместо нее подставляем таблицу с нулями в простоях
  else:
    maintanance_jobs_df = maintanance_jobs__for_zero_dowtime_groupped
  # фильтруем выборку по годам
  year = year
  maintanance_jobs_df = maintanance_jobs_df.loc[maintanance_jobs_df['year']==year]

    
  month_year_downtime = maintanance_jobs_df.groupby(['teh_mesto_month_year','level_upper','Название технического места', 'month_year'], as_index=False)['dowtime_plan, hours'].sum()

   
  eo_calendar_fond = eo_calendar_fond
  eo_calendar_fond = eo_calendar_fond.loc[eo_calendar_fond['year'] ==year]
  # джойним с full_eo_list
  full_eo_list = initial_values.full_eo_list.loc[:, ['eo_code', 'level_upper']]
  
  eo_calendar_fond_eo_list = pd.merge(eo_calendar_fond, full_eo_list, on = 'eo_code', how = 'left')
  level_upper = pd.read_csv('data/level_upper.csv')
  eo_calendar_fond_level_upper = pd.merge(eo_calendar_fond_eo_list, level_upper, on = 'level_upper', how = 'left')
  # создаем поле-ключ teh-mesto-month-year 
  eo_calendar_fond_level_upper['teh_mesto_month_year'] = eo_calendar_fond_level_upper['level_upper'] + '_' + eo_calendar_fond_level_upper['month_year']
  
  month_year_calendar_fond = eo_calendar_fond_level_upper.groupby(['teh_mesto_month_year','level_upper','Название технического места', 'month_year'], as_index=False)['calendar_fond'].sum()

  month_year_calendar_fond = month_year_calendar_fond.loc[:, ['teh_mesto_month_year', 'calendar_fond']]


  ######################## ЕСЛИ ТАБЛИЦА С ПРОСТОЯМИ НЕПУСТАЯ ##########################
  if len(maintanance_jobs_df) != 0:
    downtime_calendar_fond_df = pd.merge(month_year_downtime, month_year_calendar_fond, on = 'teh_mesto_month_year')
   
    
  elif len(maintanance_jobs_df) == 0:
    month_year_calendar_fond['dowtime_plan, hours'] = 0
    downtime_calendar_fond_df = month_year_calendar_fond
    downtime_calendar_fond_df = pd.merge(month_year_downtime, month_year_calendar_fond, on = 'teh_mesto_month_year')

    
  downtime_calendar_fond_df['ktg'] = (downtime_calendar_fond_df['calendar_fond'] -downtime_calendar_fond_df['dowtime_plan, hours'])/downtime_calendar_fond_df['calendar_fond']
  
 
  downtime_calendar_fond_df['ktg'].round(decimals = 3)
  decimals = 2    
  downtime_calendar_fond_df['ktg'] = downtime_calendar_fond_df['ktg'].apply(lambda x: round(x, decimals))
  period_dict = {'1_2023': "янв 2023", '2_2023': "фев 2023", '3_2023': "мар 2023", '4_2023': "апр 2023", '5_2023': "май 2023", '6_2023': "июн 2023", '7_2023': "июл 2023", '8_2023': "авг 2023", '9_2023': "сен 2023", '10_2023': "окт 2023", '11_2023': "ноя 2023", '12_2023': "дек 2023"}
  period_sort_index = {'1_2023':1, '2_2023': 2, '3_2023': 3, '4_2023': 4, '5_2023': 5, '6_2023': 6, '7_2023': 7, '8_2023': 8, '9_2023': 9, '10_2023': 10, '11_2023': 11, '12_2023': 12}
  downtime_calendar_fond_df['period'] = downtime_calendar_fond_df['month_year'].map(period_dict).astype(str)

  downtime_calendar_fond_df['period_sort_index'] = downtime_calendar_fond_df['month_year'].map(period_sort_index)
  downtime_calendar_fond_df.sort_values(by='period_sort_index', inplace = True)
  
  # итерируемся по списку техмест - моделей машин
  level_upper_list = maintanance_jobs_df['level_upper'].unique()
  for level_upper in level_upper_list:
    downtime_calendar_fond_df_temp = downtime_calendar_fond_df.loc[downtime_calendar_fond_df['level_upper']==level_upper]
    category_name = downtime_calendar_fond_df_temp['Название технического места'].unique()
    df = pd.DataFrame({'категория оборудования':  category_name})
    
    for index, row in downtime_calendar_fond_df_temp.iterrows():
      period_name = row['period']
      ktg_value = row['ktg']
      df[period_name] = ktg_value
        
    df.to_csv('data/ktg_by_months.csv')
    return df
    

  

  

  
 


      
    

  
  
  