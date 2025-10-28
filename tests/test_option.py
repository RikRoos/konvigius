# tests/test_class_Option.py
import re
import pytest
from typing import Any
import types

from konvigius.configlib import Config, Option
from konvigius.core.types import Schema
from konvigius.exceptions import (
    ConfigMetadataError,
    ConfigTypeError,
    ConfigRangeError,
    ConfigValidationError,
    ConfigDomainError,
    ConfigRequiredError,
)

# ----------------------------
# Basic Tests
# ----------------------------


def test_instantion_default_raises():
    "raise: when no Schema is given"
    with pytest.raises(
        TypeError,
        match=re.escape(
            "Option.__init__() missing 1 required positional argument: 'entry'"
        ),
    ):
        opt = Option()


def test_instantion_with_minimal_entry():
    "OK: only name is given"
    entry = Schema("username")
    cfg = Config.config_factory([entry])
    opt = cfg.get_meta("username")
    assert opt.name == "username"
    assert opt.short_flag is None
    assert opt.field_type is None
    assert opt.domain is None
    assert opt.default_value is None
    assert opt.r_min is None
    assert opt.r_max is None
    assert opt.fn_validator == None
    assert opt.fn_computed == None
    assert opt.help_text == "Option: username (default 'None')"
    assert opt.help_add_default is True
    assert opt.do_validate is True


def test_instantion_with_dashes_in_entry_names():
    "OK: dashes were replaced by underscores"
    entry = [Schema("user-name|u", domain=("guest", "admin"), default="guest"),
             Schema("actions-today", domain=("test", "meeting")),
             Schema("--go--working--today", field_type=bool),
             Schema("-----go-fishing-today", field_type=bool, default=True, no_validate="")]

    cfg = Config.config_factory(entry)
    opt = cfg.get_meta("user_name")
    assert opt.name == "user_name"
    assert opt.short_flag == "u"
    assert opt.field_type is None
    assert opt.domain == ("guest", "admin")
    assert opt.default_value == "guest"
    opt = cfg.get_meta("actions_today")
    assert opt.name == "actions_today"
    assert opt.short_flag is None
    assert opt.field_type is None
    assert opt.domain == ("test", "meeting")
    assert opt.default_value is None
    opt = cfg.get_meta("go__working__today")
    assert opt.name == "go__working__today"
    assert opt.short_flag is None
    assert opt.field_type is bool
    assert opt.default_value is False
    assert cfg.go__working__today is False
    assert cfg.no_go__working__today is True
    opt = cfg.get_meta("go_fishing_today")
    assert opt.name == "go_fishing_today"
    assert opt.short_flag is None
    assert opt.field_type is bool
    assert opt.default_value is True
    assert cfg.go_fishing_today is True
    assert cfg.no_go_fishing_today is False


def test_instantion_with_validation_False():
    "OK: only name is given"
    entry = Schema("username", no_validate=True)
    cfg = Config.config_factory([entry])
    opt = cfg.get_meta("username")
    assert opt.name == "username"
    assert opt.short_flag is None
    assert opt.field_type is None
    assert opt.domain is None
    assert opt.default_value is None
    assert opt.r_min is None
    assert opt.r_max is None
    assert opt.fn_validator == None
    assert opt.fn_computed == None
    assert opt.help_text == "Option: username (default 'None')"
    assert opt.help_add_default is True
    assert opt.do_validate == False


def test_instantion_with_short_flag_in_name():
    "OK: only name is given"
    entry = Schema("username|u")
    cfg = Config.config_factory([entry])
    opt = cfg.get_meta("username")
    assert opt.name == "username"
    assert opt.short_flag == "u"
    assert opt.field_type is None
    assert opt.domain is None
    assert opt.default_value is None
    assert opt.r_min is None
    assert opt.r_max is None
    assert opt.fn_validator == None
    assert opt.fn_computed == None
    assert opt.help_text == "Option: username (default 'None')"
    assert opt.help_add_default is True
    assert opt.do_validate == True


def test_instantion_with_short_flag_in_name_2():
    "OK: only name is given"
    entry = Schema("username|u", short_flag="n")
    cfg = Config.config_factory([entry])
    opt = cfg.get_meta("username")
    assert opt.name == "username"
    assert opt.short_flag == "n"
    assert opt.field_type is None
    assert opt.domain is None
    assert opt.default_value is None
    assert opt.r_min is None
    assert opt.r_max is None
    assert opt.fn_validator == None
    assert opt.fn_computed == None
    assert opt.help_text == "Option: username (default 'None')"
    assert opt.help_add_default is True
    assert opt.do_validate == True


def test_instantion_with_too_long_short_flag_in_name():
    "raises: short_flag to long"
    entry = Schema("username|us")
    with pytest.raises(
        ConfigMetadataError,
        match=re.escape("short CLI flags must be a single character: 'us'"),
    ):
        cfg = Config.config_factory([entry])


def test_instantion_with_short_flag_in_name_3():
    "OK: short_flag to long but is replaced by explicit short_flag"
    entry = Schema("username|us", short_flag="u")
    cfg = Config.config_factory([entry])
    opt = cfg.get_meta("username")
    assert opt.name == "username"
    assert opt.short_flag == "u"
    assert opt.field_type is None
    assert opt.domain is None
    assert opt.default_value is None
    assert opt.r_min is None
    assert opt.r_max is None
    assert opt.fn_validator == None
    assert opt.fn_computed == None
    assert opt.help_text == "Option: username (default 'None')"
    assert opt.help_add_default is True
    assert opt.do_validate == True


def test_instantion_with_short_flag_in_name_4():
    "raises: no name"
    entry = Schema("|u")
    with pytest.raises(
        ConfigMetadataError, match=re.escape("Schema name not valid (|u)")
    ):
        cfg = Config.config_factory([entry])


# ----------------------------
# Validator Tests
# ----------------------------


def test_validate_name():
    "OK: only name is given"
    entry = Schema("username|u")
    cfg = Config.config_factory([entry])
    opt = cfg.get_meta("username")
    assert opt.name == "username"
    assert opt.short_flag == "u"


def test_validate_name_and_str():
    "OK: name is given and datatype is str"
    entry = Schema(
        "username|u", field_type=str, default=1234, no_validate=True
    )  # False is default
    cfg = Config.config_factory([entry])
    assert cfg.username == 1234


def test_validate_name_and_int():
    "Fail: name is given and datatype is int"
    entry = Schema("username|u", field_type=str, default=123)
    with pytest.raises(ConfigValidationError):
        cfg = Config.config_factory([entry])


def test_validate_name_and_int_NO_VALIDATE_1():
    "OK: only name is given, but datatype is INT"
    entry = Schema("username|u", field_type=int, no_validate=True)  # False is default
    cfg = Config.config_factory([entry])
    assert cfg.username is None


def test_validate_name_and_int_NO_VALIDATE_2():
    "Fail: name is given and datatype is int AND wrong lenght short-flag"
    "Shortflag length must always be 1"
    entry = Schema("username|XXX", field_type=int, no_validate=True)
    with pytest.raises(ConfigMetadataError):
        cfg = Config.config_factory([entry])


@pytest.mark.parametrize("arg", [1, 2, 3, 4, 5])
def test_validate_int(arg):
    "OK: ints are in range"
    entry = Schema("username|u", r_min=1, r_max=5, default=arg)
    cfg = Config.config_factory([entry])
    assert cfg.username == arg


@pytest.mark.parametrize("arg", [-1, 0, 6, 7])
def test_validate_int_raises(arg):
    "FAIL: ints are not in range"
    entry = Schema("username|u", r_min=1, r_max=5, default=arg)
    with pytest.raises(ConfigRangeError):
        cfg = Config.config_factory([entry])


@pytest.mark.parametrize(
    "arg", [(int, 0), (str, "a"), (float, 3.14), (list, [1, 2]), (set, {1, 2})]
)
def test_validate_multiple_types_1(arg):
    "OK: multiple types"
    entry = Schema("username|u", field_type=arg[0], default=arg[1])
    cfg = Config.config_factory([entry])
    assert cfg.username == arg[1]


@pytest.mark.parametrize("arg", [0, "ab", [1, 2]])
def test_validate_multiple_types_2(arg):
    "OK: multiple types"
    entry = Schema("username|u", field_type=(int, str, list), default=arg)
    cfg = Config.config_factory([entry])
    assert cfg.username == arg


@pytest.mark.parametrize("arg", ["ab", [1, 2]])
def test_validate_multiple_types_3(arg):
    "Fail: multiple types"
    entry = Schema("username|u", field_type=(float, set), default=arg)
    with pytest.raises(ConfigValidationError):
        cfg = Config.config_factory([entry])


@pytest.mark.parametrize(
    "arg", [(int, "0"), (str, 1), (float, 4), (list, "abc"), (set, [1, 2])]
)
def test_validate_multiple_types_raises(arg):
    "raises: wrong types"
    entry = Schema("username|u", field_type=arg[0], default=arg[1])
    with pytest.raises(ConfigTypeError):
        cfg = Config.config_factory([entry])

# --- DOMAIN ---

@pytest.mark.parametrize("arg", ["guest", "admin", "finance"])
def test_validate_domain(arg):
    "OK: domain"
    entry = Schema("username|u", domain=("guest", "admin", "finance"), default=arg)
    cfg = Config.config_factory([entry])
    assert cfg.username == arg


@pytest.mark.parametrize("arg", ["hacker", "finance"])
def test_validate_domain_raises(arg):
    "FAIL: domain"
    entry = Schema("username|u", domain=("guest", "admin"), default=arg)
    with pytest.raises(ConfigValidationError):
        cfg = Config.config_factory([entry])


@pytest.mark.parametrize("arg", ["hacker", 0, 1, [], [3, 4], set(), 3.14, False, True])
def test_validate_required(arg):
    "OK: required"
    entry = [Schema("username|u", required=True, default=arg)]
    cfg = Config.config_factory(entry)
    assert cfg.username == arg


def test_validate_required_raises():
    "Fail: a default is required required"
    entry = [Schema("username|u", required=True)]
    with pytest.raises(ConfigValidationError):
        Config.config_factory(entry)


def test_validate_type_and_domain():
    "OK: domain"
    entry = [
        Schema("username|u", default=123, domain=("guest", 123), field_type=(str, int))
    ]
    cfg = Config.config_factory(entry)
    assert cfg.username == 123

@pytest.mark.parametrize("arg", [(object(), object(), object())] ) # is hashable !
def test_validate_domain_definition_raw_objects(arg):
    "OK: objects are hashable"
    entry = [
        Schema("username|u", default=arg[0], domain=arg)
    ]
    cfg = Config.config_factory(entry)
    opt_domain = cfg.get_meta("username").domain
    assert opt_domain == arg 

@pytest.mark.parametrize("arg", [ "string", 123, [1,2,3], {1:2} ])
def test_validate_wrong_domain_definition_raises_1(arg):
    "FAIL: domain definition"
    entry = [
        Schema("username|u", default="john", domain=arg)
    ]
    with pytest.raises(ConfigDomainError):
        Config.config_factory(entry)


@pytest.mark.parametrize("arg", [ ([1,2], [2,3])] )
def test_validate_wrong_domain_definition_raises_2(arg):
    "FAIL: domain definition"
    entry = [
        Schema("username|u", default="john", domain=arg)
    ]
    with pytest.raises(ConfigDomainError):
        Config.config_factory(entry)

def test_validate_contradiction_type_and_domain_1():
    "OK: domain"
    entry = [Schema("username|u", default=3.14, domain=("guest", 123), field_type=str)]
    with pytest.raises(ConfigTypeError):
        Config.config_factory(entry)

def test_validate_contradiction_type_and_domain_2():
    "OK: domain"
    entry = [Schema("username|u", default="john", domain=(123, 345), field_type=str)]
    with pytest.raises(ConfigDomainError):
        Config.config_factory(entry)


@pytest.mark.parametrize("arg", ["str", "int", "boolean", 123, 3.14, [], {'k': 'v'}])
def test_validate_wrong_fieldtype_definition_raises_1(arg):
    "FAIL: field_type definition"
    entry = [
        Schema("username|u", default="john", field_type=arg)
    ]
    with pytest.raises(ConfigTypeError):
        Config.config_factory(entry)


@pytest.mark.parametrize("arg", [ (1,2,3) ,  ('a', 'b', 'c') ])
def test_validate_wrong_fieldtype_definition_raises_2(arg):
    "FAIL: field_type definition"
    entry = [
        Schema("username|u", default="john", field_type=arg)
    ]
    with pytest.raises(ConfigTypeError):
        Config.config_factory(entry)

@pytest.mark.parametrize("arg", [ True, False, None ])
def test_validate_required_definition(arg):
    "FAIL: field_type definition"
    entry = [
        Schema("username|u", default="john", required=arg)
    ]
    cfg = Config.config_factory(entry)
    req = cfg.get_meta('username').required
    assert req == (True if arg is True else False)

@pytest.mark.parametrize("arg", [ 1, "true", (True,), (1,2,3) ])
def test_validate_wrong_required_definition_raises(arg):
    "FAIL: field_type definition"
    entry = [
        Schema("username|u", default="john", required=arg)
    ]
    with pytest.raises(ConfigRequiredError):
        Config.config_factory(entry)

def test_validate_fn_compute_def_raises_1():
    "FAIL"
    entry = [Schema("username|u", default="john", fn_computed="not a function")]
    with pytest.raises(ConfigTypeError):
        Config.config_factory(entry)


def test_validate_fn_compute_def_raises_2():
    "FAIL"
    entry = [Schema("username|u", default="john", fn_computed=lambda x: x)]
    with pytest.raises(ConfigTypeError):
        Config.config_factory(entry)








# === END ===
