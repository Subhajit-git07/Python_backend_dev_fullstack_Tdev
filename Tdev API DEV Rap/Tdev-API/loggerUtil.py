import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler
from config import settings

class Logging:
	logger = logging.getLogger(__name__)
	logger.setLevel(logging.INFO)
	logger.addHandler(AzureLogHandler(connection_string=settings.loggerConnStr))

logger = Logging.logger
