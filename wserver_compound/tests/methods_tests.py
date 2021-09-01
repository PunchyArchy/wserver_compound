""" Тесты модуля с функционалом """
import unittest
import uuid
from wserver_compound import settings
from wserver_compound import methods
from wserver_compound import functions
from wserver_compound.tests.test_objects import test_sql_shell


class FunctionsTest(unittest.TestCase):
    """ Класс TestCase, тестирующий все методы WServer.
    После внесения данных в БД и проверки корректности - удаляет запись. """

    def test_set_auto(self):
        """ Тестирование функции добавления нового авто в GDB """
        car_number = str(uuid.uuid4())[:9]
        response_success = methods.set_auto(test_sql_shell,
                                            car_number=car_number,
                                            polygon=9,
                                            id_type='rfid',
                                            rg_weight=0,
                                            rfid='SAF')

        self.assertTrue(response_success['status'])
        response_fail = methods.set_auto(test_sql_shell,
                                         car_number=car_number,
                                         polygon=9,
                                         id_type='rfid',
                                         rg_weight=0,
                                         rfid='SAF')
        self.assertTrue(not response_fail['status'])
        methods.delete_record(test_sql_shell, 'id',
                              response_success['info'],
                              'auto')

    def test_set_act(self):
        """ Тестирование функции добавления нового акта """
        response = methods.set_act(test_sql_shell, 466961,
                                   gross=13000, tare=8000, cargo=5000,
                                   time_in='2021.08.24 14:33:39',
                                   time_out='2099.08.24 21:22:19',
                                   carrier_id=None,
                                   trash_cat_id=4, trash_type_id=4,
                                   polygon_id=1, operator=22, ex_id=1488)
        self.assertTrue(response['status'] and int(response['info']))
        methods.delete_record(test_sql_shell, 'id', response['info'],
                              'records')

    def test_set_photo(self):
        """ Тесты сохранения фотографии на винте """
        photo_obj = functions.encode_photo(settings.TEST_PHOTO)
        photo_obj = str(photo_obj)
        result = methods.set_photos(test_sql_shell, None, photo_obj, None)
        self.assertTrue(result['status'],
                        isinstance(result['info'], int))
        methods.delete_record(test_sql_shell, 'id', result['info'],
                              'act_photos')

    def test_add_note(self):
        """ Тестирование добавления комментария к заезду """
        result = methods.add_operator_notes(test_sql_shell, None, 'TEST_NOTE',
                                            1)
        self.assertTrue(result['status'],
                        isinstance(result['info'], int))
        methods.delete_record(test_sql_shell, 'id', result['info'],
                              'operator_notes')

    def test_set_company(self):
        """ Тетстирование добавления новой компании-перевозчика """
        result = methods.set_company(test_sql_shell, 'TEST_COMPANY', '123',
                                     9, None, True, None)
        self.assertTrue(result['status'],
                        isinstance(result['info'], int))
        methods.delete_record(test_sql_shell, 'id', result['info'],
                              'companies')

    def test_set_trash_cat(self):
        """ Тетстирование добавления новой компании-перевозчика """
        result = methods.set_trash_cat(test_sql_shell, 'TEST_TRASH_CAT',
                                       polygon=9)
        self.assertTrue(result['status'] and
                        isinstance(result['info'], int) or not result[
            'status'])
        methods.delete_record(test_sql_shell, 'id', result['info'],
                              'trash_cats')

    def test_set_trash_type(self):
        """ Тетстирование добавления новой компании-перевозчика """
        result = methods.set_trash_type(test_sql_shell, 'TEST_TRASH_NAME',
                                        trash_cat_id=None,
                                        polygon=9)
        self.assertTrue(result['status'],
                        isinstance(result['info'], int))
        methods.delete_record(test_sql_shell, 'id', result['info'],
                              'trash_types')

    def test_set_operator(self):
        result = methods.set_operator(test_sql_shell, 'FIO', 'LOGIN', 'pw',
                                      polygon=None)
        self.assertTrue(result['status'] and
                        isinstance(result['info'], int))
        methods.delete_record(test_sql_shell, 'id', result['info'],
                              'operators')

    def test_add_rfid(self):
        random_rfid = str(uuid.uuid4())[:10]
        result_success = methods.add_rfid(test_sql_shell,
                                          rfid_num=random_rfid,
                                          rfid_type=1,
                                          owner=9)
        self.assertTrue(result_success['status'])
        result_failed = methods.add_rfid(test_sql_shell,
                                         rfid_num=random_rfid,
                                         rfid_type=1,
                                         owner=9)
        self.assertTrue(not result_failed['status'])
        methods.delete_record(test_sql_shell, 'id',
                              result_success['info'],
                              'rfid_marks')

    def test_get_auto_id(self):
        car_number = '450f58f3-'
        response = methods.get_auto_id(test_sql_shell, car_number)
        self.assertTrue(isinstance(response, int))
        response = methods.get_auto_id(test_sql_shell, '00000')
        self.assertTrue(not response)

    def test_get_company_id(self):
        company_name = 'test_company_1'
        response = methods.get_company_id(test_sql_shell, company_name)
        self.assertTrue(isinstance(response, int))

    def test_get_rfid(self):
        res = methods.get_rfid_id(test_sql_shell, 'FFFF000160')
        self.assertTrue(isinstance(res, int))
        res_fail = methods.get_rfid_id(test_sql_shell,
                                       'a00240sf')
        self.assertTrue(not res_fail)


if __name__ == '__main__':
    unittest.main()
