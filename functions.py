import pandas as pd
from datetime import timedelta
import datetime
import initial_values

full_eo_list = pd.read_csv('data/full_eo_list.csv', dtype = str)
full_eo_list['avearage_day_operation_hours'] = 23.5
# даты начала и конца трехлетнего периода
first_day_of_selection = pd.to_datetime('01.01.2023', format='%d.%m.%Y')
last_day_of_selection = pd.to_datetime('01.01.2026', format='%d.%m.%Y')


# при получении внешнего excel maintanance_job_list_general проверяем - есть ли в полученном файле ноые записи.
# Если есть, то обновляем файл
def check_maintanance_job_list_general_file(df):
  # сначала получаем то, что у нас уже сохранено.
  maintanance_job_list_general_old = pd.read_csv('data/maintanance_job_list_general.csv', dtype = str)
  maintanance_job_list_general_old = maintanance_job_list_general_old.astype({'downtime_planned': float})

  # получаем новый файл
  maintanance_job_list_general_new = df.astype({'downtime_planned': float})

  # maintanance_job_list_general_new.to_csv('data/maintanance_job_list_general_new_delete.csv')

  maintanance_job_list_general_updated = maintanance_job_list_general_new
  return maintanance_job_list_general_updated


# справочник работ eo_job_catologue
def eo_job_catologue():
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

  # eo_maintanance_plan_df.to_csv('data/eo_maintanance_plan_df_delete.csv')

  eo_maintanance_plan_df['eo_maintanance_job_code'] = eo_maintanance_plan_df['eo_code'] + '_' + eo_maintanance_plan_df['maintanance_code_id']
  eo_maintanance_plan_df = eo_maintanance_plan_df.loc[:, ['eo_maintanance_job_code','maintanance_code','eo_code', 'eo_main_class_code','eo_description', 'maintanance_name', 'interval_motohours', 'downtime_planned']].reset_index(drop=True)
  # eo_maintanance_plan_df['last_maintanance_date'] = '31.12.2022'
  eo_maintanance_job_code_last_date = pd.read_csv('data/eo_maintanance_job_code_last_date.csv')
  eo_maintanance_plan_last_date_df = pd.merge(eo_maintanance_plan_df, eo_maintanance_job_code_last_date, on = 'eo_maintanance_job_code', how = 'left')
  
  # eo_maintanance_plan_last_date_df.to_csv('data/eo_maintanance_plan_last_date_df_delete.csv')    
  eo_maintanance_plan_df.to_csv('data/eo_job_catologue.csv', index=False)
  return eo_maintanance_plan_df
eo_job_catologue()



# maintanance_eo_list_start_date_df_prepare()
# Приклеивааем полученные даты последнего ТО
def eo_maintanance_plan_df_phase_2():
  eo_maintanance_plan_update_start_date_df = maintanance_eo_list_start_date_df_prepare()
  eo_maintanance_plan_update_start_date_df.drop(columns=['last_maintanance_date'], inplace=True)
  
  eo_maint_plan_with_last_dates = pd.read_csv('data/eo_maintanance_plan_with_start_date_df.csv', dtype = str)
  eo_maint_plan_with_last_dates = eo_maint_plan_with_last_dates.loc[:, ['eo_maintanance_job_code', 'last_maintanance_date']]
  eo_maint_plan = pd.merge(eo_maintanance_plan_update_start_date_df, eo_maint_plan_with_last_dates, on='eo_maintanance_job_code', how='left')
  
  eo_maint_plan["dowtime_plan, hours"] = eo_maint_plan["dowtime_plan, hours"].astype('float')
  eo_maint_plan.to_csv('data/eo_maint_plan_delete.csv')
  # в maintanance_jobs_result_list будем складывать дикты с записями о сгенерированных ТО-шках.
  maintanance_jobs_result_list = []
  for index, row in eo_maint_plan.iterrows():
    maintanance_job_code = row['eo_maintanance_job_code']
    eo_code = row['eo_code']
    interval_motohours = float(row['interval_motohours'])
    plan_downtime = row['dowtime_plan, hours']
    start_point = row['last_maintanance_date']
    avearage_day_operation_hours = float(row['avearage_day_operation_hours'])
    maintanance_name = row['maintanance_name']

    start_point = pd.to_datetime(start_point, format='%Y-%m-%d')
    # print(type(start_point))
    next_maintanance_datetime = start_point
    # print('interval_motohours: ', type(interval_motohours))
    # если это ежедневное обслуживание
    if maintanance_name == 'ЕТО':
      while next_maintanance_datetime < last_day_of_selection:
        temp_dict = {}
        temp_dict['maintanance_job_code'] = maintanance_job_code
        temp_dict['eo_code'] = eo_code
        temp_dict['interval_motohours'] = interval_motohours
        temp_dict['dowtime_plan, hours'] = plan_downtime
        temp_dict['maintanance_datetime'] = next_maintanance_datetime
        temp_dict['maintanance_date'] = next_maintanance_datetime.date()
        temp_dict['maintanance_name'] = maintanance_name
        # temp_dict['avearage_day_operation_hours'] = avearage_day_operation_hours
        maintanance_jobs_result_list.append(temp_dict)
        next_maintanance_datetime = next_maintanance_datetime + timedelta(hours=24)
    # для остальных надо посчитать помент начала следующей работы
    else:
      while next_maintanance_datetime < last_day_of_selection:
        temp_dict = {}
        temp_dict['maintanance_job_code'] = maintanance_job_code
        temp_dict['eo_code'] = eo_code
        temp_dict['interval_motohours'] = interval_motohours
        temp_dict['dowtime_plan, hours'] = plan_downtime
        temp_dict['maintanance_datetime'] = next_maintanance_datetime
        temp_dict['maintanance_date'] = next_maintanance_datetime.date()
        temp_dict['maintanance_name'] = maintanance_name
        maintanance_jobs_result_list.append(temp_dict)    
        
        # количество суток, которые требуются для того, чтобы выработать интервал до следующей формы
        number_of_days_to_next_maint = interval_motohours // avearage_day_operation_hours
        # остаток часов в следующие сутки для выработки интервала до следующей формы
        remaining_hours = interval_motohours - number_of_days_to_next_maint * avearage_day_operation_hours
        # календарный интервал между формами = кол-во суток х 24 + остаток
        calendar_interval_between_maint = number_of_days_to_next_maint *24 + remaining_hours
        next_maintanance_datetime = next_maintanance_datetime + timedelta(hours=calendar_interval_between_maint) 
        

  maintanance_jobs_df = pd.DataFrame(maintanance_jobs_result_list)
  # maintanance_jobs_df['maintanance_date'] = maintanance_jobs_df['maintanance_date'].astype(str)

  maintanance_jobs_df.to_csv('data/maintanance_jobs_df.csv')
  return maintanance_jobs_df
# eo_maintanance_plan_df_phase_2()
 

# заполняем календарный фонд по оборудованию
# берем машины, кооторые участвуют в файле eo_maintanance_plan_with_start_date_df.csv
def fill_calendar_fond():
  eo_list_under_maintanance_program = pd.read_csv('data/eo_maintanance_plan_with_start_date_df.csv', dtype = str)
  # new data frame with split value columns
  new = eo_list_under_maintanance_program['eo_code'].str.split(".", n = 1, expand = True)
  # making separate first name column from new data frame
  eo_list_under_maintanance_program["eo_code"]= new[0]
  
  eo_list = eo_list_under_maintanance_program['eo_code'].unique()
  
  first_day_of_selection
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
  # print(eo_list)
# fill_calendar_fond()


# матрица по датам 
# EO - тип работы  - и вправо в даты суммируем простои по дням.
# затем джойнами доплним данные о машине и работах
def maintanance_matrix():
  maintanance_jobs_df = eo_maintanance_plan_df_phase_2()
  # заполняем колонки датами
  # итерируемся по maintanance_jobs_df
  matrix_result_list = []
  for index, row in maintanance_jobs_df.iterrows():
    eo_code = row['eo_code']
    maintanance_job_code = row['maintanance_job_code']
    maintanance_date = row['maintanance_date']
    

  
  first_day_of_selection = initial_values.first_day_of_selection
  last_day_of_selection_date = initial_values.last_day_of_selection

  
  calendar_date = first_day_of_selection
  date_list = []
  month_list = []
  year_list = []
  while calendar_date < last_day_of_selection_date:
    date_cal = calendar_date.date()
    month_cal = calendar_date.month
    year_cal = calendar_date.year
    date_list.append(date_cal)
    month_list.append(month_cal)
    year_list.append(year_cal) 
    calendar_date = calendar_date + timedelta(hours=24)
  matrix_df = pd.DataFrame(columns = date_list).fillna(0)
  
  # new_df = pd.concat([maintanance_jobs_df, matrix_df], axis=1).fillna(0)
 

  

def maintanance_matrix():
  maintanance_jobs_df = eo_maintanance_plan_df_phase_2()
  # print(maintanance_jobs_df.info())
  first_date = first_day_of_selection.date()
  last_date = last_day_of_selection.date()
  date_list = []
  current_date = first_date
  while current_date <= last_date:
    date_list.append(current_date)
    current_date = current_date + timedelta(hours=24)
  
  eo_maint_unique_list = maintanance_jobs_df['maintanance_job_code'].unique()
  
  matrix_df = pd.DataFrame(index = eo_maint_unique_list, columns = date_list).fillna(0)
  # удаляем из maintanance_jobs_df записи раньше 2023 года
  maintanance_jobs_df = maintanance_jobs_df.loc[maintanance_jobs_df['maintanance_datetime'] >= first_day_of_selection]
  for maintanance_job_code, row in matrix_df.iterrows():
    # режем таблицу со списком по текущему индексу, который есть работах
    temp_df = maintanance_jobs_df.loc[maintanance_jobs_df['maintanance_job_code'] == maintanance_job_code]
    for index_temp_df, row_temp_df in temp_df.iterrows():
      temp_date = row_temp_df['maintanance_date']
      downtime = row_temp_df['dowtime_plan, hours']
      matrix_df.loc[maintanance_job_code, temp_date] = downtime 



  matrix_df.to_csv('data/matrix_df.csv')

  # result_list = []
  #for index, row in maintanance_jobs_df.iterrows():
  #  maintanance_job_code = row['maintanance_job_code']
  #  eo_code = row['eo_code']
  #  dowtime_plan = row['dowtime_plan, hours']
  #  interval_motohours = row['interval_motohours']
  #  maintanance_datetime = row['maintanance_datetime']
  #  maintanance_date = row['maintanance_date']
  #  maintanance_name = row['maintanance_name']
  #  temp_dict = {}
  #  temp_dict['maintanance_job_code'] = maintanance_job_code
    # maintanance_jobs_df = maintanance_jobs_df.copy()
    # maintanance_jobs_df.loc[index, maintanance_date] = dowtime_plan
    # result_list.append(temp_dict)
  
  # df = pd.DataFrame(result_list)
  # df.to_csv('data/df.csv')



#maintanance_matrix()


# нужно заджойнить запланированный список работ maintanance_jobs_df и матрицу с датами
#maintanance_job_list = pd.read_csv('data/maintanance_job_list.csv')
#maintanance_matrix = pd.merge(maintanance_job_list, maintanence_chart_df, on = 'eo_code', how = 'left')

# заполяняем матрицу
#for index, row in maintanance_matrix.iterrows():
#  maintanance_code = row['maintanance_job_code']
#  eo_code = row['eo_code']
  # фильтруем списоку работ по текущему коду
#  maintanance_jobs = maintanance_jobs_df.loc[maintanance_jobs_df['maintanance_job_code'] == maintanance_code] 
  
  # итерируемся по списку работ
 # for index_jobs, row_jobs in  maintanance_jobs.iterrows():
 #   downtime_plan_hours = row_jobs['dowtime_plan, hours']
 #   maintanance_date = row_jobs['maintanance_date']
 #   maintanance_matrix = maintanance_matrix.copy()
 #   maintanance_matrix.loc[index, maintanance_date] = downtime_plan_hours

# maintanance_matrix.to_csv('data/maintanance_matrix.csv')


# python functions.py
