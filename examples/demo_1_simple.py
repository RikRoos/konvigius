"""
In this demo, two instances of the Config class are created: one for production
and one for a test environment.

Example:

    `python examples/demo_1_simple.py`


The test environment is created using the `Config.from_dict` method, which allows
the instance to be initialized with custom values.

Next, the `timeout` configuration option is modified for both environments and printed.

Note that the `debug` option automatically creates an inverted configuration variable
`no_debug`. This is done to provide an inverted option for testing the debug mode in code.
"""

from konvigius import Config, Schema

# Define the config schema (or place this dict in a seperate file named 'schema.py')

schema = [
    Schema("username", default="guest", field_type=str),
    Schema("debug", default=False, field_type=bool),
    Schema("timeout", default=30, r_min=1, r_max=120, field_type=int),  # r_ : range_
]

# Create a config instance

cfg = Config.config_factory(schema)

# Create another config instance with different defaults from a dict argument

cfg_tst = Config.from_dict(schema, values={"username": "tester", "debug": True})

# Use now the config values in your app

line = f"{'- ' * 15}"

print(line, __doc__, line)
print("Username:", cfg.username)
print("Debug mode:", cfg.debug)
print("No-Debug mode:", cfg.no_debug)  # inverted bonus
print("Timeout:", cfg.timeout)
print(line)
print("Test/Username:", cfg_tst.username)
print("Test/Debug mode:", cfg_tst.debug)
print("test/No-Debug mode:", cfg_tst.no_debug)
print("Test/Timeout:", cfg_tst.timeout)
print(line + "\n")

cfg.timeout = 70
cfg_tst.timeout = 120

print("Timeout:", cfg.timeout)
print(line)
print("Test/Timeout:", cfg_tst.timeout)
print(line + "\n")


# === END ===
