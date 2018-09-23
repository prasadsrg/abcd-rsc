class Config(object):
    """
    Common configurations
    """
    HOST = '0.0.0.0'
    PORT = 5000
    SECRET_KEY = 'p9Bv<3Eid9%$i01'
    SQLALCHEMY_DATABASE_URI = 'mysql://abcd_user:abcd!234@qa.dfftech.com:3306/abcd_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Put any configurations here that are common across all environments


class QaConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://abcd_user:abcd!234@qa.dfftech.com:3306/abcd_db'
    DEBUG = True

class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DEBUG = True
    SQLALCHEMY_ECHO = True


class MasterConfig(Config):
    """
    Production configurations
    """
    SQLALCHEMY_DATABASE_URI = 'mysql://abcd_user:abcd!234@prd.dfftech.com:3306/abcd_db'
    DEBUG = False


app_config = {
    'dev': DevelopmentConfig,
    'qa': QaConfig,
    'prd': MasterConfig,
    'master': MasterConfig
}
