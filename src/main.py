import logging

from app.logging import config as log_config
from app.openwhisk import OpenwhiskErrorHandler
from app.app import app

if __name__ == "__main__":
    logging.config.dictConfig(log_config)
    app.error_handler = OpenwhiskErrorHandler()
    app.run(host="0.0.0.0", port=8080, workers=4, access_log=False)
