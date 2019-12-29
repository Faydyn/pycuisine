from random import randint
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit
import pandas as pd
import os
import sys


def lookup(dishname, from_main):
    df = getDB(from_main)
    dish = df[df['Name'] == dishname]
    dish = dish.reset_index(drop=True)
    return show_transposed(dish)


def show_transposed(dish):
    dish['Dish'] = list(dish.loc[:, 'Name'])
    dish = dish.drop('Tags', axis=1)

    all_ingres = list(dish['Ingredients'])

    ingres_lst = all_ingres[0].split(', ')
    for i, ing in enumerate(ingres_lst, 1):
        dish[f'Ingredient {i}'] = [ing]

    recipe = list(dish['Recipe'])
    recipe_lst = []
    maxlen = 150

    for part in recipe[0].split('\n'):
        size = len(part)
        if len(part) > maxlen:
            intervalls = size // maxlen + 1
            size_intervall = size // intervalls
            lstintervalls = list(range(size_intervall // 2, size - (size_intervall // 2), size_intervall))
            for k, v in enumerate(lstintervalls):
                for i, c in enumerate(part[v:], v):
                    if not c.isalnum():
                        lstintervalls[k] = i
                        break

            indices = [0] + lstintervalls + [size]
            for a, b in zip(indices[:-1], indices[1:]):
                recipe_lst.append(part[a:b])
        else:
            recipe_lst.append(part)

    for i, r in enumerate([r for r in recipe_lst if r.strip() != ''], 1):
        dish[f'Recipe - Part {i}'] = [r]

    dish = dish.drop(['Name', 'Ingredients', 'Recipe'], axis=1)
    return dish.T


def filterDB(terms, from_main):
    searchterms = [x for x in terms if x != x.upper()]
    excluds = [x for x in terms if x == x.upper()]
    df = getDB(from_main)
    colnames = list(df.columns)
    size = len(df)
    counts = dict(enumerate([0] * size))
    for i in range(size):
        for searchterm in searchterms:
            for name in colnames:
                if any([excls in (df.loc[i, name]).upper() for excls in excluds]):
                    break
                if searchterm in df.loc[i, name]:
                    counts[i] += 1

    sortedcounts = sorted(counts.items(), key=lambda kv: (kv[1], kv[0]))[::-1]
    relevance_index = [fst for fst, snd in sortedcounts if snd != 0]
    ef = df.loc[relevance_index]
    return ef


def getDB(from_appctxt, option='dat'):
    menu = {'dat': 'data', 'a': 'region', 'c': 'category', 'i': 'ingredients'}
    file = from_appctxt.get_resource(f'{menu.get(option)}.csv')
    df = pd.read_csv(file)
    df = df.fillna('')
    return df


def rndDB(from_main):  # template for search/filter etc
    df = getDB(from_main)
    x = randint(0, len(df))
    return show_transposed(df.loc[x:x])


class MainWindow(QWidget):
    def __init__(self, from_main):
        super().__init__()
        self.title = 'pycuisine'
        self.resize(180, 100)
        self.move(20, 100)
        self.main = from_main

        button = QPushButton('All')
        button.clicked.connect(self.on_pushButton_all)

        button2 = QPushButton('Random')
        button2.clicked.connect(self.on_pushButton_rnd)

        button3 = QPushButton('Tags (Region)')
        button3.clicked.connect(self.on_pushButton_region)

        button4 = QPushButton('Tags (Category)')
        button4.clicked.connect(self.on_pushButton_category)

        button5 = QPushButton('Ingredients')
        button5.clicked.connect(self.on_pushButton_ingredients)

        button6 = QPushButton('Search')
        button6.clicked.connect(self.on_pushButton_search)

        self.textbox = QLineEdit(self)

        button7 = QPushButton('Lookup')
        button7.clicked.connect(self.on_pushButton_lookup)

        self.pastebox = QLineEdit(self)

        layout = QVBoxLayout()

        layout.addWidget(button)
        layout.addWidget(button2)
        layout.addWidget(button3)
        layout.addWidget(button4)
        layout.addWidget(button5)
        layout.addWidget(self.textbox)
        layout.addWidget(button6)
        layout.addWidget(self.pastebox)
        layout.addWidget(button7)
        self.setLayout(layout)

    def on_pushButton_lookup(self):
        pasteboxValue = self.pastebox.text()
        self.dialog = ChartWindow(lookup(pasteboxValue, self.main), True)
        self.dialog.show()

    def on_pushButton_search(self):
        textboxValue = self.textbox.text()
        searchterms = [x.strip() for x in textboxValue.split(',')]
        self.dialog = ChartWindow(filterDB(searchterms, self.main))
        self.dialog.show()

    def on_pushButton_all(self):
        self.dialog = ChartWindow(getDB(self.main))
        self.dialog.show()

    def on_pushButton_rnd(self):
        self.dialog = ChartWindow(rndDB(self.main), True)
        self.dialog.show()

    def on_pushButton_region(self):
        self.dialog = ChartWindow(getDB(self.main, 'a'))
        self.dialog.show()

    def on_pushButton_category(self):
        self.dialog = ChartWindow(getDB(self.main, 'c'))
        self.dialog.show()

    def on_pushButton_ingredients(self):
        self.dialog = ChartWindow(getDB(self.main, 'i'))
        self.dialog.show()


class ChartWindow(QWidget):
    def __init__(self, df, transposed=False):
        super().__init__()
        self.resize(1000, 600)
        self.move(203, 100)
        scroll = QScrollArea()
        layout = QVBoxLayout()
        table = QTableWidget()
        scroll.setWidget(table)
        layout.addWidget(table)
        cols = list(df.columns)
        rows = list(df.index)
        table.setColumnCount(len(df.columns))
        table.setRowCount(len(df.index))
        if transposed:
            table.setVerticalHeaderLabels(rows)
        else:
            table.setHorizontalHeaderLabels(cols)
        for i in range(len(rows)):
            for j in range(len(cols)):
                table.setItem(i, j, QTableWidgetItem(str(df.iloc[i, j])))
        table.resizeColumnsToContents()
        self.setLayout(layout)


if __name__ == '__main__':
    appctxt = ApplicationContext()
    stylesheet = appctxt.get_resource('styles.qss')
    appctxt.app.setStyleSheet(open(stylesheet).read())
    appctxt.app.setStyle('Macintosh')
    main = MainWindow(appctxt)
    main.show()
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)
