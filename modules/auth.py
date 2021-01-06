import db_worker


db = db_worker.SQLighter('db/users.db')


def login(login, password):
    try:
        user = db.select("select * from users where login = ?", (login, ))
        if user == []:
            return False
        else:
            if password == user[2]:
                return True
            else:
                return False
    except:
        return False


def reg(login, password):
    try:
        user = db.select("select * from users where login = ?", (login, ))
        if user == []:
            db.execute("insert into users (login, password) values (?, ?)", (login, password))
            return True
        else:
            return False
    except:
        return False