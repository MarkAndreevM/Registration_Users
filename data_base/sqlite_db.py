import sqlite3 as sq


# ================= ФУНКЦИЯ КОТОРАЯ БЕРЕТ ИЗ БАЗЫ ДАННЫХ ВСЕ ЗАРЕГИСТРИРОВАННЫЕ USER_ID =============================
def sql_is_user_id_in_user_ids(user_id):
    global base, cur
    base = sq.connect('registration_user.db')

    if base:
        print('Data base connected OK!')
    else:
        raise Exception('Ошибка подключения к базе данных')

    cur = base.cursor()
    return cur.execute(f'SELECT user_id FROM show_data WHERE user_id = {user_id}').fetchone()  # --> извлекает одну строку из БД из user_id (id пользователя)


# def sql_get_user_ids():
#     global base, cur
#     base = sq.connect('registration_user.db')
#
#     if base:
#         print('Data base connected OK!')
#     else:
#         raise Exception('Ошибка подключения к базе данных')
#
#     cur = base.cursor()
#     return cur.execute('SELECT user_id FROM show_data').fetchall()  # --> извлекает все строки из БД из user_id


# =========================================== СОЗДАЕМ БАЗУ ДАННЫХ =============================================


def sql_start():
    global base, cur
    base = sq.connect('registration_user.db')

    if base:
        print('Data base connected OK!')
    else:
        raise Exception('Ошибка подключения к базе данных')

    cur = base.cursor()
    base.execute(
        'CREATE TABLE IF NOT EXISTS show_data(user_id INT, img VARCHAR, name VARCHAR(64), age INT, skills TEXT, phone INT)')
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO show_data VALUES (?,?,?,?,?,?)', tuple(data.values()))
        base.commit()

        with open('log.txt', 'a', encoding='utf-8') as file:
            file.write(f"\n\n'Добавлен новый пользователь' \n\n"
                       f"Имя - {data.get('name')}\n"
                       f"Возраст - {data.get('age')}\n"
                       f"Навыки - {data.get('skills')}\n"
                       f"Номер телефона - {data.get('phone')}\n")
