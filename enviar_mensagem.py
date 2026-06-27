import pandas as pd
import urllib.parse
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


WHATSAPP_WEB_URL = "https://web.whatsapp.com/"
QR_WAIT_SECONDS = 40
MSG_LOAD_TIMEOUT = 20
DELAY_BETWEEN_MESSAGES = 5

SEND_BUTTON_XPATH = '//span[@data-icon="send"]'
MESSAGE_INPUT_XPATH = '//div[@title="Digite uma mensagem"]'
PANE_SIDE_XPATH = '//*[@id="pane-side"]'


def esperar_whatsapp_carregar(driver: webdriver.Chrome) -> None:
    print("Aguardando QR Code ser escaneado...")
    WebDriverWait(driver, QR_WAIT_SECONDS).until(
        EC.presence_of_element_located((By.XPATH, PANE_SIDE_XPATH))
    )
    print("WhatsApp Web carregado com sucesso!")


def enviar_mensagem(driver: webdriver.Chrome, numero: str, texto: str) -> bool:
    texto_codificado = urllib.parse.quote(texto)
    link = f"https://web.whatsapp.com/send?phone={numero}&text={texto_codificado}"
    driver.get(link)

    try:
        campo_mensagem = WebDriverWait(driver, MSG_LOAD_TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, MESSAGE_INPUT_XPATH))
        )
        campo_mensagem.send_keys(Keys.ENTER)
        time.sleep(DELAY_BETWEEN_MESSAGES)
        return True
    except TimeoutException:
        print(f"  Timeout ao carregar conversa com {numero}. Pulando...")
        return False
    except NoSuchElementException:
        print(f"  Numero {numero} nao encontrado. Pulando...")
        return False


def main():
    try:
        contatos_df = pd.read_excel("Enviar.xlsx")
    except FileNotFoundError:
        print("Erro: arquivo 'Enviar.xlsx' nao encontrado.")
        print("Crie o arquivo com as colunas: Pessoa, Numero, Mensagem")
        return

    colunas_necessarias = {"Pessoa", "Número", "Mensagem"}
    if not colunas_necessarias.issubset(contatos_df.columns):
        print(f"Erro: o arquivo deve ter as colunas: {colunas_necessarias}")
        print(f"Colunas encontradas: {set(contatos_df.columns)}")
        return

    opcoes = webdriver.ChromeOptions()
    opcoes.add_argument("--user-data-dir=./sessao_whatsapp")

    driver = webdriver.Chrome(options=opcoes)
    driver.get(WHATSAPP_WEB_URL)

    try:
        esperar_whatsapp_carregar(driver)

        enviados = 0
        falhos = 0

        for i, linha in contatos_df.iterrows():
            pessoa = linha["Pessoa"]
            numero = str(linha["Número"]).strip()
            mensagem = linha["Mensagem"]

            texto_completo = f"Oi {pessoa}! {mensagem}"
            print(f"[{i+1}/{len(contatos_df)}] Enviando para {pessoa} ({numero})...")

            sucesso = enviar_mensagem(driver, numero, texto_completo)
            if sucesso:
                enviados += 1
                print(f"  Mensagem enviada!")
            else:
                falhos += 1

        print(f"\nConcluido! Enviados: {enviados} | Falhas: {falhos}")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
