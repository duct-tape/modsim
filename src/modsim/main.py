import logging
import logging.config

import asyncio
import click

from modsim.server import ModSimServer

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "format": "%(asctime)s %(levelname)s %(message)s",
        }
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "json",
        }
    },
    "loggers": {"": {"handlers": ["stdout"], "level": "DEBUG"}},
}


@click.command()
@click.argument("configuration_filename", type=click.Path(exists=True))
@click.option("-h", "--host", default="localhost", type=str)
@click.option("-p", "--port", default=5020, type=int)
def cli(configuration_filename, host, port):
    logging.config.dictConfig(LOGGING)
    logger = logging.getLogger("modsim")

    logger.info(
        f"Start modsim"

    )

    modserver = ModSimServer(
        host=host,
        port=port,
        configuration_file=configuration_filename
    )
    asyncio.run(
        modserver.run_async_server(),
        debug=True
    )

    logger.info("exiting.")


if __name__ == "__main__":
    cli()