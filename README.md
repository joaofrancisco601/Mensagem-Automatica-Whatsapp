# Mensagem-Automatica-Whatsapp
#Mensagem Automatica Whatsapp
import pandas as pd
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

contatos_df = pd.read_excel("Enviar.xlsx")

navegador = webdriver.Chrome()
navegador.get("https://web.whatsapp.com/")
time.sleep(40)

while len(navegador.find_elements_by_xpath('//*[@id="pane-side"]')) < 1:
    time.sleep(1)

for i, mensagem in enumerate(contatos_df['Mensagem']):
    pessoa = contatos_df.loc[i, "Pessoa"]
    numero = contatos_df.loc[i, "Número"]
    texto = urllib.parse.quote(f"Oi {pessoa}! {mensagem}")
    link = f"https://web.whatsapp.com/send?phone={numero}&text={texto}"
    navegador.get(link)
    time.sleep(5)  
    while len(navegador.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div[2]/div[1]/p')) < 1:
        time.sleep(1)
    navegador.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div[2]/div[1]/p').send_keys(Keys.ENTER)
    
    time.sleep(10)
