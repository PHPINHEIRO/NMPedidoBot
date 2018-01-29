from source import order_details,list_order_today
import os,logging
from telegram.ext import Updater, CommandHandler
from emoji import emojize

API_TELEGRAM_NMPEDIDOBOT_TOKEN = os.environ.get('API_TELEGRAM_NMPEDIDOBOT_TOKEN')


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)
def detalhe(bot,update):
    pass

def start(bot, update):
    """Envia a mensagem quando o comando /start é executado"""
    smile = emojize(":smile:", use_aliases=True)

    start_message = (
        "Bem vindo ao NMPedidoBot "+smile+"\n\n"
        "A cada minuto o bot verifica se tem novos pedidos na loja integrada,"
        "caso tenha pedido(s) novo(s), sera(o) mostrado(s)\n\n"
        "Para mais informacoes consulte o /help"

    )
    update.message.reply_text(start_message)

def help(bot, update):

    help_message = (

        "Assim que o bot eh iniciado, ele ja fica fazendo a verificacao se tem pedidos novos.\n\n"
        "Caso queira saber informacoes de algum pedido especifico, "
        "voce pode consultar atravez do comando /detelhe <numero_pedido>\n\n"

    )
    update.message.reply_text(help_message)


def bot_main():
    updater = Updater(API_TELEGRAM_NMPEDIDOBOT_TOKEN) # Token dado pelo BotFather
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start)) # Manipulador de comandos
    dp.add_handler(CommandHandler("help", help)) # Manipulador de comandos
    dp.add_handler(CommandHandler("detalhe",detalhe)) # Manipulador de comandos
    # dp.add_handler(CommandHandler("/procurar", show_movie_list,pass_args=True,pass_job_queue=True,pass_chat_data=True))
    # dp.add_handler(MessageHandler(Filters.text, show_movie_list))
    # dp.add_handler(MessageHandler(Filters.text, show_movie_info))

    updater.start_polling() #Inicia o loop de execução do bot
    updater.idle()

if __name__ == '__main__':
    bot_main()
