WSQluse - фреймворк на основе psycopg2, используемые в микросервисах проекта Watchman

1.3:
Исправлено поведение метода try_execute_get, когда метод get_table_dict запрашивает у него записи и названия полей,
а транзакция проваливается, try_execute_get все равно возвращал status='succes', с кривыми данными в ключе info.