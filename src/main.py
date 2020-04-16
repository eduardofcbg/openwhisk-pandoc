import logging

from sanic import Sanic

from app.logging import config as log_config
from app.app import pandoc


logging.config.dictConfig(log_config)

app = Sanic(name="pandoc_service")

app.blueprint(pandoc)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, workers=4, access_log=False)
