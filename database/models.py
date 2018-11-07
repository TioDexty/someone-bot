import datetime

import peewee

db = peewee.SqliteDatabase('someonebot.db', pragmas={'journal_mode': 'wal'})


class User(peewee.Model):
    user_id = peewee.IntegerField(primary_key=True, index=True)
    first_name = peewee.CharField()
    username = peewee.CharField(null=True)
    alias = peewee.CharField(null=True)

    class Meta:
        table_name = 'Users'
        database = db

    @classmethod
    def upsert(cls, user_obj):
        # upsert: http://docs.peewee-orm.com/en/latest/peewee/querying.html#upsert
        user = cls.replace(user_id=user_obj.id, first_name=user_obj.first_name, username=user_obj.username)
        user.save()

    @classmethod
    def upsert_many(cls, users):
        users_list = [(user.id, user.first_name, user.username) for user in users]
        with cls._meta.database.atomic():
            # upsert: http://docs.peewee-orm.com/en/latest/peewee/querying.html#upsert
            (
                cls.insert_many(users_list, fields=(cls.user_id, cls.first_name, cls.username))
                .on_conflict_replace()
                .execute()
            )


class Member(peewee.Model):
    chat_id = peewee.IntegerField()
    user_id = peewee.ForeignKeyField(User, backref='members')
    last_activity = peewee.DateField(default=datetime.datetime.now)

    class Meta:
        table_name = 'Members'
        database = db
        primary_key = peewee.CompositeKey('chat_id', 'user_id')
        indexes = ((('chat_id', 'user_id'), True),)

    @classmethod
    def upsert(cls, chat_id, user_obj):
        # upsert: http://docs.peewee-orm.com/en/latest/peewee/querying.html#upsert
        user = cls.replace(chat_id=chat_id, user_id=user_obj.id, last_activity=datetime.datetime.now())
        user.save()

    @classmethod
    def upsert_many(cls, chat_id, users):
        now = datetime.datetime.now()
        users_list = [(chat_id, user.id, user.first_name, now) for user in users]
        with cls._meta.database.atomic():
            # upsert: http://docs.peewee-orm.com/en/latest/peewee/querying.html#upsert
            (
                cls.insert_many(users_list, fields=(cls.chat_id, cls.user_id, cls.last_activity))
                .on_conflict_replace()
                .execute()
            )



