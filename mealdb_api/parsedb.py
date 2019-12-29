import mealdb_api.api_dict as db
from mealdb_api.call_api_to_df import create_df
import pandas as pd

df = pd.DataFrame()
for i in range(52600, 53000):
    a = db.lookupmeal(i)
    b = create_df(a)
    if b is not None:
        df = df.append(b)
    print(i)

df.to_csv('/Users/nilsseitz/Coding/Conda/pycuisine/data/data_backup.csv')



