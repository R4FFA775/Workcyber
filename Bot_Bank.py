from SQL_lite import BankDatabase
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from bank_email import enviar_extrato_mensal, enviar_alerta_transacao, enviar_boleto_vencimento, enviar_extrato_pdf

TOKEN = "7927020967:AAH98kEI69H9JENuVNFDEjpCULV0yscAtSc"
db = BankDatabase()

# Função para consultar o saldo da conta
async def saldo(update: Update, context: CallbackContext):
    args = update.message.text.split()
    if len(args) < 2:
        await update.message.reply_text("Uso: /saldo <número da conta>")
        return

    numero_conta = args[1]
    saldo = db.get_saldo(numero_conta)
    if saldo is not None:
        await update.message.reply_text(f"Saldo da conta {numero_conta}: R$ {saldo:.2f}")
    else:
        await update.message.reply_text("Conta não encontrada.")

# Comando /extrato
async def extrato(update: Update, context: CallbackContext):
    args = update.message.text.split()
    if len(args) < 2:
        await update.message.reply_text("Uso: /extrato <número da conta>")
        return

    numero_conta = args[1]
    movimentacoes = db.get_movimentacoes(numero_conta)
    if movimentacoes:
        extrato_texto = "\n".join([f"{m[0]}: R$ {m[1]:.2f} - {m[3]} ({m[2]})" for m in movimentacoes])
        await update.message.reply_text(f"Extrato da conta {numero_conta}:\n{extrato_texto}")
    else:
        await update.message.reply_text("Conta não encontrada ou sem movimentações.")

# Comando /enviar_extrato
async def enviar_extrato(update: Update, context: CallbackContext):
    args = update.message.text.split()
    if len(args) < 2:
        await update.message.reply_text("Uso: /enviar_extrato <número da conta>")
        return

    numero_conta = args[1]
    movimentacoes = db.get_movimentacoes(numero_conta)
    if movimentacoes:
        extrato_texto = "\n".join([f"{m[0]}: R$ {m[1]:.2f} - {m[3]} ({m[2]})" for m in movimentacoes])
        resultado = enviar_extrato_mensal(extrato_texto)
        await update.message.reply_text(resultado)
    else:
        await update.message.reply_text("Conta não encontrada ou sem movimentações.")

# Comando /alerta_transacao
async def alerta_transacao(update: Update, context: CallbackContext):
    args = update.message.text.split()
    if len(args) < 2:
        await update.message.reply_text("Uso: /alerta_transacao <detalhes da transação>")
        return

    transacao = " ".join(args[1:])
    resultado = enviar_alerta_transacao(transacao)
    await update.message.reply_text(resultado)

# Comando /segunda_via_boleto
async def segunda_via_boleto(update: Update, context: CallbackContext):
    args = update.message.text.split()
    if len(args) < 2:
        await update.message.reply_text("Uso: /segunda_via_boleto <detalhes do boleto>")
        return

    boleto = " ".join(args[1:])
    resultado = enviar_boleto_vencimento(boleto)
    await update.message.reply_text(resultado)

# Comando /notificar_transacao
async def notificar_transacao(update: Update, context: CallbackContext):
    args = update.message.text.split()
    if len(args) < 2:
        await update.message.reply_text("Uso: /notificar_transacao <detalhes da transação>")
        return

    transacao = " ".join(args[1:])
    resultado = enviar_alerta_transacao(transacao)
    await update.message.reply_text(resultado)

# Comando /enviar_extrato_pdf
async def enviar_extrato_pdf_command(update: Update, context: CallbackContext):
    args = update.message.text.split()
    if len(args) < 2:
        await update.message.reply_text("Uso: /enviar_extrato_pdf <número da conta>")
        return

    numero_conta = args[1]
    movimentacoes = db.get_movimentacoes(numero_conta)
    if movimentacoes:
        extrato_texto = "\n".join([f"{m[0]}: R$ {m[1]:.2f} - {m[3]} ({m[2]})" for m in movimentacoes])
        resultado = enviar_extrato_pdf(extrato_texto)
        await update.message.reply_text(resultado)
    else:
        await update.message.reply_text("Conta não encontrada ou sem movimentações.")

# Comando /help
async def help_command(update: Update, context: CallbackContext):
    comandos = (
        "/saldo <número da conta> - Consultar saldo da conta\n"
        "/extrato <número da conta> - Consultar extrato da conta\n"
        "/enviar_extrato <número da conta> - Enviar extrato mensal por e-mail\n"
        "/alerta_transacao <detalhes da transação> - Enviar alerta de transação suspeita por e-mail\n"
        "/segunda_via_boleto <detalhes do boleto> - Solicitar segunda via de boletos\n"
        "/notificar_transacao <detalhes da transação> - Receber notificações de transações\n"
        "/enviar_extrato_pdf <número da conta> - Enviar extrato mensal em PDF por e-mail\n"
    )
    await update.message.reply_text(comandos)

# Função principal para rodar o bot
def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("saldo", saldo))
    application.add_handler(CommandHandler("extrato", extrato))
    application.add_handler(CommandHandler("enviar_extrato", enviar_extrato))
    application.add_handler(CommandHandler("alerta_transacao", alerta_transacao))
    application.add_handler(CommandHandler("segunda_via_boleto", segunda_via_boleto))
    application.add_handler(CommandHandler("notificar_transacao", notificar_transacao))
    application.add_handler(CommandHandler("enviar_extrato_pdf", enviar_extrato_pdf_command))
    application.add_handler(CommandHandler("help", help_command))

    print("Bot iniciado...")
    application.run_polling()

if __name__ == "__main__":
    main()