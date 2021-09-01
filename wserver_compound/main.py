""" Модуль содержит основной класс WServer """
from qpi.main import QPI
from wserver_compound import methods
from wsqluse.wsqluse import Wsqluse


class WServer(Wsqluse):
    """ Класс WServer. С помощью QPI принимает клиентов,
    выполняет их команды, взаимодействуя с базой данных (GDB, global data base)
    """

    def __init__(self, port, *args, **kwargs):
        super(WServer, self).__init__(*args, **kwargs)
        """
        Инициация WServer

        :param port: порт, на котором он будет ожидать клиентов
        :pself (wsqluse) для подключения к GDB
        """
        self.qpi = QPI('0.0.0.0', port, self,
                       without_auth=True, auto_start=True,
                       mark_disconnect=False, name='WServer QPI')

    def start(self):
        while True:
            pass

    def get_api_support_methods(self):
        """ Открыть методы для QPI. """
        api_methods = {'set_act': {'method': self.set_act},
                       'set_auto': {'method': self.set_auto},
                       'set_photos': {'method': self.set_photos},
                       'set_notes': {'method': self.add_operator_notes},
                       'set_company': {'method': self.set_company},
                       'get_auto_id': {'method': self.get_auto_id},
                       'get_company_id': {'method': self.get_company_id},
                       'set_operator': {'method': self.set_operator},
                       'set_trash_cat': {'method': self.set_trash_cat},
                       'set_trash_type': {'method': self.set_trash_type}
                       }
        return api_methods

    def set_act(self, auto_id, gross, tare, cargo,
                time_in, time_out,
                carrier_id, trash_cat_id, trash_type_id,
                polygon_id, operator, ex_id, *args, **kwargs):
        """
        Добавить новый акт на WServer.k

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
                {'status': True, 'info': *id: int*)
            В случае провала:
                {'status': False, 'info': Python Traceback}
        """
        response = methods.set_act(self, auto_id, gross, tare, cargo,
                                   time_in, time_out,
                                   carrier_id, trash_cat_id, trash_type_id,
                                   polygon_id, operator, ex_id)
        return response

    def set_auto(self, car_number, polygon, id_type, rg_weight, model, rfid_id,
                 *args, **kwargs):
        """
        Добавить новое авто в GDB

        :param car_number: Гос. номер
        :param polygon: Полигон, за которым закреплено авто, если авто
            передвигается по всему региону, его стоит закрепить за РО.
        :param id_type: Протокол авто (rfid, NEG, tails)
        :param rg_weight: Справочный вес (тара)
        :param model: ID модели авто из gdb.auto_models
        :param rfid_id: ID RFID метки из gdb.rfid_marks
        :return:
            В случае успеха:
                {'status': True, 'info': *id: int*)
            В случае провала:
                {'status': False, 'info': Python Traceback}
        """
        response = methods.set_auto(self, car_number, polygon,
                                    id_type, rg_weight, model, rfid_id)
        return response

    def set_photos(self, record: int, photo_obj: str, photo_type: int,
                   *args, **kwargs):
        """
        Сохранить фотографии на WServer.

        :param record: ID заезда
        :param photo_obj: Объект фото в кодировке base64, но в виде строки
        :param photo_type: Тип фотографии (gdb.photo_types)
        :return:
            В случае успеха:
                {'status': True, 'info': *id: int*)
            В случае провала:
                {'status': False, 'info': Python Traceback}
        """
        return methods.set_photos(self, record, photo_obj,
                                  photo_type)

    def add_operator_notes(self, record, note, note_type, *args, **kwargs):
        """
        Добавить комментарии весовщика к заезду.

        :param record: ID заезда
        :param note: Комментарий
        :param note_type: Тип комментария (при брутто, добавочный и т.д.)
        :return:
            В случае успеха:
                {'status': True, 'info': *id: int*)
            В случае провала:
                {'status': False, 'info': Python Traceback}
        """
        return methods.add_operator_notes(self, record, note, note_type)

    def set_company(self, name, inn, kpp,
                    polygon, status, ex_id,
                    active, *args, **kwargs):
        """
         Добавить нового перевозчика.

         :param name: Название перевозчика.
         :param inn: ИНН перевозчика.
         :param kpp: КПП перевозчика.
         :param ex_id: ID перевозичка из внешней системы. (1C, например)
         :param status: Действующий или нет? True/False
         :param polygon: ID полигона.
         :param active: Запись по умолчанию активна?
         :return:
             В случае успеха:
                 {'status': True, 'info': *id: int*)
             В случае провала:
                 {'status': False, 'info': Python Traceback}
         """
        return methods.set_company(self, name, inn, kpp,
                                   polygon, status, ex_id,
                                   active)

    def set_trash_cat(self, name, polygon, active=True, *args, **kwargs):
        """
          Добавить новую категорию груза.

          :param name: Название категории груза.
          :param polygon: ID полигона.
          :param active: Запись по умолчанию активна?
          :return:
              В случае успеха:
                  {'status': True, 'info': *id: int*)
              В случае провала:Отп
                  {'status': False, 'info': Python Traceback}
          """
        return methods.set_trash_cat(self, name, polygon, active)

    def set_trash_type(self, name: str, polygon: int, category: int = None,
                       active: bool = True, *args, **kwargs):
        """
        Добавить новый вид груза.

        :param name: Название вида груза.
        :param category: ID категории груза, за которым этот вид закреплен.
        :param polygon: ID полигона.
        :param active: Запись по умолчанию активна?
        :return:
            В случае успеха:
                {'status': True, 'info': *id: int*)
            В случае провала:
                {'status': False, 'info': Python Traceback}
        """
        return methods.set_trash_type(self, name, category, polygon,
                                      active)

    def set_operator(self, full_name: str, login: str, password: str,
                     polygon: int, active: bool = True, *args, **kwargs):
        """
        Добавить нового весовщика.

        :param full_name: Полное имя весовщика (ФИО).
        :param login: Логин пользователя.
        :param password: Пароль пользователя.
        :param polygon: ID полигона, за которым закреплен весовщик.
        :param active: Запись по умолчанию активна?
        :return:
            В случае успеха:
                {'status': True, 'info': *id: int*)
            В случае провала:
                {'status': False, 'info': Python Traceback}
        """
        return methods.set_operator(self, full_name, login, password,
                                    polygon, active)

    def get_auto_id(self, car_number: str, *args, **kwargs):
        """ Вернуть ID авто по его гос.номеру.

        :param car_number: Гос.номер авто.
        :return: ID авто. """
        return methods.get_auto_id(self, car_number)

    def get_company_id(self, company_name: str, *args, **kwargs):
        """
        Вернуть ID компании по его названию.

        :param company_name: Название компании.
        :param args:
        :param kwargs:
        :return: ID или None
        """
        return methods.get_company_id(self, company_name)
