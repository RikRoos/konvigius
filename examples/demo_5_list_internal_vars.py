"""
In this demo the utility to list the internal vars is demonstrated.

    `python examples/demo_5_list_internal_vars.py

"""

from konvigius import Config, Schema, with_field_name

# Define the config schema (or place this dict in a seperate file named 'schema.py')


@with_field_name("spaces")
def fn_spaces(value, cfg):
    return " " * cfg.num_spaces


@with_field_name("in_seconds")
def fn_seconds(value, cfg):
    return 60 * cfg.minutes


schema = [
    Schema("username", default="guest", field_type=str),
    Schema("debug", default=False, field_type=bool),
    Schema("wrap|w", default=True, field_type=bool),
    Schema("timeout", default=30, r_min=1, r_max=120, field_type=int),  # r_ : range_
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

# Create another config instance with different defaults from a dict argument

cfg_tst = Config.from_dict(
    schema, values={"username": "tester", "debug": True, "minutes": 60}
)

line = f"{'- ' * 15}"

print(line, __doc__, line)
print("\nShowing vars of instance `cfg`  (S:schema C:computed):\n")
print(cfg.info_vars())

print("\n", line)

print("\nShowing vars of instance `cfg_tst`:\n")
print(cfg_tst.info_vars())


# === END ===
