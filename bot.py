from telegram.ext import Updater, CommandHandler
from emoji import emojize
from source import order_details,list_order_today
import os,logging

API_TELEGRAM_NMPEDIDOBOT_TOKEN = os.environ.get('API_TELEGRAM_NMPEDIDOBOT_TOKEN')


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)

def pedido_detalhe(num_ped):
    order_detail = order_details(num_ped)
    dolar = emojize(":dollar:", use_aliases=True)
    pedido = emojize(":pencil:", use_aliases=True)
    cliente = emojize(":dog:", use_aliases=True)
    envio = emojize(":package:", use_aliases=True)
    forma_pagamento = emojize(":moneybag:", use_aliases=True)
    caption = (
        " "+pedido+" -> "+str(num_ped)+"\n"
        " "+cliente+" -> "+order_detail[0]['cliente']+"\n"
        " "+envio+" -> "+order_detail[0]['envio']+"\n"
        " "+forma_pagamento+" -> "+order_detail[0]['forma_pagamento']+"\n"
        " "+dolar+" -> "+order_detail[0]['valor_total']+"\n"
    )
    return caption

def detalhe(bot,update,args):
    order_id = ' '.join(args)
    caption=pedido_detalhe(order_id)
    bot.send_message(chat_id=update.message.chat_id,text=caption)

def start(bot, update):
    """Envia a mensagem quando o comando /start é executado"""
    smile = emojize(":smile:", use_aliases=True)

    start_message = (
        "Bem vindo ao NMPedidoBot "+smile+"\n\n"
        "O objetivo deste bot verifica se tem novos pedidos na loja integrada.\n"
        "Consulte o /help para saber como configurar o bot"

    )
    update.message.reply_text(start_message)

def help(bot, update):
    smile = emojize(":smile:", use_aliases=True)
    clock = emojize(":clock10:", use_aliases=True)
    cancel= emojize(":x:", use_aliases=True)
    look= emojize(":mag:", use_aliases=True)
    help_message = (
        "Bem vindo ao help do NMPedidoBot "+smile+"\n\n"
        "Abaixo nos mostramos os comandos que vc pode usar para configurar o bot\n\n"
        ""+clock+" /set <segundos> para configurar o intervalo de atualizacoes.\n\n"
        ""+cancel+" /unset para cancelar a atualizacao.\n\n"
        ""+look+" /detalhe <numero_pedido> para saber mais detalhe do pedido.\n"

    )
    update.message.reply_text(help_message)

def alarm(bot, job):
    orders_numbers=list_order_today() #pega a lista dos pedidos do dia
    if(len(orders_numbers)!=0):# tem pedido?
        for order_number in orders_numbers: # sim, exibe os pedidos
            text = pedido_detalhe(order_number['ID'])
            bot.send_message(job.context, text=text)
    else:
        bot.send_message(job.context, text='Sem novos pedidos')# nao tem

def set_timer(bot, update, args, job_queue, chat_data):
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        due = int(args[0])
        if due < 0:
            update.message.reply_text('Sinto muito, mas ainda nao podemos viajar no tempo')
            return

        # Add job to queue
        job = job_queue.run_repeating(alarm, due, context=chat_id)
        chat_data['job'] = job
        check = emojize(":white_check_mark:", use_aliases=True)
        update.message.reply_text('Intervalo das notificacoes setado com sucesso '+check+'')

    except (IndexError, ValueError):
        update.message.reply_text('Exemplo: /set <seconds>')


def unset(bot, update, chat_data):
    """Remove the job if the user changed their mind."""
    if 'job' not in chat_data:
        update.message.reply_text('Sem notificacoes ativadas')
        return

    job = chat_data['job']
    job.schedule_removal()
    del chat_data['job']
    check = emojize(":white_check_mark:", use_aliases=True)
    update.message.reply_text('Notificacao cancelada com sucesso'+check+'')


def bot_main():
    updater = Updater(API_TELEGRAM_NMPEDIDOBOT_TOKEN) # Token dado pelo BotFather
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start)) # Manipulador de comandos
    dp.add_handler(CommandHandler("help", help)) # Manipulador de comandos
    dp.add_handler(CommandHandler("detalhe",detalhe,pass_args=True)) # Manipulador de comandos
    dp.add_handler(CommandHandler("set", set_timer,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("unset", unset, pass_chat_data=True))

    updater.start_polling() #Inicia o loop de execução do bot
    updater.idle()

if __name__ == '__main__':
    bot_main()
