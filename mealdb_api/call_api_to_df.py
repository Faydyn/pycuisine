import pandas as pd
from urllib.request import Request, urlopen
import json


def getheader(exampleentry):
    return list(exampleentry.keys())


def getdata(listentries):
    return [list(x.values()) for x in listentries]


def create_df(link):
    try:
        request = Request(link)
        response = urlopen(request)
        elevations = response.read()
        data_dict = json.loads(elevations)
        listofentries = list(data_dict.values())[0]
        header = getheader(listofentries[0])
        data = getdata(listofentries)
        df = pd.DataFrame(data, columns=header)
        return df
    except TypeError:
        print('Chosen Link doesnt exists!')
        return None
