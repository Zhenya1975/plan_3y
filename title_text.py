######################## титульный текст из КАКИХ БЕ машины в выборке #######################
import pandas as pd
import initial_values

def title_text(maintanance_jobs_df):

  eo_list_with_filters_df = pd.DataFrame(maintanance_jobs_df['eo_code'].unique(), columns = ['eo_code'], dtype = str)
  eo_list = initial_values.full_eo_list.loc[:, ['eo_code', 'level_1', 'level_upper']]
  # джойним со списком машин
  
  eo_list_with_filters_data_df = pd.merge(eo_list_with_filters_df, eo_list, on='eo_code', how='left')

  # джойним с текстом наименований бизнес-единиц
  level_1 = pd.read_csv('data/level_1.csv', dtype = str)
  eo_list_with_filters_data_level_1_df = pd.merge(eo_list_with_filters_data_df, level_1, on = 'level_1', how = 'left')

  # список бизнес единиц:
  be_list = eo_list_with_filters_data_level_1_df['level_1_description'].unique()

  text_be= ''
  for word in be_list:
    text_be = text_be + word + ' '

  be_title = 'БЕ: {}'.format(text_be)
  
  ######################## титульный текст level_upper в выборке #######################
  # список уникальных level_upper в выборке
  level_upper_current_unique_df = pd.DataFrame(eo_list_with_filters_data_df['level_upper'].unique(), columns = ['level_upper'])
  
  level_upper_df = pd.read_csv('data/level_upper.csv')
  level_upper_with_filters_data_level_upper_df = pd.merge(level_upper_current_unique_df, level_upper_df, on = 'level_upper', how = 'left')
  level_upper_title_list = level_upper_with_filters_data_level_upper_df['Название технического места'].unique()
  text_level_upper= ''
  for word in level_upper_title_list:
    text_level_upper = text_level_upper + word + ' '

  level_upper_title = 'Вшст. техместо: {}'.format(text_level_upper)
  
  number_of_eo = len(maintanance_jobs_df['eo_code'].unique())
  
  number_of_eo_title = 'Кол-во EO в выборке: {}'.format(number_of_eo)  



  return be_title, level_upper_title, number_of_eo_title