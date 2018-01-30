from telegram.ext import Updater, CommandHandler
from emoji import emojize
from source import order_details,list_order_today
import os,logging

API_TELEGRAM_NMPEDIDOBOT_TOKEN = os.environ.get('API_TELEGRAM_NMPEDIDOBOT_TOKEN')


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)

def detalhe(bot,update,args):
    order_id = ' '.join(args)
    order_detail = order_details(order_id)
    dolar = emojize(":dollar:", use_aliases=True)
    pedido = emojize(":pencil:", use_aliases=True)
    cliente = emojize(":dog:", use_aliases=True)
    envio = emojize(":package:", use_aliases=True)
    forma_pagamento = emojize(":moneybag:", use_aliases=True)
    caption = (
        " "+pedido+" -> "+order_id+"\n"
        " "+cliente+" -> "+order_detail[0]['cliente']+"\n"
        " "+envio+" -> "+order_detail[0]['envio']+"\n"
        " "+forma_pagamento+" -> "+order_detail[0]['forma_pagamento']+"\n"
        " "+dolar+" -> "+order_detail[0]['valor_total']+"\n"
    )
    bot.send_message(chat_id=update.message.chat_id,text=caption)

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

def callback_minute(bot,update,job):
        bot.send_message(chat_id=update.message.chat_id,text='One message every minute')
# def search_order_loop(bot,job):
#     orders = list_order_today()
#     for order in orders:
#         bot.send_message(chat_id='@NMPedidosBot',text="pedido!")

def bot_main():
    updater = Updater(API_TELEGRAM_NMPEDIDOBOT_TOKEN) # Token dado pelo BotFather
    dp = updater.dispatcher
    j = dp.job_queue
    dp.add_handler(CommandHandler("start", start)) # Manipulador de comandos
    dp.add_handler(CommandHandler("help", help)) # Manipulador de comandos
    dp.add_handler(CommandHandler("detalhe",detalhe,pass_args=True)) # Manipulador de comandos
    j.run_repeating(callback_minute, interval=10, first=0)
    updater.start_polling() #Inicia o loop de execução do bot
    updater.idle()

if __name__ == '__main__':
    bot_main()
