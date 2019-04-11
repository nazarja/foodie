import os


class Config(object):

    """
        This config class contains methods to get a secret key needed for
        some modules such as wtf_forms and the database uri,these variables
        are stored as properties of the Config class.
    """

    SECRET_KEY = os.environ.get('SECRET_KEY')
    MONGO_URI = os.environ.get('MONGO_URI')
