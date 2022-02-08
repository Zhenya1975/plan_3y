import pandas as pd
from datetime import timedelta
import datetime


"""датафрейм с протянутыми датами"""

# даты начала и конца трехлетнего периода
first_day_of_selection = pd.to_datetime('01.01.2023', format='%d.%m.%Y')
last_day_of_selection = pd.to_datetime('01.01.2026', format='%d.%m.%Y')

# plan_dates_df - список дат в трехлетнем диапазоне
plan_dates_df = pd.DataFrame([first_day_of_selection+timedelta(days=x) for x in range((last_day_of_selection-first_day_of_selection).days)], columns=['plan_date'])
plan_dates_df['plan_date'] = plan_dates_df['plan_date'].dt.date
plan_dates_df['plan_date'] = plan_dates_df['plan_date'].astype('str')

# print(plan_dates_df.info())
# plan_dates_df['plan_date'] = plan_dates_df['plan_date'].astype("str")

eo_list = pd.read_csv('data/eo_list.csv')

index_list = []
for index in range(len(eo_list)):
  index_list.append(index)


# plan_df - пустой датафрейм с индексом, колонками - датами и заполненными нулями
plan_df = pd.DataFrame(index = index_list, columns = plan_dates_df['plan_date']).fillna(0)

# в пустой датафрейм добавляем данные о машинах
maintanence_chart_df = pd.concat([eo_list, plan_df], axis=1)

maintanence_chart_df.to_csv('data/maintanence_chart.csv')

# создаем записи о работах
last_day_of_selection = pd.to_datetime('01.01.2026', format='%d.%m.%Y')

maint_job_list = pd.read_csv('data/maintanance_job_list.csv')
maint_job_list['dowtime_plan, hours'] = maint_job_list['dowtime_plan, hours'].str.replace(",", ".").astype("float")
#  даты - в даты
date_column_list = ['last_job_in_previous_period_date']

for date_column in date_column_list:
  maint_job_list.loc[:, date_column] = pd.to_datetime(maint_job_list[date_column], infer_datetime_format=True, format='%d.%m.%Y')
  # maint_job_list.loc[:, date_column] = maint_job_list.loc[:, date_column].apply(lambda x: datetime.date(x.year,x.month, x.day))
# сортируем по колонке close_event
maint_job_list.sort_values(['last_job_in_previous_period_date'], inplace=True)

# в maintanance_jobs_result_list будем складывать дикты с записями о сгенерированных ТО-шках.
maintanance_jobs_result_list = []
for index, row in maint_job_list.iterrows():
  maintanance_datetime_list = []
  maintanance_job_code = row['maintanance_job_code']
  eo_code = row['eo_code']
  interval_motohours = row['interval_motohours']
  plan_downtime = row['dowtime_plan, hours']
  start_point = row['last_job_in_previous_period_date']

  next_maintanance_datetime = start_point

  while next_maintanance_datetime < last_day_of_selection:
    temp_dict = {}
    next_maintanance_datetime = next_maintanance_datetime + timedelta(hours=interval_motohours) + timedelta(hours = plan_downtime)
    temp_dict['maintanance_job_code'] = maintanance_job_code
    temp_dict['eo_code'] = eo_code
    temp_dict['interval_motohours'] = interval_motohours
    temp_dict['dowtime_plan, hours'] = plan_downtime
    temp_dict['maintanance_datetime'] = next_maintanance_datetime
    temp_dict['maintanance_date'] = next_maintanance_datetime.date()
    maintanance_jobs_result_list.append(temp_dict)
  
maintanance_jobs_df = pd.DataFrame(maintanance_jobs_result_list)
maintanance_jobs_df['maintanance_date'] = maintanance_jobs_df['maintanance_date'].astype(str)
  # maint_job_list.loc[index, 'next_maintanance'] = maintanance_datetime_list

maintanance_jobs_df.to_csv('data/maintanance_jobs_df.csv')

# нужно заджойнить запланированный список работ maintanance_jobs_df и матрицу с датами
maintanance_job_list = pd.read_csv('data/maintanance_job_list.csv')
maintanance_matrix = pd.merge(maintanance_job_list, maintanence_chart_df, on = 'eo_code', how = 'left')

# заполяняем матрицу
for index, row in maintanance_matrix.iterrows():
  maintanance_code = row['maintanance_job_code']
  eo_code = row['eo_code']
  # фильтруем списоку работ по текущему коду
  maintanance_jobs = maintanance_jobs_df.loc[maintanance_jobs_df['maintanance_job_code'] == maintanance_code] 
  
  # итерируемся по списку работ
  for index_jobs, row_jobs in  maintanance_jobs.iterrows():
    downtime_plan_hours = row_jobs['dowtime_plan, hours']
    maintanance_date = row_jobs['maintanance_date']
    maintanance_matrix = maintanance_matrix.copy()
    maintanance_matrix.loc[index, maintanance_date] = downtime_plan_hours

maintanance_matrix.to_csv('data/maintanance_matrix.csv')


# python functions.py
