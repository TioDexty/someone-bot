CREATE_TABLE_USERS = """CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY,
    first_name NVARCHAR(256),
    username NVARCHAR(32),
    alias NVARCHAR(256)
);"""

CREATE_TABLE_CHATSUSERS = """CREATE TABLE IF NOT EXISTS ChatsUsers (
    chat_id INTEGER,
    user_id INTEGER,
    last_activity DATETIME,
    PRIMARY KEY (chat_id, user_id),
    FOREIGN KEY(user_id) REFERENCES Users(user_id)
);"""

INSERT_USER = """INSERT OR REPLACE INTO Users (user_id, first_name, username)
VALUES (?, ?, ?);"""

INSERT_CHAT_USER = """INSERT OR REPLACE INTO ChatsUsers (chat_id, user_id, last_activity)
VALUES (?, ?, DATETIME('now'));"""

REMOVE_USER = """DELETE
FROM ChatsUsers
WHERE chat_id = ? AND user_id = ?;"""

GET_ACTIVE_USERS = """SELECT u.*
FROM ChatsUsers AS cu
    LEFT JOIN Users AS u
        ON cu.user_id = u.user_id
WHERE cu.chat_id = ?
AND cu.last_activity > datetime('now', '-{} days');"""

SET_ALIAS = """UPDATE Users
SET alias = ?
WHERE user_id = ?;"""

GET_ALIAS = """SELECT alias
FROM Users
WHERE user_id = ?;"""
