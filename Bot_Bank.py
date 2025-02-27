from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import difflib


# Dicionário com sinônimos e variações de frases
respostas = {
    "Oi! Como posso te ajudar?": ["oi", "olá", "e aí", "opa", "fala", "salve", "eai"],
    "Estou ótimo! Espero que você também esteja bem.": ["tudo bem?", "como você está?", "como vai?", "beleza?", "suave?", "tudo certo?"],
    "Eu sou um bot simples, mas posso te ajudar no que precisar!": ["qual seu nome?", "quem é você?", "como se chama?", "como posso te chamar?"],
    "Até mais! Volte sempre. 😊": ["tchau", "até mais", "até logo", "falou", "valeu", "fui"],
    "De nada! Fico feliz em ajudar. 😃": ["obrigado", "valeu", "agradecido", "muito obrigado", "obg"],
}

# Função para encontrar a melhor resposta, mesmo com erros
def encontrar_resposta(mensagem):
    mensagem = mensagem.lower()
    todas_frases = sum(respostas.values(), [])  # Junta todas as frases em uma lista única
    melhor_correspondencia = difflib.get_close_matches(mensagem, todas_frases, n=1, cutoff=0.6)

    if melhor_correspondencia:
        for resposta, frases in respostas.items():
            if melhor_correspondencia[0] in frases:
                return resposta  # Retorna a resposta correspondente
    
    return "Desculpe, não entendi."  # Se não encontrar, retorna essa resposta padrão

# Função para responder ao comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Olá! Eu sou um bot simples. Envie-me uma mensagem e eu responderei.")

# Função para responder mensagens de texto
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    resposta = encontrar_resposta(user_message)
    await update.message.reply_text(resposta)

# Configuração e execução do bot
def main():
    token = ""
    
    application = Application.builder().token(token).build()

    # Registra os handlers
    application.add_handler(CommandHandler("start", start))  # Responde ao /start
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))  # Responde mensagens de texto

    print("Bot está rodando...")
    application.run_polling()

main()
