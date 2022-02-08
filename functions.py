import pandas as pd
from datetime import timedelta


# создаем датафрейм с протянутыми датами
first_day_of_selection = pd.to_datetime('01.01.2023', format='%d.%m.%Y')
last_day_of_selection = pd.to_datetime('01.01.2026', format='%d.%m.%Y')


# def quarter_all_dates_prepare(first_day_of_selection, last_day_of_selection):
"""список всех дней квартала с полем qty = 0. Заготовка для построения графика факта"""

plan_dates_df = pd.DataFrame([first_day_of_selection+timedelta(days=x) for x in range((last_day_of_selection-first_day_of_selection).days)], columns=['plan_date'])

eo_list = pd.read_csv('data/eo_list.csv')
# result_df['zero_qty'] = 0

# df = result_df.pivot_table(index=eo_list['ЕО код'], columns=['plan_date']).fillna(0)
index_list = []
for index in range(len(eo_list)):
  index_list.append(index)

plan_df = pd.DataFrame(index = index_list, columns = plan_dates_df['plan_date']).fillna(0)
# plan_df.fillna(0)

result_df = pd.concat([eo_list, plan_df], axis=1)

result_df.to_csv('data/result_df_delete.csv')
  

