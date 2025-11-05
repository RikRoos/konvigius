"""
This demo demonstrates the use of the terminal CLI.

View the available options using: `simple_demo_with_cli.py -h`.

Example:

    `python example/demo_2_with_cli.py --username admin -t 20 -d`


This changes the `username` to 'admin', sets the `timeout` to 20 seconds, and enables
debug mode.

Note that the `debug` option automatically creates an inverted configuration variable
`no_debug`; this is done for all boolean options. This approach ensures that a boolean
option can always be evaluated in a positive manner within the code.
"""

from konvigius import Config, Schema, cli_parser

# Define the config schema (or place this dict in a seperate file named 'schema.py')

schema = [
    Schema("username|u", default="guest", field_type=str),
    Schema("debug|d", default=False, field_type=bool),
    Schema("no_wrap", default=False, field_type=bool),
    Schema(
        "timeout|t",
        default=30,
        r_min=1,
        r_max=120,
        field_type=int,
        help_text="Duration in seconds",
    ),
]

# Create a config instance

cfg = Config.config_factory(schema)
cfg.test_var = "RikRoos"

last_username = cfg.username
last_debug = cfg.debug
last_no_debug = cfg.no_debug
last_no_wrap = cfg.no_wrap
last_wrap = cfg.wrap
last_timeout = cfg.timeout

# Parse the CLI arguments from the terminal.

cli_parser.run_parser(cfg)

line = f"{'- ' * 15}"

print(line, __doc__, line)
print("Config values at start...")
print("Username:", last_username)
print("Debug mode:", last_debug)
print("No-Debug mode:", last_no_debug)
print("No-wrap mode:", last_no_wrap)
print("Wrap mode:", last_wrap)
print("Timeout:", last_timeout)
print(line)
print("Config values after CLI...:")
print(line)
print("Username:", cfg.username)
print("Debug mode:", cfg.debug)
print("No-Debug mode:", cfg.no_debug)
print("No-wrap mode:", cfg.no_wrap)
print("Wrap mode:", cfg.wrap)
print("Timeout:", cfg.timeout)
print(line)

print("\n\n--- internal stores values (S:from schema, C:computed) ---")
print(cfg.inspect_vars())


# === END ===
