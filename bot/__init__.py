from .utils import utils
from .bot import TorrentsBot
from .database import Database
from config import config


torrentsbot = TorrentsBot(token=config.telegram.token, use_context=True)
db = Database(config.sqlite.filename)


def main():
    utils.load_logging_config('logging.json')

    torrentsbot.import_handlers(r'bot/handlers/')
    torrentsbot.run(clean=True)


if __name__ == '__main__':
    main()
