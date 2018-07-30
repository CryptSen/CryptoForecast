# -*- coding: utf-8 -*-
"""Application configuration.

See https://github.com/sloria/cookiecutter-flask for configuration options with other flask-extensions
"""
import os
from google.cloud import datastore

datastore = datastore.Client.from_service_account_json('kryptos-stage-a7f9fd94cd62.json')



def get_from_datastore(config_key):
    print('Fetching {}'.format(config_key))

    product_key = datastore.key('Settings', 'production')
    entity = datastore.get(product_key)

    # print(value['SQLALCHEMY_DATABASE_URI'])
    return entity[config_key]




class Config(object):
    """Base configuration."""


    SECRET_KEY = os.getenv("KRYPTOS_SECRET", "secret-key")  # TODO: Change me
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    # PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REDIS_HOST = get_from_datastore('REDIS_HOST')
    RQ_POLL_INTERVAL = 1000

    # Google Cloud Project ID. This can be found on the 'Overview' page at
    # https://console.developers.google.com
    PROJECT_ID = 'kryptos-204204'

    # Cloud Datastore dataset id, this is the same as your project id.
    DATASTORE_DATASET_ID = PROJECT_ID

    MIGRATIONS_DIR = os.path.join(APP_DIR, 'models', 'migrations')

    # Flask-Assistant options
    CLIENT_ACCESS_TOKEN = get_from_datastore("CLIENT_ACCESS_TOKEN")
    DEV_ACCESS_TOKEN = get_from_datastore("DEV_ACCESS_TOKEN")



    # Flask-Mail SMTP server settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'hello@produvia.com'
    MAIL_PASSWORD = get_from_datastore('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = '"Kryptos AI" <noreply@example.com>'

    # Flask-User settings
    USER_APP_NAME = "Kryptos AI"  # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = True        # Enable email authentication
    USER_ENABLE_USERNAME = False    # Disable username authentication
    USER_ENABLE_CONFIRM_EMAIL = True
    USER_SEND_REGISTERED_EMAIL = True
    USER_AFTER_REGISTER_ENDPOINT = 'account.user_account'
    USER_AFTER_CONFIRM_ENDPOINT = 'account.user_account'
    USER_AFTER_LOGIN_ENDPOINT = 'account.user_account'
    USER_ENABLE_CONFIRM_EMAIL = False


class ProdConfig(Config):
    """Production configuration."""

    ENV = "prod"
    DEBUG = False
    FRONTEND_URL = "http://kryptos.produvia.com"
    API_URL = "http://web:5000/api"
    TELEGRAM_BOT = 'KryptosAIBot'
    SQLALCHEMY_DATABASE_URI = get_from_datastore('SQLALCHEMY_DATABASE_URI')
    TELEGRAM_TOKEN = get_from_datastore('TELEGRAM_TOKEN')

class DockerDevConfig(Config):
    ENV = "docker-dev"
    DEBUG = True
    BASE_URL = os.getenv('NGROK_URL', 'http://0.0.0.0:5000/')
    FRONTEND_URL = BASE_URL
    API_URL = "http://web:5000/api"
    USER_ENABLE_CONFIRM_EMAIL = False
    USER_SEND_REGISTERED_EMAIL = True
    TELEGRAM_BOT = 'kryptos_dev_bot'
    MAIL_USERNAME = 'testkryptos123@gmail.com'
    MAIL_PASSWORD = 'lulxeqhsnlbnsjyd'


class DevConfig(Config):
    """Development configuration."""

    ENV = "dev"
    DEBUG = True
    BASE_URL = os.getenv('NGROK_URL', 'http://0.0.0.0:5000/')
    FRONTEND_URL = BASE_URL
    API_URL = os.path.join(BASE_URL, 'api')
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/kryptos'
    # SQLALCHEMY_DATABASE_URI= 'postgresql+psycopg2://postgres:ssBB8jz1iDhCE7v2@127.0.0.1:5432/kryptos'

    USER_ENABLE_CONFIRM_EMAIL = False
    TELEGRAM_BOT = 'kryptos_dev_bot'
    REDIS_HOST = 'localhost'
    MAIL_USERNAME = 'testkryptos123@gmail.com'
    MAIL_PASSWORD = 'lulxeqhsnlbnsjyd'
    # SQLALCHEMY_ECHO = True


class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/testkryptos'
