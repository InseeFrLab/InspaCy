import os
import configparser

relativeLocation = "/inspacy/static/config.ini"

cfg = configparser.ConfigParser()
if os.environ.get('INSPACY_HOME') is None:
    os.environ['INSPACY_HOME'] = '.'

cfg.read(os.environ['INSPACY_HOME'] + relativeLocation)