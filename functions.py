import pandas as pd
from datetime import timedelta
import datetime


full_eo_list = pd.read_csv('data/full_eo_list.csv', dtype = str)
full_eo_list['avearage_day_operation_hours'] = 23.5
# даты начала и конца трехлетнего периода
first_day_of_selection = pd.to_datetime('01.01.2023', format='%d.%m.%Y')
last_day_of_selection = pd.to_datetime('01.01.2026', format='%d.%m.%Y')


def maintanance_eo_list_start_date_df_prepare():
  """ maintanance_eo_list_df - записи о работах, проводимых на машинах в соответствии с регламентом """
  # Джойним список машин из full_eo_list c планом ТО из maintanance_job_list_general
  maintanance_job_list_general_df = pd.read_csv('data/maintanance_job_list_general.csv', dtype = str)
  maintanance_job_list_general_df.rename(columns={'upper_level_tehmesto_code': 'level_upper'}, inplace=True)
  
  eo_maintanance_plan_df = pd.merge(full_eo_list, maintanance_job_list_general_df, on = 'level_upper', how='inner')
  # удаляем строки, в которых нет данных в колонке eo_main_class_code
  eo_maintanance_plan_df = eo_maintanance_plan_df.loc[eo_maintanance_plan_df['eo_main_class_code'] != 'no_data']

  # для того чтобы можно было заполнить таблицу с датами проведения работ, нужнно получить даты, с которых будем стартовать.
  # оттдаем на выгрузку эксель для ввода дат
  eo_maintanance_plan_df['eo_maintanance_job_code'] = eo_maintanance_plan_df['eo_code'] + '_' + eo_maintanance_plan_df['maintanance_code']
  # eo_maintanance_plan_df.to_csv('data/eo_maintanance_plan_df_delete.csv')
  eo_maintanance_plan_update_start_date_df = eo_maintanance_plan_df.loc[:, ['eo_maintanance_job_code','eo_code', 'eo_description', 'maintanance_name', 'interval_motohours', 'dowtime_plan, hours', 'avearage_day_operation_hours']]
  eo_maintanance_plan_update_start_date_df['last_maintanance_date'] = ''
  eo_maintanance_plan_update_start_date_df.to_csv('data/eo_maintanance_plan_update_start_date_df.csv', index=False)
  
  return eo_maintanance_plan_update_start_date_df
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
      temp_dict['eo'] = eo
      temp_dict['datetime'] = maint_date
      temp_dict['calendar_fond'] = 24 
      result_list.append(temp_dict)
      maint_date = maint_date + timedelta(hours=24)

  eo_calendar_fond = pd.DataFrame(result_list)
  eo_calendar_fond.to_csv('data/eo_calendar_fond.csv')
  # print(eo_list)
fill_calendar_fond()




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
