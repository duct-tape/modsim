# ModBus Simulator instance.

Simplified ModBus Server to be used for local development and integration testing.

## Configuration

Bus Slaves can be configured using json file, which should contain mapping of slave definitions.

### Slave Definition

Each slave devined by it's ID and settings dictionary.

Configuration dictionary contains following items:
 - `address`: integer with slave address
 - `number_of_registries`: number of data registries to reserve
 - `byteorder`: slave byte order (`>`, `<`)
 - `wordorder`: slave word order (`>`, `<`)
 - `data_format`: data format (`16bit`, `32bit`, `32bit_float`)

Example:

```
{
    "0": {
        "address": 40493,
        "number_of_registers": 1,
        "byteorder": ">",
        "wordorder": "<",
        "data_format": "16bit"
    }
}
```

## Running server

Server can be started by running `modsim <configuration_file.json>`.

`modsim` command accepts following parameters:
 - `-h`: hostname to listen to
 - `-p`: port to listen to

## Installation

Package can be installed via pip:

```
pip install git+https://github.com/duct-tape/modsim.git
```