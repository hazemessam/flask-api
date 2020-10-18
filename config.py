from platform import system

ENV = 'development'
DEBUG = True
PORT = 500
localhost = '172.25.160.1' if system() == 'Linux' else '127.0.0.1'
SQLALCHEMY_DATABASE_URI = f'postgres://root:toor@{localhost}:5432/testdb'
SQLALCHEMY_TRACK_MODIFICATIONS = False