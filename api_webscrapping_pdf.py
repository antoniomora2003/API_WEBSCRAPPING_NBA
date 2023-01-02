# el tiempo de ejecucion esta sobre los dos minutos y 10 segundos 
from pprint import pprint
import re 
import pandas as pd
import requests 
from bs4 import BeautifulSoup
from fpdf import FPDF
import matplotlib.pyplot as plt
import seaborn as sns
import signal
import warnings
import sys
import time as t 


def handler_signal(signal, frame):
    print("\n\n Interrupción!")
    sys.exit()

signal.signal(signal.SIGINT, handler_signal)
warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', 40)

# extraccion de los datos:

def extract(API_KEY, url):
    header = {'Ocp-Apim-Subscription-Key': API_KEY}
    api = requests.get(url, headers = header)
    diccionario = api.json()
    df = pd.DataFrame(diccionario)
    return df


# Trabsformacion de los datos, nos quedaremos solo con los de los nets 

def transform(df):
    df = df[df['Team'] == 'BKN']
    # los porcentajes de tiros de campo, triples y libres se calculan a partir de los tiros realizados y los intentos, estaban fatal realizados los de la API por ello lo cambie 
    # para asemejar los datos a la realidad y acabar con datos medianamente fiables
    df_nuevo = df.loc[:, ['Name', 'Points', 'Assists', 'Rebounds', 'Minutes', 'Games', 'Steals', "PlusMinus", "TwoPointersMade", "TwoPointersAttempted", "ThreePointersMade", "ThreePointersAttempted", "FreeThrowsMade", "FreeThrowsAttempted"]]
    df_nuevo['PointsPG'] = df['Points'] / df['Games']
    df_nuevo["AssitsPG"] = df["Assists"] / df["Games"]
    df_nuevo["ReboundsPG"] = df["Rebounds"] / df["Games"]
    df_nuevo["StealsPG"] = df["Steals"] / df["Games"]
    df_nuevo["MinutesPG"] = df["Minutes"] / df["Games"]
    df_nuevo["FielGoals %"] = (df["FieldGoalsMade"] / df["FieldGoalsAttempted"]) * 100
    df_nuevo["TwoPointers %"] = (df["TwoPointersMade"] / df["TwoPointersAttempted"] ) * 100
    df_nuevo["ThreePointers %"] = (df["ThreePointersMade"] / df["ThreePointersAttempted"] ) * 100
    df_nuevo["FreeThrows %"] = (df["FreeThrowsMade"] / df["FreeThrowsAttempted"] ) * 100
    df_nuevo["PlusMinusPG"] = df["PlusMinus"] / df["Games"]
    df_per_game = df_nuevo.drop(columns = ["Assists", "Rebounds", "Steals", "Minutes", "Games", "PlusMinus","TwoPointersMade", "TwoPointersAttempted", "ThreePointersMade", "ThreePointersAttempted", "FreeThrowsMade", "FreeThrowsAttempted"])
    return df_per_game

# por ultimo la visualizacion de los datos se lleva a cabo mediante un reporte ejecutivo en pdf

class PDF(FPDF):

    def portada(self):
        "incluyeme portada"
        self.add_page()
        self.set_font('Arial', 'B', 35)
        self.cell(80)
        self.cell(30, 10,"STATISTICS OF BROOKLYN NETS", 0, 0, 'C')
        self.ln(20)
        "añadir al final de la pagina un frase"
        self.set_font('Arial', 'B', 20)
        self.cell(0, 10, 'By: GM Antonio Mora', 0, 0, 'R')
        "mayor tamaño de la fuente"
        self.image('logo.png', 40, 80, 150)

    def hoja1(self):
        self.add_page()
        self.set_font('Arial', 'B', 20)
        self.cell(80)
        self.cell(30, 5,"STATISTICS OF BROOKLYN NETS", 0, 0, 'C')
        self.ln(20)
        self.set_font('Arial', 'B', 20)
        self.ln(10)
        self.image('Prueba1bis.png', 40, 40, 150)
        self.image('logo.png', 170, 10, 30)

    def hoja1b(self):
        self.add_page()
        self.set_font('Arial', 'B', 20)
        self.cell(80)
        self.cell(30, 5,"PRONOSTICADOR DE APUESTAS", 0, 0, 'C')
        self.ln(20)
        self.set_font('Arial', 'B', 20)
        self.ln(10)
        self.image('PRONOSTICOS.png', 40, 40, 150)
        self.image('logo.png', 170, 10, 30)


    def hoja2(self):
        self.add_page()
        self.set_font('Arial', 'B', 20)
        self.cell(80)
        self.cell(30, 5,"STATISTICS OF BROOKLYN NETS", 0, 0, 'C')
        self.ln(20)
        self.set_font('Arial', 'B', 20)
        self.ln(10)
        self.image('Prueba3.png', 40, 40, 110)
        self.image('Prueba4.png', 40, 160, 110)
        self.image('logo.png', 170, 10, 30)

    def hoja3(self):
        self.add_page()
        self.set_font('Arial', 'B', 20)
        self.cell(80)
        self.cell(30, 5,"STATISTICS OF BROOKLYN NETS", 0, 0, 'C')
        self.ln(20)
        self.set_font('Arial', 'B', 20)
        self.ln(10)
        self.image('Prueba5.png', 30, 30, 70)
        self.image('Prueba6.png', 30, 110, 70)
        self.image('Prueba7.png', 30, 190, 70)
        self.image('logo.png', 170, 10, 30)

    def hoja4(self):
        self.add_page()
        self.set_font('Arial', 'B', 20)
        self.cell(80)
        self.cell(30, 5,"STATISTICS OF BROOKLYN NETS", 0, 0, 'C')
        self.ln(20)
        self.set_font('Arial', 'B', 20)
        self.ln(10)
        self.image("Kevin-Durant-PNG-File.png", 10, 30, 60)
        self.image('Prueba8.png', 30, 90, 80)
        self.image("Prueba8bis.png", 30, 170, 80)
        self.image('logo.png', 170, 10, 30)

    def hoja5(self):
        self.add_page()
        self.set_font('Arial', 'B', 20)
        self.cell(80)
        self.cell(30, 5,"STATISTICS OF BROOKLYN NETS", 0, 0, 'C')
        self.ln(20)
        self.set_font('Arial', 'B', 20)
        self.ln(10)
        self.image("i.png", 10, 30, 60)
        self.image('Prueba9.png', 30, 90, 80)
        self.image("Prueba9bis.png", 30, 170, 80)
        self.image('logo.png', 170, 10, 30)

    def hoja6(self):
        self.add_page()
        self.set_font('Arial', 'B', 20)
        self.cell(80)
        self.cell(30, 5,"STATISTICS OF BROOKLYN NETS", 0, 0, 'C')
        self.ln(20)
        self.set_font('Arial', 'B', 20)
        self.ln(10)
        self.image("descarga.jpeg", 10, 30, 60)
        self.image('Prueba10.png', 30, 90, 80)
        self.image("Prueba10bis.png", 30, 170, 80)
        self.image('logo.png', 170, 10, 30)

    def hoja7(self):
        self.add_page()
        self.set_font('Arial', 'B', 20)
        self.cell(80)
        self.cell(30, 5,"STATISTICS OF BROOKLYN NETS", 0, 0, 'C')
        self.ln(20)
        self.set_font('Arial', 'B', 20)
        self.ln(10)
        self.image("descarga2.jpeg", 10, 30, 60)
        self.image('Prueba11.png', 30, 90, 80)
        self.image("Prueba11bis.png", 30, 170, 80)
        self.image('logo.png', 170, 10, 30)

    def hoja8(self):
        self.add_page()
        self.set_font('Arial', 'B', 20)
        self.cell(80)
        self.cell(30, 5,"STATISTICS OF BROOKLYN NETS", 0, 0, 'C')
        self.ln(20)
        self.set_font('Arial', 'B', 20)
        self.ln(10)
        self.image("descarga3.png", 10, 30, 60)
        self.image('Prueba12.png', 30, 90, 80)
        self.image("Prueba12bis.png", 30, 170, 80)
        self.image('logo.png', 170, 10, 30)

        
        
def tabla_inicial(df):
    df_ppg = df.loc[:, ["Name","PointsPG", "AssitsPG", "ReboundsPG", "StealsPG", "MinutesPG","FielGoals %", "TwoPointers %", "ThreePointers %", "FreeThrows %"]]
    df_ppg = df_ppg.round(3)
    fig, ax = plt.subplots(figsize=(10,10))
    ax.axis('off')
    plt.title("Estadisticas por partido")
    tabla3 = ax.table(cellText=df_ppg.values, cellLoc='center', loc='center', colLabels=df_ppg.columns, colWidths = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,0.1,0.1,0.1])
    tabla3.auto_set_font_size(False)
    tabla3.set_fontsize(7)
    plt.savefig('Prueba1bis.png', dpi=300)

def grafica_mas_menos(df):
    "quedarse en la columna name con el utlimo y penultimo string de cada casilla"
    df_mas_menos = df.loc[:, ["Name", "PlusMinusPG"]]
    df_mas_menos = df_mas_menos.sort_values(by = "PlusMinusPG", ascending = False)
    figure = plt.figure(figsize=(8,8))
    sns.barplot(y = df_mas_menos["Name"], x = df_mas_menos["PlusMinusPG"], color = "blue")
    plt.title("PlusMinus por partido")
    plt.savefig('Prueba3.png', dpi=300)

    df_ppg = df.loc[:, ["Name", "Points"]]
    df_ppg = df_ppg.sort_values(by = "Points", ascending = False)
    figure = plt.figure(figsize=(8,8))
    sns.barplot(y = df_ppg["Name"], x = df_ppg["Points"], color = "green")
    plt.title("Puntos totales")
    plt.savefig('Prueba4.png', dpi=300)

    



def distintas_graficas(df):

    df_ppg = df.loc[:, ["Name", "PointsPG"]]
    df_ppg = df_ppg.sort_values(by = "PointsPG", ascending = False)
    df_ppg = df_ppg.head(5)
    figure = plt.figure(figsize=(8,8))
    sns.barplot(y = df_ppg["Name"], x = df_ppg["PointsPG"], color = "green")
    plt.title("Puntos por partido")
    plt.savefig('Prueba5.png', dpi=300)

    df_rpg = df.loc[:, ["Name", "ReboundsPG"]]
    df_rpg = df_rpg.sort_values(by = "ReboundsPG", ascending = False)
    df_rpg = df_rpg.head(5)
    figure = plt.figure(figsize=(8,8))
    sns.barplot(y = df_rpg["Name"], x = df_rpg["ReboundsPG"], color = "red")
    plt.title("Rebotes por partido")
    plt.savefig('Prueba6.png', dpi=300)

    df_apg = df.loc[:, ["Name", "AssitsPG"]]
    df_apg = df_apg.sort_values(by = "AssitsPG", ascending = False)
    df_apg = df_apg.head(5)
    figure = plt.figure(figsize=(8,8))
    sns.barplot(y = df_apg["Name"], x = df_apg["AssitsPG"], color = "blue")
    plt.title("Asistencias por partido")
    plt.savefig('Prueba7.png', dpi=300)

def jugadores_mas_destacados(df):
    df1= df.loc[df["Name"] == "Durant"]
    df1 = df1.loc[:, ["PointsPG", "ReboundsPG", "AssitsPG", "StealsPG", "PlusMinusPG"]]
    df2 = df.loc[df["Name"] == "Durant"]
    df2 = df2.loc[:,["FielGoals %", "ThreePointers %", "FreeThrows %", "TwoPointers %"]]
    df1 = df1.T
    df1.columns = ["Durant"]
    df1 = df1.sort_values(by = "Durant", ascending = False)
    figure = plt.figure(figsize=(8,8))
    sns.barplot(y = df1.index, x = df1["Durant"], color = "green")
    plt.title("Estadisticas de Durant")
    plt.savefig('Prueba8.png', dpi=300)

    df2 = df2.T
    df2.columns = ["Durant"]
    df2 = df2.sort_values(by = "Durant", ascending = False)
    figure = plt.figure(figsize=(8,8))
    sns.barplot(y = df2.index, x = df2["Durant"], color = "blue")
    plt.title("Estadisticas de Durant")
    plt.savefig('Prueba8bis.png', dpi=300)




    

def jugadores_mas_destacados2(df):
    df1 = df.loc[df["Name"] == "Irving"]
    df1 = df1.loc[:, ["PointsPG", "ReboundsPG", "AssitsPG", "StealsPG", "PlusMinusPG"]]
    df2 = df.loc[df["Name"] == "Irving"]
    df2 = df2.loc[:,["FielGoals %", "ThreePointers %", "FreeThrows %", "TwoPointers %"]]
    df1= df1.T
    df1.columns = ["Irving"]
    df1 = df1.sort_values(by = "Irving", ascending = False)
    figure = plt.figure(figsize=(8,8))
    sns.barplot(y = df1.index, x = df1["Irving"], color = "green")
    plt.title("Estadisticas de Irving")
    plt.savefig('Prueba9.png', dpi=300)

    df2 = df2.T
    df2.columns = ["Irving"]
    df2 = df2.sort_values(by = "Irving", ascending = False)
    figure = plt.figure(figsize=(8,8))
    sns.barplot(y = df2.index, x = df2["Irving"], color = "blue")
    plt.title("Porcentaje de tiros de Irving")
    plt.savefig('Prueba9bis.png', dpi=300)


def jugadores_mas_destacados3(df):
    df1 = df.loc[df["Name"] == "Curry"]
    df1 = df1.loc[:, ["PointsPG", "ReboundsPG", "AssitsPG", "StealsPG", "PlusMinusPG"]]
    df2 = df.loc[df["Name"] == "Curry"]
    df2 = df2.loc[:,["FielGoals %", "ThreePointers %", "FreeThrows %", "TwoPointers %"]]
    df1= df1.T
    df1.columns = ["Curry"]
    df1 = df1.sort_values(by = "Curry", ascending = False)
    figure = plt.figure(figsize=(8,8))
    sns.barplot(y = df1.index, x = df1["Curry"], color = "green")
    plt.title("Estadisticas de Curry")
    plt.savefig('Prueba10.png', dpi=300)

    df2 = df2.T
    df2.columns = ["Curry"]
    df2 = df2.sort_values(by = "Curry", ascending = False)
    figure = plt.figure(figsize=(8,8))
    sns.barplot(y = df2.index, x = df2["Curry"], color = "blue")
    plt.title("Porcentaje de tiros de Curry")
    plt.savefig('Prueba10bis.png', dpi=300)


def jugadores_mas_destacados4(df):
    df1 = df.loc[df["Name"] == "Drummond"]
    df1 = df1.loc[:, ["PointsPG", "ReboundsPG", "AssitsPG", "StealsPG", "PlusMinusPG"]]
    df2 = df.loc[df["Name"] == "Drummond"]
    df2 = df2.loc[:,["FielGoals %", "ThreePointers %", "FreeThrows %", "TwoPointers %"]]
    df1= df1.T
    df1.columns = ["Drummond"]
    df1 = df1.sort_values(by = "Drummond", ascending = False)
    figure = plt.figure(figsize=(8,8))
    sns.barplot(y = df1.index, x = df1["Drummond"], color = "green")
    plt.title("Estadisticas de Drummond")
    plt.savefig('Prueba11.png', dpi=300)

    df2 = df2.T
    df2.columns = ["Drummond"]
    df2 = df2.sort_values(by = "Drummond", ascending = False)
    figure = plt.figure(figsize=(8,8))
    sns.barplot(y = df2.index, x = df2["Drummond"], color = "blue")
    plt.title("Porcentaje de tiros de Drummond")
    plt.savefig('Prueba11bis.png', dpi=300)

def jugadores_mas_destacados5(df):
    "hacer lo mismo pero con Mills"
    df1 = df.loc[df["Name"] == "Mills"]
    df1 = df1.loc[:, ["PointsPG", "ReboundsPG", "AssitsPG", "StealsPG", "PlusMinusPG"]]
    df2 = df.loc[df["Name"] == "Mills"]
    df2 = df2.loc[:,["FielGoals %", "ThreePointers %", "FreeThrows %", "TwoPointers %"]]
    df1= df1.T
    df1.columns = ["Mills"]
    df1 = df1.sort_values(by = "Mills", ascending = False)
    figure = plt.figure(figsize=(8,8))
    sns.barplot(y = df1.index, x = df1["Mills"], color = "green")
    plt.title("Estadisticas de Mills")
    plt.savefig('Prueba12.png', dpi=300)

    df2 = df2.T
    df2.columns = ["Mills"]
    df2 = df2.sort_values(by = "Mills", ascending = False)
    figure = plt.figure(figsize=(8,8))
    sns.barplot(y = df2.index, x = df2["Mills"], color = "blue")
    plt.title("Porcentaje de tiros de Mills")
    plt.savefig('Prueba12bis.png', dpi=300)



def webscrapping(url2):
    pagina_html = requests.get(url2)
    soup = BeautifulSoup(pagina_html.content, "html.parser")
    matches = soup.find_all("div", class_ = "cursor-pointer border rounded-md mb-4 px-1 py-2 flex flex-col lg:flex-row relative")
    dicci = {}
    for match in matches:
        pass
        
def creacion_reporte_ejecutivo():
    reporte_ejecutivo = PDF('P', 'mm', 'A4')
    reporte_ejecutivo.portada()
    reporte_ejecutivo.hoja1()
    reporte_ejecutivo.hoja1b()
    reporte_ejecutivo.hoja2()
    reporte_ejecutivo.hoja3()
    reporte_ejecutivo.hoja4()
    reporte_ejecutivo.hoja5()
    reporte_ejecutivo.hoja6()
    reporte_ejecutivo.hoja7()
    reporte_ejecutivo.hoja8()
    reporte_ejecutivo.output('Practica_Final.pdf')

def webscrapping(soup):
    matches = soup.find_all('div', class_="cursor-pointer border rounded-md mb-4 px-1 py-2 flex flex-col lg:flex-row relative")
    dicci = {}
    for partido in matches:
        match = partido.find('a', class_='').text.replace('\n', '')
        equipos = match.split(' - ')
        dicci[match] = {}
        cuotas = partido.find_all('span', class_="px-1 h-booklogosm font-bold bg-primary-yellow text-white leading-8 rounded-r-md w-14 md:w-18 flex justify-center items-center text-base")
        for i in range(len(cuotas)):
            dicci[match][equipos[i]] = (cuotas[i].text)
        if dicci[match][equipos[0]] > dicci[match][equipos[1]]:
            dicci[match]['Wins'] = equipos[1]
        else:
            dicci[match]['Wins'] = equipos[0]
    return dicci

def tratamiento_webscrapping(dicci):
    matches = list(dicci.keys())
    equipos_locales = []
    equipos_visitantes = []
    ganadores = []
    odds_locales = []
    odds_visitantes = []

    for partido in range(len(matches)):
        equipo_local  = list(dicci[matches[partido]].keys())[0]
        equipos_locales.append(equipo_local)
        equipo_visitante = list(dicci[matches[partido]].keys())[1]
        equipos_visitantes.append(equipo_visitante)
        ganador = list(dicci[matches[partido]].values())[2]
        ganadores.append(ganador)
        odds_local = list(dicci[matches[partido]].values())[0]
        odds_locales.append(odds_local)
        odds_visitante = list(dicci[matches[partido]].values())[1]
        odds_visitantes.append(odds_visitante)
   
    df = pd.DataFrame({'Partidos': matches, 'Equipos locales': equipos_locales, 'Equipos visitantes': equipos_visitantes, 'Cuotas locales': odds_locales, 'Cuotas visitantes': odds_visitantes, 'Ganador': ganadores})
    fig, ax = plt.subplots(figsize=(10,10))
    ax.axis('off')
    plt.title("Pronosticador de apuestas NBA")
    tabla3 = ax.table(cellText=df.values, cellLoc='center', loc='center', colLabels=df.columns, colWidths = [0.3, 0.15, 0.15, 0.15, 0.15, 0.15 ])
    tabla3.auto_set_font_size(False)
    tabla3.set_fontsize(7)
    plt.savefig('PRONOSTICOS.png', dpi=300)
    return df

if __name__ == "__main__":
    inicio = t.time()
    API_KEY = "6595ecd10189452884bddb1e4e15a194"
    url = "https://api.sportsdata.io/v3/nba/stats/json/PlayerSeasonStats/2022"
    url2 = "https://www.sportytrader.es/cuotas/baloncesto/usa/nba-306/"
    page_html = requests.get(url2).content
    soup = BeautifulSoup(page_html, 'html.parser')
    dicci = webscrapping(soup)
    df_webscrapping = tratamiento_webscrapping(dicci)
    df_webscrapping.to_csv('PRONOSTICOS.csv', index=False)
    print(df_webscrapping)
    
    tratamiento_webscrapping(dicci)
    df = extract(API_KEY, url)
    df_per_game = transform(df)
    df_per_game = df_per_game.dropna()
    df_per_game["Name"] = df_per_game["Name"].str.split(" ").str[-1]
    pprint(dicci)
    tabla_inicial(df_per_game)
    grafica_mas_menos(df_per_game)
    distintas_graficas(df_per_game)
    jugadores_mas_destacados(df_per_game)
    jugadores_mas_destacados2(df_per_game)
    jugadores_mas_destacados3(df_per_game)
    jugadores_mas_destacados4(df_per_game)
    jugadores_mas_destacados5(df_per_game)
    intermedio = t.time()
    print("Tiempo de ejecución intermedio : ", intermedio - inicio)
    creacion_reporte_ejecutivo()
    fin = t.time()
    print("Tiempo de ejecución: ", fin - inicio)

    
   