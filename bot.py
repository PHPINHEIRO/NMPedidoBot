from source import order_details,list_order_today
import os,logging
from telegram.ext import Updater, CommandHandler
from emoji import emojize

API_TELEGRAM_NMPEDIDOBOT_TOKEN = os.environ.get('API_TELEGRAM_NMPEDIDOBOT_TOKEN')


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)

def start(bot, update):
    """Envia a mensagem quando o comando /start é executado"""
    smile = emojize(":smile:", use_aliases=True)
    clapper = emojize(":clapper:", use_aliases=True)
    film_frames = emojize(":film_frames:", use_aliases=True)
    movie_camera = emojize(":movie_camera:", use_aliases=True)
    popcorn = emojize(":popcorn:", use_aliases=True)

    start_message = (
        "Cineasta "+update.message.from_user.first_name+" bem vindo!"+smile+"\n\n"
        ""+clapper+"Esse bot lhe ajudará a encontrar informações sobre seus filmes favoritos."+film_frames+movie_camera+"\n\n"
        "Pegue a sua "+popcorn+" e vamos nos aventurar no mundo cinematográfico.\n\n"
        "Para mais informações digite /help\n\n\n"
        "Qual filme gostaria de procurar?"

    )
    update.message.reply_text(start_message)

def help(bot, update):

    help_message = (

        "Assim que o bot eh iniciado, vc ja pode fazer pesquisas de filmes.\n\n"
        "Basta digitar o nome do filme que vc deseja pesquisas.\n\n"

    )
    update.message.reply_text(help_message)

def bot_main():
    updater = Updater(API_TELEGRAM_NMPEDIDOBOT_TOKEN) # Token dado pelo BotFather
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start)) # Manipulador de comandos
    dp.add_handler(CommandHandler("help", help)) # Manipulador de comandos
    # dp.add_handler(CommandHandler("/procurar", show_movie_list,pass_args=True,pass_job_queue=True,pass_chat_data=True))
    # dp.add_handler(MessageHandler(Filters.text, show_movie_list))
    # dp.add_handler(MessageHandler(Filters.text, show_movie_info))

    updater.start_polling() #Inicia o loop de execução do bot
    updater.idle()

if __name__ == '__main__':
    bot_main()
