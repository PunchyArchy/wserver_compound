""" Содержит функционал WServer.
 ВАЖНО! Здесь находятся именно features WServer, его основной функционал методов,
 а в модуле functions, находятся небольшие функции, которые необходимы для
 выполнения функционала, изложенного здесь."""

from wserver_compound import functions


@functions.send_data_to_core('auto')
@functions.format_wsqluse_response
def set_auto(sql_shell, car_number: str, polygon: int, id_type: str,
             rg_weight: int = 0, model: int = 0, rfid: str = None,
             rfid_id: int = None):
    """
    Добавить новое авто в GDB

    :param sql_shell: Объект WSQLuse для взаимодействия с GDB
    :param car_number: Гос. номер
    :param polygon: Полигон, за которым закреплено авто, если авто
        передвигается по всему региону, его стоит закрепить за РО.
    :param id_type: Протокол авто (rfid, NEG, tails)
    :param rg_weight: Справочный вес (тара)
    :param model: ID модели авто из gdb.auto_models
    :param rfid: номер RFID метки.
    :param rfid_id: id RFID метки.
    :return:
        В случае успеха:
            {'status': 'success', 'info': *id: int*)
        В случае провала:
            {'status': 'failed', 'info': Python Traceback}
    """
    if rfid and not rfid_id:
        rfid_id = functions.get_rfid_id(sql_shell, rfid)
    command = """INSERT INTO auto 
                (car_number, id_type, rg_weight, auto_model, polygon, rfid_id) 
                VALUES 
                (%s, %s, %s, %s, %s, %s)"""
    values = (car_number, id_type, rg_weight, model, polygon, rfid_id)
    response = sql_shell.try_execute_double(command, values)
    return response


@functions.format_wsqluse_response
def set_act(sql_shell, auto_id: int, gross: int, tare: int, cargo: int,
            time_in: str, time_out: str,
            carrier_id: int, trash_cat_id: int, trash_type_id: int,
            polygon_id: int, operator: int, ex_id: int):
    """
    Добавить новый акт на WServer.

    :param sql_shell: Объект WSQLuse, для взаимодействия с GDB
    :param auto_id: ID автомобиля
    :param gross: Вес-брутто
    :param tare: Вес-тара
    :param cargo: Вес-нетто
    :param time_in: Время въезда
    :param time_out: Время выезда
    :param carrier_id: ID перевозчика
    :param trash_cat_id: ID категории груза
    :param trash_type_id: ID вида груза
    :param polygon_id: ID полигона
    :param operator: ID весовщика
    :param ex_id: ID записи в wdb
    :return:
        В случае успеха:
            {'status': 'success', 'info': *id: int*)
        В случае провала:
            {'status': 'failed', 'info': Python Traceback}
    """
    command = """INSERT INTO records
                (car, brutto, tara, cargo, time_in, time_out, carrier, 
                trash_cat, trash_type, polygon, operator, ex_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s)"""
    values = (auto_id, gross, tare, cargo, time_in, time_out, carrier_id,
              trash_cat_id, trash_type_id, polygon_id, operator, ex_id)
    response = sql_shell.try_execute_double(command, values)
    return response


@functions.format_wsqluse_response
def set_photos(sql_shell, record: int, photo_obj: str, photo_type: int):
    """
    Сохранить фотографии на WServer.

    :param sql_shell: Объект WSQLuse, для взаимодействия с GDB
    :param record: ID заезда
    :param photo_obj: Объект фото в кодировке base64, но в виде строки
    :param photo_type: Тип фотографии (gdb.photo_types)
    :return:
        В случае успеха:
            {'status': 'success', 'info': *id: int*)
        В случае провала:
            {'status': 'failed', 'info': Python Traceback}
    """
    # Сгенерировать название фото
    photo_name = functions.generate_photo_name(record)
    # Сохранить фото на винте
    result = functions.save_photo(photo_obj, photo_name)
    if result:
        # Сохранить данные о фото в БД
        response = functions.save_photo_database(sql_shell, record, photo_name,
                                                 photo_type)
        return response


@functions.format_wsqluse_response
def add_operator_notes(sql_shell, record, note, note_type):
    """
    Добавить комментарии весовщика к заезду.
    :param sql_shell: Объект WSQLuse, для взаимодействия с GDB
    :param record: ID заезда
    :param note: Комментарий
    :param note_type: Тип комментария (при брутто, добавочный и т.д.)
    :return:
        В случае успеха:
            {'status': 'success', 'info': *id: int*)
        В случае провала:
            {'status': 'failed', 'info': Python Traceback}
    """
    command = """INSERT INTO operator_notes
                (record, note, type)
                VALUES (%s, %s, %s)"""
    values = (record, note, note_type)
    response = sql_shell.try_execute_double(command, values)
    return response


@functions.format_wsqluse_response
def set_company(sql_shell, name: str, inn: str, kpp: str,
                polygon: int, status: bool = True, ex_id: str = None,
                active: bool = True):
    """
    Добавить нового перевозчика.
    :param sql_shell: Объект WSQLuse, для взаимодействия с GDB.
    :param name: Название перевозчика.
    :param inn: ИНН перевозчика.
    :param kpp: КПП перевозчика.
    :param ex_id: ID перевозичка из внешней системы. (1C, например)
    :param status: Действующий или нет? True/False
    :param polygon: ID полигона.
    :param active: Запись по умолчанию активна?
    :return:
        В случае успеха:
            {'status': 'success', 'info': *id: int*)
        В случае провала:
            {'status': 'failed', 'info': Python Traceback}
    """
    command = """INSERT INTO companies
                (name, inn, kpp, ex_id, polygon, status, active)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
    values = (name, inn, kpp, ex_id, polygon, status, active)
    response = sql_shell.try_execute_double(command, values)
    return response


@functions.send_data_to_core('trash_cats')
@functions.format_wsqluse_response
def set_trash_cat(sql_shell, name, polygon, active=True):
    """
    Добавить новую категорию груза.

    :param sql_shell: Объект WSQLuse, для взаимодействия с GDB.
    :param name: Название категории груза.
    :param polygon: ID полигона.
    :param active: Запись по умолчанию активна?
    :return:
        В случае успеха:
            {'status': 'success', 'info': *id: int*)
        В случае провала:
            {'status': 'failed', 'info': Python Traceback}
    """
    command = """INSERT INTO trash_cats
                (name, polygon, active)
                VALUES (%s, %s, %s)"""
    values = (name, polygon, active)
    response = sql_shell.try_execute_double(command, values)
    return response


@functions.send_data_to_core('trash_types')
@functions.format_wsqluse_response
def set_trash_type(sql_shell, name: str, trash_cat_id: int, polygon: int,
                   active: bool = True):
    """
    Добавить новый вид груза.

    :param sql_shell: Объект WSQLuse, для взаимодействия с GDB.
    :param name: Название вида груза.
    :param trash_cat_id: ID категории груза, за которым этот вид закреплен.
    :param polygon: ID полигона.
    :param active: Запись по умолчанию активна?
    :return:
        В случае успеха:
            {'status': 'success', 'info': *id: int*)
        В случае провала:
            {'status': 'failed', 'info': Python Traceback}
    """
    command = """INSERT INTO trash_types
                (name, category, polygon, active)
                VALUES (%s, %s, %s, %s)"""
    values = (name, trash_cat_id, polygon, active)
    response = sql_shell.try_execute_double(command, values)
    return response


@functions.send_data_to_core('users')
@functions.format_wsqluse_response
def set_operator(sql_shell, full_name: str, login: str, password: str,
                 polygon: int, active: bool = True):
    """
    Добавить нового весовщика.

    :param sql_shell: Объект WSQLuse, для взаимодействия с GDB.
    :param full_name: Полное имя весовщика (ФИО).
    :param login: Логин пользователя.
    :param password: Пароль пользователя.
    :param polygon: ID полигона, за которым закреплен весовщик.
    :param active: Запись по умолчанию активна?
    :return:
        В случае успеха:
            {'status': 'success', 'info': *id: int*)
        В случае провала:
            {'status': 'failed', 'info': Python Traceback}
    """
    command = """INSERT INTO operators 
                (full_name, username, password, polygon, active)
                VALUES (%s, %s, %s, %s, %s)"""
    values = (full_name, login, password, polygon, active)
    response = sql_shell.try_execute_double(command, values)
    return response


@functions.format_wsqluse_response
def delete_record(sql_shell, column: str, value: any, table_name: str):
    """
    Удалить запись с базы данных, в которой колонке соответствует значение.

    :param sql_shell: Объект WSQLuse, для взаимодействия с GDB.
    :param column: Название колонки.
    :param value: Значение колонки.
    :param table_name: Название таблиы.
    :return:
        В случае успеха:
            {'status': 'success', 'info': *id: int*)
        В случае провала:
            {'status': 'failed', 'info': Python Traceback}
    """
    command = "DELETE FROM {} WHERE {}={}".format(table_name, column, value)
    response = sql_shell.try_execute(command)
    return response


@functions.format_wsqluse_response
def add_rfid(sql_shell, rfid_num: str, rfid_type: int, owner: int):
    """
    Добавить новую RFID метку.

    :param sql_shell: Объект WSQLuse для работы с БД.
    :param rfid_num: Номер RFID метки.
    :param rfid_type: Тип RFID метки.
    :param owner: ID владельца метки.
    :return:
    """
    command = """INSERT INTO rfid_marks (rfid, owner_id, rfid_type) 
                VALUES (%s, %s, %s)"""
    values = (rfid_num, owner, rfid_type)
    response = sql_shell.try_execute_double(command, values)
    return response


def get_auto_id(sql_shell, car_number):
    """
    Поолучить ID авто в БД GDB по его гос.номеру.

    :param sql_shell: Экземпляр wsqluse для работы с GDB.
    :param car_number: Гос. номер авто.
    :return: ID авто.
    """
    command = "SELECT id FROM auto WHERE car_number='{}'".format(car_number)
    response = sql_shell.try_execute_get(command)
    if response:
        return response[0][0]
