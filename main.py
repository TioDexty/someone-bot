import importlib
import logging

from bot import dispatcher
from bot import updater

logging.basicConfig(format='[%(asctime)s][%(name)s] %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    logger.info('starting...')

    for modname in ('help', 'someone', 'alias', 'registeruser'):
        module = getattr(importlib.import_module(f'modules.{modname}'), 'module')
        logger.info('module imported: %s (handlers: %d)', module.name, len(module.handlers))
        for handler in module.handlers:
            dispatcher.add_handler(handler)

    updater.start_polling(clean=True)
    updater.idle()


if __name__ == '__main__':
    main()
