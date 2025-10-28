"""
This demo demonstrates the use of validation AND transaction mode:

  - parameters `r_min` and `r_max` to validate the port number
  - cross-field validation: ports below 1024 only allowed for userrole admin.

View the available options using: `demo_4_validation_cross_fields.py -h`.

Example:

    `python demo_4_validation_cross_fields.py --port 5000 --userrole tester  # --> OK

    `python demo_4_validation_cross_fields.py --port 23   --userrole admin   # --> OK
    
    `python demo_4_validation_cross_fields.py --port 23                      # --> error message
    
    `python demo_4_validation_cross_fields.py --port 70000                   # --> error message

"""

from konvigius import Config, Schema, cli_parser
from konvigius.exceptions import ConfigError, ConfigValidationError


line = f"{'- ' * 15}"
print(line, __doc__, line)


def fn_check_port_admin(value, cfg):
    if value <= 1023 and cfg.userrole != "admin":
        e = f"Port {value} not permitted; login as admin please."
        msg = ["\n", len(e) * "*", e, len(e) * "*", "\n"]
        raise ConfigValidationError("\n".join(msg))


# Define the config schema (or place this dict in a seperate file named 'schema.py')

schema = [
    Schema(
        "port|p",
        default=3274,
        r_min=0,
        r_max=65535,
        field_type=int,
        fn_validator=fn_check_port_admin,
    ),
    Schema("userrole|r", default="guest", field_type=str),
]

# help can injected by adding a list-structure to the config-factory

helplines = {
    "port": "Port number of gaming stream.",
    "userrole": "User role, e.g. admin, tester, guest.",
}

# Create a config instance

cfg = Config.config_factory(schema, help_map=helplines)

# Parse the CLI arguments from the terminal.
# Because the validator checks the 'port' argument against the previous value of
# the userrole (guest, not admin) it will reject the mutation. To handle this situation the
# transaction-mode of the config is used. During the transaction no validation will
# be processed. At 'commit' point the validators will run.

try:
    cfg.start_transaction()
    cli_parser.run_parser(cfg)
    cfg.commit_transaction()
except ConfigError as e:
    print(e)

print("Config values after CLI...")
print("userrole", cfg.userrole)
print("port:", cfg.port)
print(line)

print("\n\n--- internal option values ---")
print(cfg.info_vars())


# === END ===
