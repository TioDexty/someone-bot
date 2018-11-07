from .models import db
from .models import User, Member


def create_tables():
    with db:
        db.create_tables([User, Member])


create_tables()
