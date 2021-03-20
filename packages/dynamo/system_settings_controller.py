from Cloud.packages.Models import system_settings_model
from Cloud.packages.dynamo import dynamo_manager
from Cloud.packages.constants import constants
from Cloud.packages import logger
from decimal import Decimal

LOGGER = logger.Logger(__name__)
log = LOGGER.logger

cst = constants

##############################################################################################
SETTINGS_MODEL = system_settings_model.SystemSettingsModel()
SETTINGS_TABLE = "Settings"


def create_item(version=1):
    model = SETTINGS_MODEL
    model.version = version
    dynamo_manager.create_item(table_name=SETTINGS_TABLE, dictionary_item=model.__dict__)
    return model.__dict__


def get_item(version):
    result = dynamo_manager.read_item(SETTINGS_TABLE, "version", version)
    return result


def get_or_create(version):
    result = get_item(version)

    if result is None:
        result = create_item(version)

    return result


def update_item(data):
    dynamo_manager.create_item(table_name=SETTINGS_TABLE, dictionary_item=data)


##############################################################################################
if __name__ == '__main__':
    data = {'search_speed': Decimal('2'), 'version': Decimal('2'), 'search_engine': False}
    print(update_item(data))
