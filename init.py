import requests
import json
from bs4 import BeautifulSoup
import time
import datetime

class Ingrediente:
    def __init__(self,nome,link,imagem,health,hunger,sanity,perish,arrayValues,arrayDlcs):
        self.name = nome
        self.link = link
        self.img = imagem
        try:
            self.health = float(health)
        except: 
            self.health = health
        try:
            self.hunger = float(hunger)
        except: 
            self.hunger = hunger
        try:
            self.sanity = float(sanity)
        except: 
            self.sanity = sanity
        try:
            self.perish = float(perish)
        except: 
            self.perish = perish
        self.arrayValues = arrayValues
        self.arrayDlcs = arrayDlcs

class Receita:
    def __init__(self,nome,link,imagem,health,hunger,sanity,perish,arrayDlcs):
        self.name = nome
        self.link = link
        self.img = imagem
        try:
            self.health = float(health)
        except: 
            self.health = health
        try:
            self.hunger = float(hunger)
        except: 
            self.hunger = hunger
        try:
            self.sanity = float(sanity)
        except: 
            self.sanity = sanity
        try:
            self.perish = float(perish)
        except: 
            self.perish = perish

        self.arrayDlcs = arrayDlcs
        self.examples = pegarExemplos(self.link)

class Comestivel:
    def __init__(self,nome,link,imagem,health,hunger,sanity,perish,arrayDlcs):
        self.name = nome
        self.link = link
        self.img = imagem
        try:
            self.health = float(health)
        except: 
            self.health = health
        try:
            self.hunger = float(hunger)
        except: 
            self.hunger = hunger
        try:
            self.sanity = float(sanity)
        except: 
            self.sanity = sanity
        try:
            self.perish = float(perish)
        except: 
            self.perish = perish

        self.arrayDlcs = arrayDlcs


def pegarExemplos(link):
    url = 'https://dontstarve.fandom.com' + link
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    exemplos = []
    tabelas_exemplo = soup.find_all('table')

    print('Searching for examples of '+link)
    #REMOVENDO TODAS AS TABELAS DESNECESSARIAS
    for index,table in enumerate(tabelas_exemplo):
        colunas = table.find_all('td')
        if len(colunas) > 8:
            tabelas_exemplo.pop(index)
            continue
        for td in colunas:
            if '×' in td.text:
                tabelas_exemplo.pop(index)
                continue
        # if '(' in table.text:
        #     tabelas_exemplo.pop(index)
        # if '.' in table.text:
        #     tabelas_exemplo.pop(index)



    print('Found '+str(len(tabelas_exemplo))+ ' examples for: '+link)


    for table in tabelas_exemplo:
        try:
            colunas = table.find_all('td')
            cont = 1    
            ingredients = []
            for td in colunas:
                if cont > 4:
                    break
                
                ingredient = {
                    'name': td.find('a')['title'],
                    'img': td.find('a').find('img')['data-src']
                }

                cont = cont + 1
                ingredients.append(ingredient)
            recipe = {'recipe':ingredients}

            if len(ingredients) == 4:
                exemplos.append(recipe)

        except:
            pass
    print('Returning '+str(len(exemplos))+ ' examples for '+link )
    return exemplos

def atualizarDadosJSON():

    r = requests.get('https://dontstarve.fandom.com/wiki/Food')
    soup = BeautifulSoup(r.text, 'html.parser')

    tabelas = soup.find_all('table')
    tabela_comida = tabelas[0]

    arrayComestiveis = []
    arrayIngredientes = []
    arrayReceitas = []

    for linha in tabela_comida.find_all('tr'):
        colunas = linha.find_all('td')
        arrayDlcs = []
        try:
            link = colunas[0].find('a')
            imagem = link.find('img')['data-src']
            nome = colunas[1].find('a').text
            acesso = colunas[1].find('a')['href']
        except:
            continue

        try:
            dlcs = colunas[2].find_all('a')
            for dlc in dlcs:

                arrayDlcs.append(dlc['title'].replace('icon','').strip())
        except:
            pass
        arrayValues = []
        try:
            groups = colunas[8].find_all('a')
            headers = []
            valores = colunas[8].text.replace('\n','').replace('x','').split(' ')
            valores = list(filter(None, valores))
            
            if groups[0]['title'] == 'Crock Pot' or groups[0]['title'] == 'Portable Crock Pot':
                arrayValues = None
            else:
                for group,valor in zip(groups,valores):
                    headers.append(group['title'])

                for header,valor in zip(headers,valores):
                    dicionario = {
                        "nome": header,
                        "valor": float(valor.replace('×',''))
                    }
                    arrayValues.append(dicionario)

        except:
            pass




        health = colunas[3].text.replace('+','').strip()
        hunger = colunas[4].text.replace('+','').strip()
        sanity = colunas[5].text.replace('+','').strip()
        perish = colunas[6].text.strip()

        if arrayValues == None:
            arrayReceitas.append(Receita(nome,acesso,imagem,health,hunger,sanity,perish,arrayDlcs))
        elif arrayValues == []:
            arrayComestiveis.append(Comestivel(nome,acesso,imagem,health,hunger,sanity,perish,arrayDlcs))
        else:
            arrayIngredientes.append(Ingrediente(nome,acesso,imagem,health,hunger,sanity,perish,arrayValues,arrayDlcs))
            
    arrayReceitasJSON = []
    arrayIngredientesJSON = []
    arrayComestiveisJSON = []
    

    for x in arrayReceitas:
        arrayReceitasJSON.append(x.__dict__)
    for x in arrayIngredientes:
        arrayIngredientesJSON.append(x.__dict__)
    for x in arrayComestiveis:
        arrayComestiveisJSON.append(x.__dict__)

    jsonDadosReceitas = {
        'author':'Glok',
        'lastUpdate':str(datetime.date.today()),
        'lastUpdateTs':str(time.time()),
        'recipes': arrayReceitasJSON

    }
    jsonDadosIngredientes = {
        'author':'Glok',
        'lastUpdate':str(datetime.date.today()),
        'lastUpdateTs':str(time.time()),
        'recipes': arrayIngredientesJSON

    }
    jsonDadosComestiveis = {
        'author':'Glok',
        'lastUpdate':str(datetime.date.today()),
        'lastUpdateTs':str(time.time()),
        'recipes': arrayComestiveisJSON

    }

    with open('recipes.json', 'w') as fp:
        fp.write(json.dumps(jsonDadosReceitas,indent=4))
    with open('ingredients.json', 'w') as fp:
        fp.write(json.dumps(jsonDadosIngredientes,indent=4))
    with open('foods.json', 'w') as fp:
        fp.write(json.dumps(jsonDadosComestiveis,indent=4))



atualizarDadosJSON()