import importlib
import logging

from bot import dispatcher
from bot import updater

logging.basicConfig(format='[%(asctime)s][%(name)s] %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    logger.info('starting...')

    for modname in ('help', 'someone', 'alias', 'registeruser'):
        handlers = getattr(importlib.import_module(f'handlers.{modname}'), 'HANDLERS')
        logger.info('module imported: %s (handlers: %d)', modname, len(handlers))
        for handler in handlers:
            dispatcher.add_handler(handler)

    updater.start_polling(clean=True)
    updater.idle()


if __name__ == '__main__':
    main()
