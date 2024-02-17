CREATE_USER_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS users(
ID INTEGER PRIMARY KEY,
TELEGRAM_ID INTEGER,
USERNAME CHAR(125),
FIRST_NAME CHAR(125),
LAST_NAME CHAR(125),
UNIQUE (TELEGRAM_ID)
)
"""

INSERT_USER_QUERY = """
INSERT INTO users VALUES (?, ?, ?, ?, ?)
"""

CREATE_ANSWER_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS answers(
ID INTEGER PRIMARY KEY,
TELEGRAM_ID INTEGER,
ANSWER CHAR(50),
FOREIGN KEY (TELEGRAM_ID) REFERENCES users(TELEGRAM_ID)
)
"""

INSERT_ANSWER_QUERY = """
INSERT INTO answers (TELEGRAM_ID, ANSWER) VALUES ( ?, ?)
"""

CREATE_BAN_USER_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS ban_users(
ID INTEGER PRIMARY KEY,
TELEGRAM_ID INTEGER,
COUNT_WARNINGS INTEGER,
UNIQUE (TELEGRAM_ID)
)
"""

INSERT_BAN_USER_TABLE_QUERY = """
INSERT INTO ban_users VALUES (?, ?, ?)
"""

SELECT_BAN_USER_TABLE_QUERY = """
SELECT * FROM ban_users WHERE TELEGRAM_ID = ?
"""

UPDATE_BAN_USER_COUNT_QUERY = """
UPDATE ban_users SET COUNT_WARNINGS = COUNT_WARNINGS + 1 WHERE TELEGRAM_ID = ?
"""

CREATE_USER_FORM_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS user_form (
ID INTEGER PRIMARY KEY,
TELEGRAM_ID INTEGER,
NICKNAME CHAR(50),
BIOGRAPHY TEXT,
LOCATION TEXT,
GENDER CHAR(50),
AGE INTEGER,
PHOTO TEXT,
UNIQUE (TELEGRAM_ID)
)
"""

INSERT_USER_FORM_TABLE_QUERY = """
INSERT INTO user_form VALUES (?, ?, ?, ?, ?, ?, ?, ?)
"""

SELECT_USER_FORM_QUERY = """
SELECT * FROM user_form WHERE TELEGRAM_ID = ?
"""

SELECT_ALL_USER_FORM_QUERY = """
SELECT * FROM user_form 
"""

CREATE_LIKE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS like_forms (
ID INTEGER PRIMARY KEY,
OWNER_TELEGRAM_ID INTEGER,
LIKER_TELEGRAM_ID INTEGER,
UNIQUE (OWNER_TELEGRAM_ID, LIKER_TELEGRAM_ID)
)
"""

INSERT_LIKE_QUERY = """
INSERT INTO like_forms  VALUES (?, ?, ?)
"""

FILTER_LEFT_JOIN_USERFORM_LIKE_QUERY = """
SELECT * FROM user_form
LEFT JOIN like_forms ON user_form.TELEGRAM_ID = like_forms.OWNER_TELEGRAM_ID
AND like_forms.LIKER_TELEGRAM_ID = ?
WHERE like_forms.ID IS NULL 
AND user_form.TELEGRAM_ID != ?
"""