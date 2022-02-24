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

  # фильтруем maintanance_jobs_df по годам
  year = year
  maintanance_jobs_df = maintanance_jobs_df.loc[maintanance_jobs_df['year']==year]
  # maintanance_jobs_df.to_csv('data/maintanance_jobs_df_delete.csv')
  eo_models_df = pd.read_csv('data/eo_models.csv')
  eo_models_df = eo_models_df.astype({'eo_model_id': str})
 
  maintanance_jobs_df = maintanance_jobs_df.astype({'eo_model_id': str})

  
  maintanance_jobs_df = pd.merge(maintanance_jobs_df, eo_models_df, on = 'eo_model_id', how = 'left')
  # maintanance_jobs_df.to_csv('data/maintanance_jobs_df_delete.csv')
  maintanance_jobs_df = maintanance_jobs_df.copy()
  maintanance_jobs_df['eo_model_id_month_year'] = maintanance_jobs_df['eo_model_id'] + '_' + maintanance_jobs_df['month_year']
  
  month_year_downtime = maintanance_jobs_df.groupby(['eo_model_id_month_year','eo_model_id','eo_model_name', 'month_year'], as_index=False)['dowtime_plan, hours'].sum()
  
  
  # month_year_downtime.to_csv('data/month_year_downtime_delete.csv')

  # Считаем календарный фонд
  eo_calendar_fond = eo_calendar_fond
  eo_calendar_fond = eo_calendar_fond.loc[eo_calendar_fond['year'] ==year]
  # джойним с full_eo_list
  full_eo_list = initial_values.full_eo_list.loc[:, ['eo_code', 'level_upper', 'eo_model_id', 'eo_model_name']]
  eo_calendar_fond_eo_list = pd.merge(eo_calendar_fond, full_eo_list, on = 'eo_code', how = 'left')  

    # создаем поле-ключ eo_model_ideo_model_id-month-year 
  eo_calendar_fond_eo_list['eo_model_id_month_year'] =eo_calendar_fond_eo_list['eo_model_id'] + '_' + eo_calendar_fond_eo_list['month_year']
  
  month_year_calendar_fond = eo_calendar_fond_eo_list.groupby(['eo_model_id_month_year'], as_index=False)['calendar_fond'].sum()
  
  ######################## ЕСЛИ ТАБЛИЦА С ПРОСТОЯМИ ПУСТАЯ #######
  if len(maintanance_jobs_df) == 0:
    month_year_downtime['dowtime_plan, hours'] = 0
  
  downtime_calendar_fond_df = pd.merge(month_year_downtime, month_year_calendar_fond, on = 'eo_model_id_month_year')
  downtime_calendar_fond_df['ktg'] = (downtime_calendar_fond_df['calendar_fond'] -downtime_calendar_fond_df['dowtime_plan, hours'])/downtime_calendar_fond_df['calendar_fond']
  decimals = 2    
  downtime_calendar_fond_df['ktg'] = downtime_calendar_fond_df['ktg'].apply(lambda x: round(x, decimals))
  
  period_dict = {'1_2023': "янв 2023", '2_2023': "фев 2023", '3_2023': "мар 2023", '4_2023': "апр 2023", '5_2023': "май 2023", '6_2023': "июн 2023", '7_2023': "июл 2023", '8_2023': "авг 2023", '9_2023': "сен 2023", '10_2023': "окт 2023", '11_2023': "ноя 2023", '12_2023': "дек 2023"}
  period_sort_index = {'1_2023':1, '2_2023': 2, '3_2023': 3, '4_2023': 4, '5_2023': 5, '6_2023': 6, '7_2023': 7, '8_2023': 8, '9_2023': 9, '10_2023': 10, '11_2023': 11, '12_2023': 12}
  downtime_calendar_fond_df['period'] = downtime_calendar_fond_df['month_year'].map(period_dict).astype(str)

  downtime_calendar_fond_df['period_sort_index'] = downtime_calendar_fond_df['month_year'].map(period_sort_index)
  
  # model_names_dict = 
  
  downtime_calendar_fond_df.sort_values(by='period_sort_index', inplace = True)
  
  
  # downtime_calendar_fond_df.to_csv('data/downtime_calendar_fond_df_delete.csv')

  # итерируемся по списку техмест - моделей машин
  downtime_calendar_fond_df = downtime_calendar_fond_df.astype({'eo_model_id': float})
  downtime_calendar_fond_df = downtime_calendar_fond_df.astype({'eo_model_id': int})
  
  eo_model_id_list = list(downtime_calendar_fond_df['eo_model_id'].unique())
  # print('type of eo_model_id_list', type(eo_model_id_list))
  # print(eo_model_id_list)
  # index_listindex_list - индексы целефого датафрейма
  # список колонок 
  
  columns_list = ['модель', "янв 2023", "фев 2023", "мар 2023", "апр 2023", "май 2023", "июн 2023", "июл 2023", "авг 2023", "сен 2023",  "окт 2023", "ноя 2023", "дек 2023"]
  index_list = eo_model_id_list
  
  ktg_table_df = pd.DataFrame(columns=columns_list, index=index_list)
  # print(df)
  for indx in eo_model_id_list:
    temp_dict = {}
    temp_df = downtime_calendar_fond_df.loc[downtime_calendar_fond_df['eo_model_id']==indx]
    # print(temp_df)
    # df.loc['y'] = pd.Series({'a':1, 'b':5, 'c':2, 'd':3})
    
    temp_dict["модель"] = list(temp_df['eo_model_name'].unique())[0]
    
    for index, row in temp_df.iterrows():
      model_code = row['eo_model_id']
      month_year = row['period']
      ktg_value = row['ktg']
      temp_dict[month_year] = ktg_value
    
    ktg_table_df.loc[indx] = pd.Series(temp_dict)
    ktg_table_df.to_csv('data/ktg_by_months.csv')
  
  return ktg_table_df    

      

      
    # print(temp_df_name)
    # df = pd.DataFrame({'eo_model_id':  eo_model})
    # print('df', df) 
    # for index, row in downtime_calendar_fond_df_temp.iterrows():
    #  period_name = row['period']
    #  ktg_value = row['ktg']
  #    df[period_name] = ktg_value

  #  temp_df_name = level_upper + "_df"
  #  temp_df_name = df
  #  # print(temp_df_name)
  #  df.to_csv('data/ktg_by_months.csv')
   # return df
    

  

  

  
 


      
    

  
  
  