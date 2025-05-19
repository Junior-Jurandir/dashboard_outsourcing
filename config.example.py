import os


class Config:
    CSRF_ENABLED = True
    SECRET = "15306ba8f39d7d1adf2dca473bb5b9047d8f054f4fcb304cd947cdc719cc2b3d"
    TEMPLATE_FOLDER = os.path.join(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
    )
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    APP = None


class DevelopmentConfig(Config):
    DEBUG = True
    IP_HOST = "localhost"
    PORT_HOST = 8000
    URL_MAIN = "http://%s:%s" % (IP_HOST, PORT_HOST)  # http://localhost:8000

    # Configuração para MySQL
    DB_USER = "root"
    DB_PASSWORD = "[Sua_senha_aqui]"
    DB_HOST = "localhost"
    DB_PORT = 3306
    DB_NAME = "outsourcing_dev"
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://{}:{}@{}:{}/{}".format(
        DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
    )


class TestingConfig(Config):
    DEBUG = True
    IP_HOST = "localhost"
    PORT_HOST = 5000
    URL_MAIN = "http://%s:%s" % (IP_HOST, PORT_HOST)  # http://localhost:8000

    # Configuração para MySQL
    DB_USER = "root"
    DB_PASSWORD = "[Sua_senha_aqui]"
    DB_HOST = "localhost"
    DB_PORT = 3306
    DB_NAME = "outsourcing_test"
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://{}:{}@{}:{}/{}".format(
        DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
    )


class ProductionConfig(Config):
    IP_HOST = "127.0.0.1"  # IP ficticio, trocar posteriormente por um IP real
    PORT_HOST = 8080
    URL_MAIN = "http://%s:%s" % (IP_HOST, PORT_HOST)  # http://127.0.0.1:8080

    # Configuração para MySQL
    DB_USER = "root"
    DB_PASSWORD = "[Sua_senha_aqui]"
    DB_HOST = "localhost"
    DB_PORT = 3306
    DB_NAME = "outsourcing_prod"
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://{}:{}@{}:{}/{}".format(
        DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
    )


app_config = {
    "development": DevelopmentConfig(),
    "testing": TestingConfig(),
    "production": ProductionConfig(),
}

app_active = os.getenv("FLASK_ENV")
if app_active is None:
    app_active = "development"
