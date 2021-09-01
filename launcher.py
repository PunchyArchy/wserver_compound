""" Запустить WServer, извлекая из переменной окружения данные для доступа
к GDB."""


from wserver_compound.main import WServer
import os

dbname = os.environ.get('GDBNAME')
dbuser = os.environ.get('GDBUSER')
dbpass = os.environ.get('GDBPASS')
dbhost = os.environ.get('GDBHOST')

inst = WServer(8888, dbname=dbname, dbuser=dbuser, dbpass=dbpass,
               dbhost=dbhost)
inst.start()
