import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler
from Config import EnvSettings

class Application_logging:
    logger = logging.getLogger(__name__)

    logger.addHandler(AzureLogHandler(
        connection_string=EnvSettings.logger_string)
    )

App_logger = Application_logging.logger