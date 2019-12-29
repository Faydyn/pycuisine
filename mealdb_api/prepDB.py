import os

import mealdb_api.api_dict as db
import pandas as pd
from mealdb_api.call_api_to_df import create_df

path = os.path.dirname(os.path.abspath(__file__))
datapath = os.path.abspath(os.path.join(path, '..', 'src/main/resources/base'))


def getDB():
    df = pd.read_csv('/Users/nilsseitz/Coding/Conda/pycuisine/data/data_conved.csv')
    return df


def prepDB(df):
    df = df.fillna('')
    df
    ef = pd.DataFrame()
    ef['Name'] = df.loc[:, 'Meal']
    ef['Tags'] = df.loc[:, 'Category'].apply(lambda x: f'{x},' if x != '' else '') + df.loc[:, 'Area'].apply(
        lambda x: f'{x}, ' if x != '' else '') + df.loc[:, 'Tags']
    ef['Tags'] = ef['Tags'].apply(lambda x: ','.join(
        list(set([word.strip().lower().capitalize() for word in x.split(',') if word != 'Unknown']))))
    ef['Tags'] = ef['Tags'].apply(lambda x: str(x).replace(',,', ','))
    ef['Tags'] = ef['Tags'].apply(lambda x: x[1:] if x.startswith(',') else x)
    ef['Tags'] = ef['Tags'].apply(lambda x: x[:-1] if x.endswith(',') else x)
    ef['Ingredients'] = df.loc[:, 'Ingredients'].apply(lambda x: str(x).replace(',  ()', ''))
    ef['Recipe'] = df.loc[:, 'Instructions'] + df.loc[:, 'Youtube'].apply(
        lambda x: f'\n\n{x}' if x != '' else '') + df.loc[:, 'Source'].apply(lambda x: f'\n\n{x}' if x != '' else '')

    return ef


def saveDB(filepath):
    df = getDB()
    ef = prepDB(df)
    ef.to_csv(f'{filepath}/data.csv', index=False)


def saveCategory(filepath):
    a = create_df(db.listdb('c'))
    a = a.rename(columns={'strCategory': 'Category'})
    a.to_csv(f'{filepath}/category.csv', index=False)


def saveRegion(filepath):
    b = create_df(db.listdb('a'))
    b = b.rename(columns={'strArea': 'Region'})
    dropping_indices = [i for i in range(len(b)) if b.loc[i, 'Region'] == 'Unknown']
    for i in dropping_indices:
        b = b.drop(i)
    b.to_csv(f'{filepath}/region.csv', index=False)


def saveIngredients(filepath):
    c = create_df(db.listdb('i'))
    lst = ['strIngredient', 'strDescription']
    d = c.loc[:, lst]
    cols = [col for col in d.columns]
    d = d.rename(columns=dict(zip(cols, ['Ingredients', 'Description'])))
    d.to_csv(f'{filepath}/ingredients.csv', index=False)


def alltodata():
    saveDB(datapath)
    saveCategory(datapath)
    saveRegion(datapath)
    saveIngredients(datapath)


# alltodata()
