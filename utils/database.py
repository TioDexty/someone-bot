import logging
import sqlite3
from contextlib import contextmanager

import utils.sql as sql

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, file_path, autocommit=True):
        self.filepath = file_path
        self.autocommit = autocommit
        self.__init_db()

    def __init_db(self):
        logger.info('__init_db')
        self.__execute(sql.CREATE_TABLE_CHATSUSERS)
        self.__execute(sql.CREATE_TABLE_USERS)

    @contextmanager
    def _conn(self):
        conn = sqlite3.connect(self.filepath)
        yield conn
        conn.commit()
        conn.close()

    def __execute(self, statement, params=(), many=False, **kwargs):
        logger.info('_execute; many: %s', many)

        result = None
        with self._conn() as conn:
            cursor = conn.cursor()

            if many:
                cursor.executemany(statement, params)
            else:
                cursor.execute(statement, params)

            if kwargs.get('fetchall', False):
                result = cursor.fetchall()
            elif kwargs.get('fetchone', False):
                result = cursor.fetchone()
            elif kwargs.get('rowcount', False):
                result = cursor.rowcount

            # conn.commit()

        return result

    @staticmethod
    def __prepare_users_list(users, chat_id=None):
        if not isinstance(users, list):
            users = [users]

        if chat_id:
            return tuple((chat_id, user.id) for user in users)
        else:
            return tuple((user.id, user.first_name[:161], user.username) for user in users)

    def save_users(self, chat_id, user_objects):
        logger.info('saving users')

        users_users = self.__prepare_users_list(user_objects)
        users_chats = self.__prepare_users_list(user_objects, chat_id=chat_id)

        rowcount = self.__execute(sql.INSERT_USER, users_users, many=True, rowcount=True)
        logger.info('inserted %d rows', rowcount)
        rowcount = self.__execute(sql.INSERT_CHAT_USER, users_chats, many=True, rowcount=True)
        logger.info('inserted %d rows', rowcount)

    def save_user(self, user_object):
        logger.info('saving single user')

        user = self.__prepare_users_list(user_object)
        self.__execute(sql.INSERT_USER, user[0])

    def remove_user(self, chat_id, user_object):
        logger.info('removing user')

        params = (chat_id, user_object.id)

        self.__execute(sql.REMOVE_USER, params)

    def get_active_users(self, chat_id, weeks=3):
        logger.info('getting active users')

        return self.__execute(sql.GET_ACTIVE_USERS.format(weeks * 7), (chat_id,), fetchall=True)

    def set_alias(self, user_id, alias=None):  # used to remove aliases too. If 'alias' is None, it will be set to NULL
        logger.info('setting alias for %d', user_id)

        self.__execute(sql.SET_ALIAS, (alias, user_id))

    def get_alias(self, user_id):
        logger.info('getting alias for %d', user_id)

        row = self.__execute(sql.GET_ALIAS, (user_id,), fetchone=True)
        return row[0]
