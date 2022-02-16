import pandas as pd
from datetime import timedelta
import datetime
import initial_values

full_eo_list = pd.read_csv('data/full_eo_list.csv', dtype = str)
full_eo_list['avearage_day_operation_hours'] = 23.5
# даты начала и конца трехлетнего периода
first_day_of_selection = pd.to_datetime('01.01.2023', format='%d.%m.%Y')
last_day_of_selection = pd.to_datetime('01.01.2026', format='%d.%m.%Y')
   
first_day_of_selection = initial_values.first_day_of_selection
last_day_of_selection_date = initial_values.last_day_of_selection


def pass_interval_fill():
  '''создание списка pass interval в maintanance_job_list_general'''
  maintanance_job_list_general = pd.read_csv('data/maintanance_job_list_general.csv')
  maintanance_job_list_general = maintanance_job_list_general.astype({'downtime_planned': float})
  

  for index, row in maintanance_job_list_general.iterrows():
    pass_interval_temp = row['pass_interval']
    interval_motohours = int(row['interval_motohours'])
    
    if pass_interval_temp != 'not':
      pass_interval_list = pass_interval_temp.split(';')
      pass_interval_list = [int(i) for i in pass_interval_list]
      
      # в temp_list складываем значения, которые соответствуют original pass_interval_list
      temp_list = []
      for pass_interval_value in pass_interval_list:
        if pass_interval_value not in temp_list:
          temp_list.append(pass_interval_value)
        
        temp_value = pass_interval_value
        # temp_list = []
        while temp_value < 27000:
   
          if temp_value not in temp_list:
            
            temp_list.append(temp_value)
            temp_list.sort()
          temp_value = temp_value + pass_interval_value
      #####################  Создаем список maintanance_interval #####################
      # next_go_interval - значение интервала проведения формы, которое будем итеративно считать
      next_go_interval = interval_motohours
      # go_interval_list  - список, в который будем складывать значения интервалов для проведения форм
      go_interval_list = []
      while next_go_interval < 27000:
        # если текущее значение next_go_interval не находится в temp_list (списке пропусков форм)
        # то добавляем значение в белый список
        if next_go_interval not in temp_list:
          go_interval_list.append(next_go_interval)
        # прибавляем к текущему значению next_go_interval значение периодичности interval_motohours
        next_go_interval = next_go_interval + interval_motohours
 
        
      temp_list = [str(i) for i in temp_list]
      temp_string = ";".join(temp_list)  
      maintanance_job_list_general.loc[index, ['pass_interval']] = temp_string

      go_interval_list = [str(i) for i in go_interval_list]
      go_interval_list_string = ";".join(go_interval_list)  
      maintanance_job_list_general.loc[index, ['go_interval']] = go_interval_list_string
    else:
      maintanance_job_list_general.loc[index, ['go_interval']] = 'not'
      

  maintanance_job_list_general.to_csv('data/maintanance_job_list_general.csv', index=False)
      
       


pass_interval_fill()  


# справочник работ eo_job_catologue
def eo_job_catologue():
  '''создание файла eo_job_catologue: список оборудование - работа на оборудовании'''
  # Джойним список машин из full_eo_list c планом ТО из maintanance_job_list_general
  maintanance_job_list_general_df = pd.read_csv('data/maintanance_job_list_general.csv', dtype = str)
  maintanance_job_list_general_df = maintanance_job_list_general_df.astype({'downtime_planned': float})
  maintanance_job_list_general_df.rename(columns={'upper_level_tehmesto_code': 'level_upper'}, inplace=True)
  eo_maintanance_plan_df = pd.merge(full_eo_list, maintanance_job_list_general_df, on = 'level_upper', how='inner')
  
  # удаляем строки, в которых нет данных в колонке eo_main_class_code
  eo_maintanance_plan_df = eo_maintanance_plan_df.loc[eo_maintanance_plan_df['eo_main_class_code'] != 'no_data']

  # получаем первую букву в поле eo_class_code
  eo_maintanance_plan_df['check_S_eo_class_code'] = eo_maintanance_plan_df['eo_class_code'].astype(str).str[0]
  eo_maintanance_plan_df = eo_maintanance_plan_df.loc[eo_maintanance_plan_df['check_S_eo_class_code'] != 'S']
  


  eo_maintanance_plan_df['eo_maintanance_job_code'] = eo_maintanance_plan_df['eo_code'] + '_' + eo_maintanance_plan_df['maintanance_code_id']
  eo_maintanance_plan_df = eo_maintanance_plan_df.loc[:, ['eo_maintanance_job_code','maintanance_code','eo_code', 'eo_main_class_code','eo_description', 'maintanance_name', 'interval_motohours','downtime_planned','pass_interval','go_interval', 'operation_start_date']].reset_index(drop=True)
  # eo_maintanance_plan_df['last_maintanance_date'] = '31.12.2022'
  eo_maintanance_job_code_last_date = pd.read_csv('data/eo_maintanance_job_code_last_date.csv')
  eo_maintanance_plan_last_date_df = pd.merge(eo_maintanance_plan_df, eo_maintanance_job_code_last_date, on = 'eo_maintanance_job_code', how = 'left')
  
  
  eo_maintanance_plan_df.to_csv('data/eo_job_catologue.csv', index=False)
  return eo_maintanance_plan_df
eo_job_catologue()



# maintanance_eo_list_start_date_df_prepare()
# Приклеивааем полученные даты последнего ТО
def maintanance_jobs_df_prepare():
  '''подготовка файла со списком работ - основной файл для построения графика простоев'''
  #eo_maintanance_plan_update_start_date_df = maintanance_eo_list_start_date_df_prepare()
  #eo_maintanance_plan_update_start_date_df.drop(columns=['last_maintanance_date'], inplace=True)
  
  #eo_maint_plan_with_last_dates = pd.read_csv('data/eo_maintanance_plan_with_start_date_df.csv', dtype = str)
  #eo_maint_plan_with_last_dates = eo_maint_plan_with_last_dates.loc[:, ['eo_maintanance_job_code', 'last_maintanance_date']]
  #eo_maint_plan = pd.merge(eo_maintanance_plan_update_start_date_df, eo_maint_plan_with_last_dates, on='eo_maintanance_job_code', how='left')
  # читаем файл eo_job_catologue
  eo_maint_plan = pd.read_csv('data/eo_job_catologue.csv', dtype = str)
  eo_maint_plan["downtime_planned"] = eo_maint_plan["downtime_planned"].astype('float')
  
  # читаем файл с датой проведения последней формы на машине. Исходим из того, что все даты должны быть записаны в этом файле
  eo_maintanance_job_code_last_date = pd.read_csv('data/eo_maintanance_job_code_last_date.csv', dtype = str)

  # джойним eo_job_catologue с датами проведения последней формы
  eo_maint_plan_with_dates = pd.merge(eo_maint_plan, eo_maintanance_job_code_last_date, on = 'eo_maintanance_job_code', how = 'left')

  # выдергиваем из full_eo_list колонки, которые нужны
  full_eo_list_selected = full_eo_list.loc[:, ['eo_code', 'avearage_day_operation_hours']]
  # джойним с full_eo_list
  eo_maint_plan_with_dates_with_full_eo_list = pd.merge(eo_maint_plan_with_dates, full_eo_list_selected, on = 'eo_code', how = 'left')
  eo_maint_plan = eo_maint_plan_with_dates_with_full_eo_list

  eo_maint_plan.to_csv('data/eo_maint_plan_delete.csv')
  # в maintanance_jobs_result_list будем складывать дикты с записями о сгенерированных ТО-шках.
  maintanance_jobs_result_list = []

  for index, row in eo_maint_plan.iterrows():
    maintanance_job_code = row['eo_maintanance_job_code']
    eo_code = row['eo_code']
    standard_interval_motohours = float(row['interval_motohours'])
    plan_downtime = row['downtime_planned']
    start_point = row['last_maintanance_date']
    operation_start_date = row['operation_start_date']
    avearage_day_operation_hours = float(row['avearage_day_operation_hours'])
    maintanance_name = row['maintanance_name']
    pass_interval = row['pass_interval']
    go_interval = row['go_interval']
    
    # start_point = pd.to_datetime(start_point, format='%Y-%m-%d')
    start_point = pd.to_datetime(start_point, format='%d.%m.%Y')
 
    maintanance_datetime = start_point
  
    # если это ежедневное обслуживание, то расставляем через каждые 24 часа
    if maintanance_name == 'ЕТО':
    
      while maintanance_datetime < last_day_of_selection:
        temp_dict = {}
        temp_dict['maintanance_job_code'] = maintanance_job_code
        temp_dict['eo_code'] = eo_code
        temp_dict['interval_motohours'] = standard_interval_motohours
        temp_dict['dowtime_plan, hours'] = plan_downtime
        temp_dict['maintanance_datetime'] = maintanance_datetime
        temp_dict['maintanance_date'] = maintanance_datetime.date()
        temp_dict['maintanance_name'] = maintanance_name
        # temp_dict['avearage_day_operation_hours'] = avearage_day_operation_hours
        
        maintanance_datetime = maintanance_datetime + timedelta(hours=24)
        maintanance_jobs_result_list.append(temp_dict)
        temp_dict = {}
    # если у формы нет поглащений другими формами, то расставляем через каждый интервал между формами
    elif maintanance_name != 'ЕТО' and pass_interval == 'not':
    
      while maintanance_datetime < last_day_of_selection:
        temp_dict = {}
        temp_dict['maintanance_job_code'] = maintanance_job_code
        temp_dict['eo_code'] = eo_code
        temp_dict['interval_motohours'] = standard_interval_motohours
        temp_dict['dowtime_plan, hours'] = plan_downtime
        temp_dict['maintanance_datetime'] = maintanance_datetime
        temp_dict['maintanance_date'] = maintanance_datetime.date()
        temp_dict['maintanance_name'] = maintanance_name
        
        # количество суток, которые требуются для того, чтобы выработать интервал до следующей формы
        number_of_days_to_next_maint = standard_interval_motohours // avearage_day_operation_hours
        # остаток часов в следующие сутки для выработки интервала до следующей формы
        remaining_hours = standard_interval_motohours - number_of_days_to_next_maint * avearage_day_operation_hours
        # календарный интервал между формами = кол-во суток х 24 + остаток
        calendar_interval_between_maint = number_of_days_to_next_maint *24 + remaining_hours
        maintanance_datetime = maintanance_datetime + timedelta(hours=calendar_interval_between_maint) + timedelta(hours = plan_downtime)
        maintanance_jobs_result_list.append(temp_dict)
        temp_dict = {}
        
    # остаются записи, которые не ЕТО, и у которых есть поглащения форм.
    # для таких записей итерируемся по списку 'go interval'
    elif go_interval != 'not': 
      go_interval_list = go_interval.split(';')
      go_interval_list = [int(i) for i in go_interval_list]
      
      # base_start_maintanance_datetime - это дата к которой будем прибавлять все интервалы из цикла периодов
      base_start_maintanance_datetime = start_point
      
      # итерируемся по списку go_interval
      for maintanance_interval_temp in go_interval_list:
        # количество суток, которые требуются для того, чтобы выработать интервал до следующей формы
        number_of_days_to_next_maint = maintanance_interval_temp // avearage_day_operation_hours
     
        # остаток часов в следующие сутки для выработки интервала до следующей формы
        remaining_hours = maintanance_interval_temp - number_of_days_to_next_maint * avearage_day_operation_hours
     
        # календарный интервал между формами = кол-во суток х 24 + остаток
        calendar_interval_between_maint = number_of_days_to_next_maint *24 + remaining_hours
        
        maintanance_datetime = base_start_maintanance_datetime + timedelta(hours=calendar_interval_between_maint) + timedelta(hours = plan_downtime)
       
        temp_dict = {}
        temp_dict['maintanance_job_code'] = maintanance_job_code
        temp_dict['eo_code'] = eo_code
        temp_dict['interval_motohours'] = standard_interval_motohours
        temp_dict['dowtime_plan, hours'] = plan_downtime
        temp_dict['maintanance_name'] = maintanance_name
        temp_dict['maintanance_datetime'] = maintanance_datetime
        temp_dict['maintanance_date'] = maintanance_datetime.date()
        temp_dict['maint_interval'] =  maintanance_interval_temp
        temp_dict['pass_interval_list'] = pass_interval
        temp_dict['go_interval_list'] = go_interval
        maintanance_jobs_result_list.append(temp_dict)

      
          
  maintanance_jobs_df = pd.DataFrame(maintanance_jobs_result_list)
  # maintanance_jobs_df['maintanance_date'] = maintanance_jobs_df['maintanance_date'].astype(str)

  maintanance_jobs_df.to_csv('data/maintanance_jobs_df.csv')

  return maintanance_jobs_df
maintanance_jobs_df_prepare()
 

# заполняем календарный фонд по оборудованию
# берем машины, кооторые участвуют в файле eo_job_catologue.csv
def fill_calendar_fond():
  eo_list_under_maintanance_program = pd.read_csv('data/eo_job_catologue.csv', dtype = str)
  # new data frame with split value columns
  # new = eo_list_under_maintanance_program['eo_code'].str.split(".", n = 1, expand = True)
  # making separate first name column from new data frame
  # eo_list_under_maintanance_program["eo_code"]= new[0]
  
  eo_list = eo_list_under_maintanance_program['eo_code'].unique()
  
  result_list = []
  # итерируемся по списку еo
  for eo in eo_list:
    maint_date = first_day_of_selection
    while maint_date < last_day_of_selection:
      temp_dict = {}
      temp_dict['eo_code'] = eo
      temp_dict['datetime'] = maint_date
      temp_dict['calendar_fond'] = 24 
      result_list.append(temp_dict)
      maint_date = maint_date + timedelta(hours=24)

  eo_calendar_fond = pd.DataFrame(result_list)
  eo_calendar_fond.to_csv('data/eo_calendar_fond.csv')

fill_calendar_fond()





def maintanance_matrix():
  maintanance_jobs_df = maintanance_jobs_df_prepare()
  
  first_date = first_day_of_selection.date()
  last_date = last_day_of_selection.date()
  date_list = []
  current_date = first_date
  while current_date <= last_date:
    date_list.append(current_date)
    current_date = current_date + timedelta(hours=24)
  
  eo_maint_unique_list = maintanance_jobs_df['maintanance_job_code'].unique()
  eo_list = []
  maintanance_job_code_list = []
  for record in eo_maint_unique_list:
    record1 = record.split('_')[0]
    maintanance_job_code_list.append(record)
    eo_list.append(record1)
  
  df = pd.DataFrame({'maintanance_job_code':maintanance_job_code_list, 'eo_code': eo_list})  
  eo_selected_data = full_eo_list.loc[:, ['eo_code','eo_description', 'eo_main_description', 'level_1','level_upper', 'avearage_day_operation_hours']]
  level_1_df = pd.read_csv('data/level_1.csv')
  eo_selected_data_with_description = pd.merge(eo_selected_data, level_1_df, on = 'level_1', how = 'left')
  # level_upper_df = pd.read_csv('data/level_upper.csv')
  # eo_selected_data_with_description_1 = pd.merge(eo_selected_data_with_description, level_1_df, on = 'level_upper', how = 'left')
  
  df1 = pd.merge(df, eo_selected_data_with_description, on = 'eo_code', how = 'left') 
  
 
  

  # making separate first name column from new data frame
  # eo_list_under_maintanance_program["eo_code"]= new[0]

  temp_df = pd.DataFrame({'maintanance_job_code': eo_maint_unique_list})
  temp_df_1 = pd.merge(temp_df, maintanance_jobs_df, on = 'maintanance_job_code', how = 'left')
  temp_df = temp_df_1.loc[:, ['maintanance_job_code', 'maintanance_name']]

  # matrix_df = pd.DataFrame(index = eo_maint_unique_list, columns = date_list).fillna(0)
  matrix_df_0 = pd.DataFrame(columns = date_list)
  matrix_df = pd.concat([temp_df, matrix_df_0 ], axis=1).fillna(0)

  # удаляем из maintanance_jobs_df записи раньше 2023 года
  maintanance_jobs_df = maintanance_jobs_df.loc[maintanance_jobs_df['maintanance_datetime'] >= first_day_of_selection]
  for index, row in matrix_df.iterrows():
    # режем таблицу со списком по текущему индексу, который есть работах
    maintanance_job_code = row['maintanance_job_code']
    temp_df = maintanance_jobs_df.loc[maintanance_jobs_df['maintanance_job_code'] == maintanance_job_code]
    for index_temp_df, row_temp_df in temp_df.iterrows():
      temp_date = row_temp_df['maintanance_date']
      downtime = row_temp_df['dowtime_plan, hours']
      matrix_df.loc[index, temp_date] = downtime 

  matrix_data_df = pd.merge(df1, matrix_df, on = 'maintanance_job_code', how ='left')

  matrix_data_df.to_csv('data/matrix_data_df.csv')


# maintanance_matrix()

def checklist_main_eo_class_options(df):
  '''подготовка данных для фильтра по main_eo_class'''
  
  join_eo_and_full_eo_df = pd.merge(df, full_eo_list, on='eo_code', how = 'left')
  
  join_eo_and_full_eo_df = join_eo_and_full_eo_df.loc[:, ['level_upper']]
  

  level_upper_unique_df = pd.DataFrame(join_eo_and_full_eo_df['level_upper'].unique(), columns=['level_upper'], dtype = str)
  

  level_upper_df = pd.read_csv('data/level_upper.csv', dtype = str)
  level_upper__df = pd.merge(level_upper_unique_df, level_upper_df, on='level_upper', how = 'left')

  level_upper_checklist_data = []
  level_upper_list = []
  for index, row in level_upper__df.iterrows():
      dict_temp = {}
      dict_temp['label'] = row['Название технического места']
      dict_temp['value'] = row['level_upper']
      level_upper_checklist_data.append(dict_temp)

      level_upper_list.append(row['level_upper'])
  
  return level_upper_checklist_data, level_upper_list




def eo_checklist_data(df):
    '''подготовка данных для фильтра по машинам'''
    eo_list_unique = pd.DataFrame(df['eo_code'].unique(), columns=['eo_code'], dtype = str)
    eo_list = pd.merge(eo_list_unique, full_eo_list, on='eo_code', how = 'left')
    eo_list_df = eo_list.loc[:, ['eo_code', 'eo_description']]
    
    # eo_list_df.sort_values('eo_description', inplace=True)
    
    eo_checklist_data = []
    eo_list = []
    for index, row in eo_list_df.iterrows():
        dict_temp = {}
        dict_temp['label'] = " " + row['eo_code'] + "_" + row['eo_description']
        dict_temp['value'] = row['eo_code']
        eo_checklist_data.append(dict_temp)
        eo_list.append(row['eo_code'])
    
    return eo_checklist_data, eo_list


# python functions.py
