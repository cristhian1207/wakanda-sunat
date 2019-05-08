import json

data=None
with open('config/config.json') as config:
    data=json.load(config)
env=data['env']
env_config=data[env]

global MYSQL_CONFIG
global OPERATIVE_SYSTEM

MYSQL_CONFIG=env_config['mysql']
OPERATIVE_SYSTEM=env_config['os']