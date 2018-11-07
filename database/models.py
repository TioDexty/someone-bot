import logging
import datetime

import peewee

logger = logging.getLogger(__name__)

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
        cls.replace(user_id=user_obj.id, first_name=user_obj.first_name, username=user_obj.username).execute()

    @classmethod
    def upsert_and_get(cls, user_obj):
        user, created = cls.get_or_create(
            user_id=user_obj.id,
            defaults={'first_name': user_obj.first_name, 'username': user_obj.username}
        )
        if not created:  # user was already saved: we update their metadata
            user.first_name, user.username = user_obj.first_name, user_obj.username
            user.save()

        return user


class Member(peewee.Model):
    chat_id = peewee.IntegerField()
    user = peewee.ForeignKeyField(User, backref='members')
    last_activity = peewee.DateField(default=datetime.datetime.now)

    class Meta:
        table_name = 'Members'
        database = db
        primary_key = peewee.CompositeKey('chat_id', 'user')
        indexes = ((('chat_id', 'user_id'), True),)

    @classmethod
    def upsert(cls, chat_id, user_obj):
        user = User.upsert_and_get(user_obj)
        # upsert: http://docs.peewee-orm.com/en/latest/peewee/querying.html#upsert
        cls.replace(chat_id=chat_id, user=user, last_activity=datetime.datetime.now()).execute()

    @classmethod
    def upsert_many(cls, chat_id, users):
        now = datetime.datetime.now()
        for usert_object in users:
            user = User.upsert_and_get(usert_object)
            # now upsert the new member
            cls.replace(chat_id=chat_id, user=user, last_activity=now).execute()

    @classmethod
    def get_active(cls, chat_id, days_delta=21, limit=200):
        now = datetime.datetime.now()
        delta = datetime.timedelta(days=days_delta)
        active_from = now - delta

        return (
            cls
            .select()
            .join(User, on=(cls.user == User.user_id))
            .where(cls.chat_id == chat_id, cls.last_activity > active_from)
            .order_by(cls.last_activity.desc())
            .limit(limit)
        )



