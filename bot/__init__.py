import os

from .utils import utils
from .bot import TorrentsBot
from .database import Database
from config import config


torrentsbot = TorrentsBot(
    token=os.environ.get('TELEGRAM_TOKEN', None) or config.telegram.token,
    workers=0,
    use_context=True
)
db = Database(config.sqlite.filename)


def main():
    utils.load_logging_config('logging.json')

    torrentsbot.import_handlers(r'bot/handlers/')
    torrentsbot.run(clean=True, jobs_enabled=config.feedsjob.enabled)


if __name__ == '__main__':
    main()
