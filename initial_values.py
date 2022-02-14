import pandas as pd

full_eo_list = pd.read_csv('data/full_eo_list.csv', dtype = str)


first_day_of_selection = pd.to_datetime('01.01.2023', format='%d.%m.%Y')
last_day_of_selection = pd.to_datetime('01.01.2026', format='%d.%m.%Y')

# протягиваем в full eo list даты начала и конца эксплуатации. 
# сначала - просто протянем. Потом сможем обновлять
first_day_of_operation = pd.to_datetime('01.01.2020', format='%d.%m.%Y')
last_day_of_opearation = pd.to_datetime('01.01.2030', format='%d.%m.%Y')

def first_and_last_day_of_operation_default():
  full_eo_list = pd.read_csv('data/full_eo_list.csv', dtype = str)
  full_eo_list['first_day_of_operation'] = first_day_of_operation
  full_eo_list['last_day_of_opearation'] = last_day_of_opearation
  full_eo_list.to_csv('data/full_eo_list.csv')

# first_and_last_day_of_operation_default()

