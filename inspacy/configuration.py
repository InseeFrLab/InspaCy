import os
import configparser

cfg = configparser.ConfigParser()
cfg.read(os.environ['INSPACY_HOME'] + '/inspacy/static/config.ini')