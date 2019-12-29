def search(searchterm):  # can also search for letters
    return f'https://www.themealdb.com/api/json/v1/1/search.php?s={searchterm}'


def lookupmeal(id):  # can also search for letters
    return f'https://www.themealdb.com/api/json/v1/1/lookup.php?i={id}'


def rndmeal():
    return 'https://www.themealdb.com/api/json/v1/1/random.php'


def listdb(reference):  # c - Category, a - Region, i - Ingredients
    return f'https://www.themealdb.com/api/json/v1/1/list.php?{reference}=list'


def filterdb(reference, filterterm):  # c - Category, a - Region, i - Ingredients
    return f'https://www.themealdb.com/api/json/v1/1/filter.php?{reference}={filterterm}'


