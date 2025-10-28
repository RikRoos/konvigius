# test_cli_parser.py

import pytest
import argparse

from konvigius.configlib import Config, Option
from konvigius import cli_parser
from konvigius.core.types import Schema
from konvigius.exceptions import ConfigRangeError


# ---------- Fixtures ----------

@pytest.fixture
def schema():
    return [
      Schema("username|u", default="guest", field_type=str, help_text="Username"),
      Schema("debug|d", default=False, field_type=bool, help_text="Enable debug mode"),
      Schema("timeout|t", default=30, field_type=int, r_min=1, r_max=120, help_text="Timeout in seconds"),
      Schema("no_wrap", default=True, field_type=bool, help_text="Disable text wrapping"),
    ]

@pytest.fixture
def config_instance(schema):
    return Config.config_factory(schema)


# ---------- Tests: build_arg_parser ----------

def test_create_parserargs_from_cfg(config_instance):
    parser_args = cli_parser.create_args_from_cfg(config_instance)
    assert isinstance(parser_args, list)
    assert len(parser_args) == 4

def test_build_parser_returns_parser(config_instance):
    parser_args = cli_parser.create_args_from_cfg(config_instance)
    parser = cli_parser.build_parser(parser_args)
    assert isinstance(parser, argparse.ArgumentParser)

# retest this with schema-option "no-wrap" , should be converted to "no_wrap"
@pytest.mark.parametrize("cli_args", [([],0), 
                                      (["--username", "bob", "--debug", "--timeout", 120],3),
                                      (["-u", "bob", "-d", "-t", 120], 3),
                                      (["-t", 120], 1),
                                      (["-d"], 1),
                                      (["--no-wrap", "-d"], 2)
                                     ])
def test_parser_can_parse_args(config_instance, cli_args):
    parser_args = cli_parser.create_args_from_cfg(config_instance)
    parser = cli_parser.build_parser(parser_args)
    parsed_args = parser.parse_args(args=cli_parser._stringify_cli_args(cli_args[0]))
    assert len(vars(parsed_args)) == cli_args[1]

def test_build_parser_includes_custom_arguments(config_instance):
    parser_args = cli_parser.create_args_from_cfg(config_instance)
    parser = cli_parser.build_parser(parser_args)
    cli_args = ["--username", "admin", "--timeout", "60", "-d", "--no-wrap"]
    parsed_args = parser.parse_args(args=cli_parser._stringify_cli_args(cli_args))
    assert parsed_args.username == "admin"
    assert parsed_args.debug is True
    #assert parsed_args.no-wrap is True
    assert parsed_args.timeout == 60

def test_run_parser_and_config_remains_unchanged(config_instance):
    prev_username = config_instance.username
    prev_debug = config_instance.debug
    prev_no_debug = config_instance.no_debug
    prev_timeout = config_instance.timeout
    prev_no_wrap = config_instance.no_wrap
    prev_wrap = config_instance.wrap
    parser, parsed_args = cli_parser.run_parser(config_instance, cli_args=[])
    assert len(vars(parsed_args)) == 0
    assert config_instance.username == prev_username
    assert config_instance.debug is prev_debug
    assert config_instance.no_debug is prev_no_debug
    assert config_instance.no_wrap is prev_no_wrap
    assert config_instance.wrap is prev_wrap
    assert config_instance.timeout == prev_timeout

def test_run_parser_and_config_is_changed(config_instance):
    prev_username = config_instance.username
    prev_debug = config_instance.debug
    prev_timeout = config_instance.timeout
    cli_args = ["--username", "alice", "-t", "45", "--debug"]
    parser, parsed_args = cli_parser.run_parser(config_instance, cli_args=cli_args)
    assert parsed_args.username == 'alice'
    assert parsed_args.debug is True
    assert parsed_args.timeout == 45
    assert config_instance.username == 'alice'
    assert config_instance.debug is True
    assert config_instance.timeout == 45
    assert config_instance.username != prev_username
    assert config_instance.debug is not prev_debug
    assert config_instance.timeout != prev_timeout

def test_run_parser_partial_update(config_instance):
    prev_username = config_instance.username
    prev_debug = config_instance.debug
    prev_timeout = config_instance.timeout
    cli_args = ["--username", "bob"]
    parser, parsed_args = cli_parser.run_parser(config_instance, cli_args=cli_args)
    assert len(vars(parsed_args)) == 1 
    assert parsed_args.username == 'bob'
    assert config_instance.username == 'bob'
    assert config_instance.debug is False
    assert config_instance.timeout == 30
    assert config_instance.username != prev_username
    assert config_instance.debug is prev_debug
    assert config_instance.timeout == prev_timeout

@pytest.mark.parametrize('schema', [
    Schema("some_numeric", default='333', field_type=str),
    Schema("some_numeric", default=333, field_type=int),
    Schema("some_numeric", default=333.3, field_type=float),
    Schema("some_numeric", default=[333], field_type=list),
    Schema("some_numeric", default=(1,2), field_type=tuple),
    Schema("some_numeric", default={'num' : 333}, field_type=dict),
    Schema("some_numeric", default='555', field_type=object),
    ])
def test_schema_single_fieldtypes(schema):
    entry = schema
    cfg = Config.config_factory([entry])
    parser_args = cli_parser.create_args_from_cfg(cfg)
    assert isinstance(parser_args, list)
    assert len(parser_args) == 1
    assert cfg.some_numeric == schema.default
    assert cfg.get_meta("some_numeric").field_type == schema.field_type



@pytest.mark.parametrize('schema', [
    Schema("some_numeric", default='333', field_type=(str, int)),
    Schema("some_numeric", default=444, field_type=(str, int)),
    Schema("some_numeric", default=555.5, field_type=(float, str, int)),
    Schema("some_numeric", default=555.5, field_type=(int, str, float)),
    Schema("some_numeric", default=555.5, field_type=(int, float)),
    Schema("some_numeric", default=555, field_type=(int, list, dict)),
    Schema("some_numeric", default=[1,2], field_type=(list, tuple)),
    ])
def test_schema_multiple_fieldtypes(schema):
    entry = schema
    cfg = Config.config_factory([entry])
    parser_args = cli_parser.create_args_from_cfg(cfg)
    assert isinstance(parser_args, list)
    assert len(parser_args) == 1
    # print
    # print(parser_args[0]['kwargs']['type'])
    assert parser_args[0]['kwargs']['type'] == schema.field_type[0]
    assert cfg.some_numeric == schema.default
    assert cfg.get_meta("some_numeric").field_type == schema.field_type

def test_short_flags_work_correctly(config_instance):
    cli_args = ["-u", "shortuser", "-t", "25", "-d"]
    cli_parser.run_parser(config_instance, cli_args=cli_args)
    assert config_instance.username == "shortuser"
    assert config_instance.timeout == 25
    assert config_instance.debug is True

@pytest.mark.parametrize("good_range", [1, 2, 100, 120 ])
def test_run_parser_accepts_valid_ranges(config_instance, good_range):
    cli_args = ["--timeout", good_range] 
    cli_parser.run_parser(config_instance, cli_args=cli_args)
    assert config_instance.timeout == good_range

def test_run_parser_respects_range(config_instance):
    cli_args = ["--timeout", "9999"]  # Exceeds max=120
    with pytest.raises(ConfigRangeError):
        # here we skip the step to create manually the parser_args
        parser, parsed_args = cli_parser.run_parser(config_instance, cli_args=cli_args)

@pytest.mark.parametrize("bad_range", [-1, 0, 121 ])
def test_run_parser_respects_ranges(config_instance, bad_range):
    cli_args = ["--timeout", bad_range] 
    with pytest.raises(ConfigRangeError):
        cli_parser.run_parser(config_instance, cli_args=cli_args)


# === END ===
