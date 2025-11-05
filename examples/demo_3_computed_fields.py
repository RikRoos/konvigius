"""
This demo demonstrates the use of computations.

The option --num-spaces will result in a generated read-only property named 'spaces'.
The option --minutes will result in a generated read-only property named 'in_seconds'.

View the available options using: `demo_3_computed_fields.py -h`.

Example:

    `python demo_3_computed_fields.py --num-spaces 5 --minutes 10

"""

from konvigius import Config, Schema, with_field_name, cli_parser

# define the help-function that returns the computed value, here concatenation of spaces


@with_field_name("spaces")
def fn_spaces(value, cfg):
    return " " * cfg.num_spaces


@with_field_name("in_seconds")
def fn_seconds(value, cfg):
    return 60 * cfg.minutes


# Define the config schema (or place this dict in a seperate file named 'schema.py')

schema = [
    Schema(
        "num_spaces|s",
        default=2,
        fn_computed=fn_spaces,
        field_type=int,
        help_text="Number of spaces.",
    ),
    Schema(
        "minutes|m",
        default=5,
        fn_computed=fn_seconds,
        field_type=int,
        help_text="Duration in minutes",
    ),
]

# Create a config instance

cfg = Config.config_factory(schema)

line = f"{'- ' * 15}"

print(line, __doc__, line)
print("Config values at start...")
print(line)
print("num-spaces", cfg.num_spaces)
print(f"spaces: '{cfg.spaces}'  (computed)")
print("minutes:", cfg.minutes)
print("seconds:", cfg.in_seconds, "  (computed)")

# Parse the CLI arguments from the terminal.

cli_parser.run_parser(cfg)

print(line)
print("Config values after CLI...")
print(line)
print("num-spaces", cfg.num_spaces)
print(f"spaces: '{cfg.spaces}'  (computed)")
print("minutes:", cfg.minutes)
print("seconds:", cfg.in_seconds, "  (computed)")
print(line)

print("\n\n--- internal values ---")
print(cfg.inspect_vars())


# === END ===
