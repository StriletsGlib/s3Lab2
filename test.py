from spyre import server
from pathlib import Path

import os, sys
import pandas as pd
import urllib3
import json

class lab2App(server.App):
    title = "Lab 2"
    years = []
    for i in range(1981, 2020): years.append({"label": i, "value": i})
    inputs = [{        "type":'dropdown',
                    "label": 'Часовий ряд',
                    "options" : [ {"label": "VCI", "value":"VC"},
                                  {"label": "TCI", "value":"TC"},
                                  {"label": "VHI", "value":"VHI"}],
                    "key": 'timeSeries',
                    "action_id": "update_data"},
                {        "type":'dropdown',
                    "label": 'Область',
                    "options" : [ {"label": "Вінницька", "value": 1},
                                  {"label": "Волинська", "value":2},
                                  {"label": "Дніпропетровська", "value":3},
                                  {"label": "Донецька", "value":4},
                                  {"label": "Житомирська", "value":5},
                                  {"label": "Закарпатська", "value":6},
                                  {"label": "Запорізька", "value":7},
                                  {"label": "Івано-Франківська", "value":8},
                                  {"label": "Київська", "value":9},
                                  {"label": "Кіровоградська", "value":10},
                                  {"label": "Луганська", "value":11},
                                  {"label": "Львівська", "value":12},
                                  {"label": "Миколаївська", "value":13},
                                  {"label": "Одеська", "value":14},
                                  {"label": "Полтавська", "value":15},
                                  {"label": "Рівенська", "value":16},
                                  {"label": "Сумська", "value":17},
                                  {"label": "Тернопільська", "value":18},
                                  {"label": "Харківська", "value":19},
                                  {"label": "Херсонська", "value":20},
                                  {"label": "Хмельницька", "value":21},
                                  {"label": "Черкаська", "value":22},
                                  {"label": "Чернівецька", "value":23},
                                  {"label": "Чернігівська", "value":24},
                                  {"label": "Республіка Крим", "value":25},
                                  {"label": "Київ", "value":26},
                                  {"label": "Севастополь", "value":27}],
                    "key": 'region',
                    "action_id": "update_data"},
                    {        "type":'dropdown',
                    "label": 'Рік 1',
                    "options" : years,
                    "key": 'startYear',
                    "action_id": "update_data"},
                    {        "type":'dropdown',
                    "label": 'Рік 2',
                    "options" : years,
                    "key": 'endYear',
                    "action_id": "update_data"}]

    controls = [{    "type" : "hidden",
                    "id" : "update_data"}]

    tabs = ["Plot", "Table"]

    outputs = [{ "type" : "plot",
                    "id" : "plot",
                    "control_id" : "update_data",
                    "tab" : "Plot"},
                { "type" : "table",
                    "id" : "table_id",
                    "control_id" : "update_data",
                    "tab" : "Table",
                    "on_page_load" : True }]
    def formFrameByID(self, ID, path, debug = False):
        ID = str(ID)
        listOfFiles=os.listdir(path)
        #print(listOfFiles)
        for i in listOfFiles:
            idRead = i.split('_')[0]
            if (ID == idRead):
                df = pd.read_csv(path+i)
                df.reset_index(drop=True, inplace=True)
                columns_names=df.columns.values
                df = df.rename(columns=
                    {columns_names[0]: 'Year',columns_names[1]:'Week', columns_names[2] :'NDVI' , columns_names[3] : 'BT',
                    columns_names[4] : 'VC',columns_names[5] : 'TC', columns_names[6] : 'VHI'})
                df= df.drop('Unnamed: 7', 1)
                if(type(df)!= 'NoneType'): return df
    def getData(self, params):
        ID = params['region']
        #self.company_name = data['meta']['Company-Name']
        df = self.formFrameByID(ID, str(Path(__file__).parent.absolute()) + '/data/')
        for i in df.columns: 
            if((i!='Year') & (i!='Week') & (i != params['timeSeries'])):
                df = df.drop(i, 1)
        df = df[(df.Year.astype(float)>=float(params["startYear"])) & (df.Year.astype(float)<=float(params["endYear"]))]
        return df

    def getPlot(self, params):
        df = self.getData(params)
        calendarData = []
        for i in df.index:
            calendarData.append(df["Year"][i] + (df["Week"][i]-1)/52)
        df["Year"]= calendarData
        df = df.drop("Week", 1)
        df = df.set_index("Year")
        plt_obj = df.plot()
        plt_obj.set_ylabel(params['timeSeries'])
        #plt_obj.set_title(title)
        fig = plt_obj.get_figure()
        return fig

app = lab2App()
app.launch()