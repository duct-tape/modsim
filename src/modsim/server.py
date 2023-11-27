import logging
import json

from pymodbus.datastore import (
    ModbusSequentialDataBlock,
    ModbusServerContext,
    ModbusSlaveContext,
)
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.server import (
    StartAsyncTcpServer,
)
from pymodbus.transaction import ModbusSocketFramer

logger = logging.getLogger("modsim.server")

DEFAULT_VALUE = 100


class ModSimServer:

    def __init__(self, host, port, configuration_file) -> None:
        self.host = host
        self.port = port
        self.configuration_file = configuration_file

    def build_slave(self, address, number_of_registers, byteorder, wordorder, data_format):
        """Build slave context."""
        hr_builder = BinaryPayloadBuilder(byteorder=byteorder, wordorder=wordorder)
        for i in range(number_of_registers):
            if data_format == "16bit":
                hr_builder.add_16bit_int(DEFAULT_VALUE)
            elif data_format == "32bit":
                hr_builder.add_32bit_uint(DEFAULT_VALUE)
            elif data_format == "32bit_uint":
                hr_builder.add_32bit_uint(DEFAULT_VALUE)
            elif data_format == "32bit_float":
                hr_builder.add_32bit_float(float(DEFAULT_VALUE))
            else:
                raise ValueError(f"Incorrect format provided: {data_format}")
        registers = hr_builder.to_registers()
        return ModbusSlaveContext(
            hr=ModbusSequentialDataBlock(address, registers),
            zero_mode=True,
        )

    def build_slaves(self, filename):
        """Build slaves from configuration."""
        with open(filename) as config_file:
            data = json.load(config_file)

        logger.info(f"Configuring slaves: {data}")
        return {
            int(id): self.build_slave(**row)
            for id, row in data.items()
        }

    async def run_async_server(self):
        """Run server setup."""
        logger.info("### Create datastore")

        slaves = self.build_slaves(filename=self.configuration_file)
        context = ModbusServerContext(slaves=slaves, single=False)

        # ----------------------------------------------------------------------- #
        # initialize the server information
        # ----------------------------------------------------------------------- #
        # If you don't set this or any fields, they are defaulted to empty strings.
        # ----------------------------------------------------------------------- #
        identity = ModbusDeviceIdentification(
            info_name={
                "VendorName": "Pymodbus",
                "ProductCode": "modsim",
                "VendorUrl": "https://github.com/riptideio/pymodbus/",
                "ProductName": "Pymodbus Simulator Server",
                "ModelName": "Pymodbus Simulator Server",
            }
        )

        logger.info(f"### start ASYNC server, listening on {self.port} - {self.host}")

        address = (self.host, self.port) if self.port else None
        server = await StartAsyncTcpServer(
            context=context,
            identity=identity,
            address=address,
            framer=ModbusSocketFramer,
        )
        return server
