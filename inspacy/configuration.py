import os
import configparser

relativeLocation = "/inspacy/static/config.ini"

cfg = configparser.ConfigParser()
if os.environ.get('INSPACY_HOME') is not None:
    cfg.read(os.environ['INSPACY_HOME'] + relativeLocation)
else:
    cfg.read("./static/config.ini")
