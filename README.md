# Mensagem Automática WhatsApp

Envia mensagens automáticas via WhatsApp Web usando Selenium.

## Requisitos

```bash
pip install -r requirements.txt
```

Também é necessário ter o [ChromeDriver](https://chromedriver.chromium.org/) instalado e compatível com a versão do seu Chrome.

## Como usar

1. Crie o arquivo `Enviar.xlsx` com as colunas:
   - **Pessoa** — nome do destinatário
   - **Número** — número com código do país (ex: `5511999999999`)
   - **Mensagem** — texto a enviar

2. Execute o script:

```bash
python enviar_mensagem.py
```

3. Escaneie o QR Code no WhatsApp Web quando solicitado.

A sessão é salva em `./sessao_whatsapp`, então nas próximas execuções o login pode não ser necessário.

## Observações

- O número deve estar no formato internacional sem `+` ou espaços (ex: `5511999999999`).
- O script aguarda até 40 segundos para o QR Code ser escaneado.
