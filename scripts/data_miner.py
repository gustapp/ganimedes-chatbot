#%%
# Import Dependencies
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

#%%
# Source file with all courses codes
with open('./scripts/dataset/disciplinas_poli.csv','r') as file:
    course_id_list = []
    for row in csv.reader(file):
        course_id_list.append(row[0])

#%%
# Initialize Selenium Chrome Driver
course_list = []

driver = webdriver.Chrome('./scripts/chromedriver')
driver.wait = WebDriverWait(driver,5)

#%%
# (Legacy) webcrawler code
for course_id in course_id_list:
    try:
        nome = ""
        creditos_aula = ""
        creditos_trabalho = ""
        carga_horaria = ""
        objetivos = ""
        docentes_list = []
        programa_resumido = ""
        programa = ""
        avaliacao_metodo = ""
        avaliacao_criterio = ""
        avaliacao_recuperacao = ""
        bibliografia = ""
        oferecimento_list = []
        requisitos = []
        
        
        jupiter_url = 'https://uspdigital.usp.br/jupiterweb/obterDisciplina?sgldis=' + course_id + '&nomdis='
        driver.get(jupiter_url)

        nome = driver.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="layout_conteudo"]/table[1]/tbody/tr[4]/td/form/table[1]/tbody/tr[1]/td/table[3]/tbody/tr[5]/td/font/span/b'))).text
        nome = nome.split('-')[1][1:]

        creditos_aula = driver.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="layout_conteudo"]/table[1]/tbody/tr[4]/td/form/table[1]/tbody/tr[1]/td/table[4]/tbody/tr[1]/td[2]/font/span'))).text
        creditos_aula = int(creditos_aula)

        creditos_trabalho = driver.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="layout_conteudo"]/table[1]/tbody/tr[4]/td/form/table[1]/tbody/tr[1]/td/table[4]/tbody/tr[2]/td[2]/font/span'))).text
        creditos_trabalho = int(creditos_trabalho)

        carga_horaria = driver.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="layout_conteudo"]/table[1]/tbody/tr[4]/td/form/table[1]/tbody/tr[1]/td/table[4]/tbody/tr[3]/td[2]/font/span'))).text
        carga_horaria = carga_horaria.split(" ")[0]
        
        x = driver.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="layout_conteudo"]/table[1]/tbody/tr[4]/td/form/table[1]'))).text.split("\n")

        for line in range(len(x)):

            texto = x[line].strip()

            if(texto == 'Objetivos'):
                objetivos = x[line + 1].strip()
            if(texto == 'Programa Resumido'):
                programa_resumido = x[line + 1].strip()
            if(texto == 'Programa'):
                programa = x[line + 1].strip()
            if(texto == 'Método'):
                avaliacao_metodo = x[line + 1].strip()
            if(texto == 'Critério'):
                avaliacao_criterio = x[line + 1].strip()
            if(texto == 'Norma de Recuperação'):
                avaliacao_recuperacao = x[line + 1].strip()
            if(texto == 'Bibliografia'):
                bibliografia_raw = x[line + 1:len(x)-1]
                bibliografia = []
                for ref in bibliografia_raw:
                    bibliografia.append(ref.strip())        
        
        driver.get('https://uspdigital.usp.br/jupiterweb/obterTurma?sgldis=' + course_id)
        
        try:
            oferecimento_table = driver.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="layout_conteudo"]/table[1]/tbody/tr[4]/td/form/table/tbody/tr[1]/td/table[6]'))).text.split('\n') 

            result = []
            for element in oferecimento_table:
                if(element[:16] == 'Código da Turma:' or element[:4] == 'Tipo'  or element[:3] == 'seg' or element[:3] == 'ter' or element[:3] == 'qua' or element[:3] == 'qui' or element[:3] == 'sex' or element[:3] == 'sab'):
                    result.append(element)

            block_list = []
            list_element = []
            list_element.append(result[0])

            for x in range(1,len(result)):
                if(result[x][:6] == 'Código'):
                    block_list.append(list_element)
                    list_element = []

                list_element.append(result[x])

            block_list.append(list_element)


            oferecimento_list = []
            for block in block_list:

                oferecimento_element = {}
                oferecimento_element['codigo_turma'] = ""
                oferecimento_element['tipo_turma'] = ""
                oferecimento_element['horario'] = []
                for oferecimento in block:        
                    if(oferecimento[:6] == 'Código'):
                        oferecimento_element['codigo_turma'] = oferecimento.split(": ")[1]
                    elif(oferecimento[:4] == 'Tipo'):
                        oferecimento_element['tipo_turma'] = oferecimento.split(": ")[1]
                    elif(oferecimento[:3] == 'seg' or oferecimento[:3] == 'ter' or oferecimento[:3] == 'qua' or oferecimento[:3] == 'qui' or oferecimento[:3] == 'sex' or oferecimento[:3] == 'sab'):
                        horario_element = {}
                        horario_element['dia'] = oferecimento[:3]
                        horario_element['horario_inicio'] = oferecimento[4:9]
                        horario_element['horario_fim'] = oferecimento[10:15]
                        horario_element['professor'] = oferecimento[16:]        
                        oferecimento_element['horario'].append(horario_element)

                oferecimento_list.append(oferecimento_element)
        except:
            oferecimento_list = []
        
        course = {
            "sigla": course_id,
            "name": nome,
            "creditos":{
                "aula":creditos_aula,
                "trabalho":creditos_trabalho
            },
            "carga_horaria":carga_horaria,
            "objetivos":objetivos,
            "docentes":docentes_list,
            "programa":programa,
            "programa_resumido":programa_resumido,
            "avaliacao":{
                "metodo":avaliacao_metodo,
                "criterio":avaliacao_criterio,
                "recuperacao":avaliacao_recuperacao
            },
            "bibliografia":bibliografia,
            "requisitos":requisitos,
            "oferecimento":oferecimento_list
        }

        course_list.append(course)    

    except:
        print('erro em ' + course_id)

#%%
import json

with open('db_resto.json','w') as outfile:
    json.dump(course_list,outfile,indent=4)
