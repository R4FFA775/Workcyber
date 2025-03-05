import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from reportlab.pdfgen import canvas
from datetime import datetime

# Substitua pelas suas informações
EMAIL_REMETENTE = 'matheushlobo7@gmail.com'
SENHA_REMETENTE = 'zcqc qyyp ruks uxsr'

def enviar_email(assunto, mensagem, destinatario, anexo=None):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_REMETENTE
    msg['To'] = destinatario
    msg['Subject'] = assunto

    msg.attach(MIMEText(mensagem, 'plain'))

    if anexo:
        with open(anexo, "rb") as f:
            part = MIMEApplication(f.read(), Name=anexo)
            part['Content-Disposition'] = f'attachment; filename="{anexo}"'
            msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_REMETENTE, SENHA_REMETENTE)
        text = msg.as_string()
        server.sendmail(EMAIL_REMETENTE, destinatario, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return False

def enviar_extrato_mensal(extrato, destinatario):
    assunto = "Extrato Mensal"
    if enviar_email(assunto, extrato, destinatario):
        return "Extrato mensal enviado por e-mail!"
    else:
        return "Falha ao enviar extrato."

def enviar_alerta_transacao(transacao, destinatario):
    assunto = "Alerta de Transação Suspeita"
    if enviar_email(assunto, transacao, destinatario):
        return "Alerta de transação enviado por e-mail!"
    else:
        return "Falha ao enviar alerta."

def enviar_boleto_vencimento(boleto, destinatario):
    assunto = "Vencimento de Boleto"
    if enviar_email(assunto, boleto, destinatario):
        return "Notificação de vencimento enviada por e-mail!"
    else:
        return "Falha ao enviar notificação."

def gerar_pdf(extrato_texto, nome_arquivo):
    c = canvas.Canvas(nome_arquivo)
    c.drawString(100, 750, "Extrato mensal")
    c.drawString(100, 730, extrato_texto)
    c.save()

def enviar_extrato_pdf(extrato_texto, destinatario):
    nome_arquivo = "extrato.pdf"
    gerar_pdf(extrato_texto, nome_arquivo)
    assunto = "Extrato Mensal em PDF"
    mensagem = "Segue em anexo o seu extrato mensal em PDF."
    if enviar_email(assunto, mensagem, destinatario, nome_arquivo):
        return "Extrato mensal em PDF enviado por e-mail!"
    else:
        return "Falha ao enviar extrato em PDF."

def enviar_notificacao_transacao(transacao, destinatario):
    assunto = "Notificação de Transação Bancária"
    
    # Melhorando o formato da mensagem
    mensagem = f"""
    ======= NOTIFICAÇÃO DE TRANSAÇÃO =======
    
    {transacao}
    
    Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
    
    Esta é uma mensagem automática. Por favor, 
    caso não reconheça esta transação, entre em
    contato imediatamente com seu banco.
    
    ====================================
    """
    
    if enviar_email(assunto, mensagem, destinatario):
        print(f"Notificação enviada para {destinatario}")
        return True
    else:
        print(f"Falha ao enviar notificação para {destinatario}")
        return False

def verificar_transacao_suspeita(valor, historico_movimentacoes):
    # Verifica se uma transação é suspeita baseado em critérios
    media_transacoes = sum(float(mov.split(':')[1]) for mov in historico_movimentacoes) / len(historico_movimentacoes) if historico_movimentacoes else 0
    return valor > media_transacoes * 2  # Transação suspeita se valor > 2x a média

def enviar_extrato_programado(contas):
    # Para ser executado mensalmente
    for numero_conta, conta in contas.items():
        extrato = "\n".join(conta["movimentacoes"])
        enviar_extrato_mensal(extrato, conta["email"])

# Nome do arquivo PDF
arquivo_pdf = "extrato.pdf"
gerar_pdf("Saque de R$2000,00", arquivo_pdf)

# Enviar o e-mail com o extrato em PDF
resultado = enviar_extrato_pdf("Saque de R$2000,00", "rafaelcipher850@gmail.com")
print(resultado)