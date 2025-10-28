import pytest
import pprint
import io

from konvigius.configlib import Config
import konvigius.cli_parser as cli
from konvigius.core.types import Schema

def test_fn_create_args_from_cfg():
    schema = [
        Schema("username", default="guest", field_type=str),
        Schema("userrole", domain=("admin", "marketing"), field_type=str),
        Schema("debug|d", default=False, field_type=bool),
        Schema("no_wrap", default=True, field_type=bool),
        Schema("timeout|t", default=10, field_type=(float, int), r_min=1, r_max=60),
        Schema("count", default=5, r_min=1, r_max=10, field_type=int),
        Schema("x", default=1, field_type=int, help_text=None),
        Schema("y", default=2, field_type=int),
        Schema("z", default="abc", field_type=str)
    ]
    cfg = Config.config_factory(schema)
    args = cli.create_args_from_cfg(cfg)
    buf = io.StringIO()
    pprint.pprint(args, stream=buf)
    buf = buf.getvalue()
    buf_expected = """\
[{'kwargs': {'dest': 'username',
             'help': "Option: username (default 'guest')",
             'metavar': 'CHARS',
             'nargs': '?',
             'type': <class 'str'>},
  'names': ['--username']},
 {'kwargs': {'dest': 'userrole',
             'help': "Option: userrole (default 'None')",
             'metavar': 'CHARS',
             'nargs': '?',
             'type': <class 'str'>},
  'names': ['--userrole']},
 {'kwargs': {'action': 'store_true',
             'dest': 'debug',
             'help': "Option: debug (default 'False')"},
  'names': ['-d', '--debug']},
 {'kwargs': {'action': 'store_true',
             'dest': 'no_wrap',
             'help': "Option: no_wrap (default 'True')"},
  'names': ['--no-wrap']},
 {'kwargs': {'dest': 'timeout',
             'help': "Option: timeout (default '10')",
             'nargs': '?',
             'type': <class 'float'>},
  'names': ['-t', '--timeout']},
 {'kwargs': {'dest': 'count',
             'help': "Option: count (default '5')",
             'metavar': 'NUM',
             'nargs': '?',
             'type': <class 'int'>},
  'names': ['--count']},
 {'kwargs': {'dest': 'x',
             'help': "Option: x (default '1')",
             'metavar': 'NUM',
             'nargs': '?',
             'type': <class 'int'>},
  'names': ['--x']},
 {'kwargs': {'dest': 'y',
             'help': "Option: y (default '2')",
             'metavar': 'NUM',
             'nargs': '?',
             'type': <class 'int'>},
  'names': ['--y']},
 {'kwargs': {'dest': 'z',
             'help': "Option: z (default 'abc')",
             'metavar': 'CHARS',
             'nargs': '?',
             'type': <class 'str'>},
  'names': ['--z']}]
"""
    assert buf == buf_expected


def test_fn_create_args_from_cfg__show_help_defaults():
    schema = [
        Schema("username", default="guest", field_type=str),
        Schema("userrole", domain=("admin", "marketing"), field_type=str),
        Schema("debug|d", default=False, field_type=bool),
        Schema("no_wrap", default=True, field_type=bool),
        Schema("timeout|t", default=10, field_type=(float, int), r_min=1, r_max=60),
        Schema("count", default=5, r_min=1, r_max=10, field_type=int),
        Schema("v", default=1, field_type=int, help_text=None, help_add_default=True),
        Schema("w", default=1, field_type=int, help_text=None, help_add_default=False),
        Schema("x", default=1, field_type=int, help_text="Helptext for option x",),
        Schema("y", default=2, field_type=int, help_text="Helptext for option y", help_add_default=True),
        Schema("z", default="abc", field_type=str, help_text="Helptext for option z", help_add_default=False)
    ]
    cfg = Config.config_factory(schema)
    args = cli.create_args_from_cfg(cfg)
    buf = io.StringIO()
    pprint.pprint(args, stream=buf)
    buf = buf.getvalue()
    buf_expected = """\
[{'kwargs': {'dest': 'username',
             'help': "Option: username (default 'guest')",
             'metavar': 'CHARS',
             'nargs': '?',
             'type': <class 'str'>},
  'names': ['--username']},
 {'kwargs': {'dest': 'userrole',
             'help': "Option: userrole (default 'None')",
             'metavar': 'CHARS',
             'nargs': '?',
             'type': <class 'str'>},
  'names': ['--userrole']},
 {'kwargs': {'action': 'store_true',
             'dest': 'debug',
             'help': "Option: debug (default 'False')"},
  'names': ['-d', '--debug']},
 {'kwargs': {'action': 'store_true',
             'dest': 'no_wrap',
             'help': "Option: no_wrap (default 'True')"},
  'names': ['--no-wrap']},
 {'kwargs': {'dest': 'timeout',
             'help': "Option: timeout (default '10')",
             'nargs': '?',
             'type': <class 'float'>},
  'names': ['-t', '--timeout']},
 {'kwargs': {'dest': 'count',
             'help': "Option: count (default '5')",
             'metavar': 'NUM',
             'nargs': '?',
             'type': <class 'int'>},
  'names': ['--count']},
 {'kwargs': {'dest': 'v',
             'help': "Option: v (default '1')",
             'metavar': 'NUM',
             'nargs': '?',
             'type': <class 'int'>},
  'names': ['--v']},
 {'kwargs': {'dest': 'w',
             'help': 'Option: w',
             'metavar': 'NUM',
             'nargs': '?',
             'type': <class 'int'>},
  'names': ['--w']},
 {'kwargs': {'dest': 'x',
             'help': "Helptext for option x (default '1')",
             'metavar': 'NUM',
             'nargs': '?',
             'type': <class 'int'>},
  'names': ['--x']},
 {'kwargs': {'dest': 'y',
             'help': "Helptext for option y (default '2')",
             'metavar': 'NUM',
             'nargs': '?',
             'type': <class 'int'>},
  'names': ['--y']},
 {'kwargs': {'dest': 'z',
             'help': 'Helptext for option z',
             'metavar': 'CHARS',
             'nargs': '?',
             'type': <class 'str'>},
  'names': ['--z']}]
"""
    assert buf == buf_expected



def test_fn_create_args_from_cfg__with_kwargs_argument():
    schema = [
        Schema("username", default="guest", field_type=str),
        Schema("userrole", domain=("admin", "marketing"), field_type=str),
        Schema("debug|d", default=False, field_type=bool),
        Schema("no_wrap", default=True, field_type=bool),
        Schema("timeout|t", default=10, field_type=(float, int), r_min=1, r_max=60),
        Schema("count", default=5, r_min=1, r_max=10, field_type=int),
        Schema("v", default=1, field_type=int, help_text=None, help_add_default=True),
        Schema("w", default=1, field_type=int, help_text=None, help_add_default=False),
        Schema("x", default=1, field_type=int, help_text="Helptext for option x",),
        Schema("y", default=2, field_type=int, help_text="Helptext for option y", help_add_default=True),
        Schema("z", default="abc", field_type=str, help_text="Helptext for option z", help_add_default=False)
    ]

    kwargs = {  "v" : {"help" : "Help from kwargs for v", "default" : 111},
                "w" : {"help" : "Help from kwargs for w", "default" : 222},
                "x" : {"help" : "Help from kwargs for x", "default" : 333},
                "y" : {"help" : "Help from kwargs for y", "default" : 444},
                "z" : {"help" : "Help from kwargs for z", "default" : '555'},
                "username" : {"default" : "Alice"},
              }

    cfg = Config.config_factory(schema)
    args = cli.create_args_from_cfg(cfg, cfg_kwargs=kwargs)
    buf = io.StringIO()
    pprint.pprint(args, stream=buf)
    buf = buf.getvalue()
    buf_expected = """\
[{'kwargs': {'default': 'Alice',
             'dest': 'username',
             'help': "Option: username (default 'guest')",
             'metavar': 'CHARS',
             'nargs': '?',
             'type': <class 'str'>},
  'names': ['--username']},
 {'kwargs': {'dest': 'userrole',
             'help': "Option: userrole (default 'None')",
             'metavar': 'CHARS',
             'nargs': '?',
             'type': <class 'str'>},
  'names': ['--userrole']},
 {'kwargs': {'action': 'store_true',
             'dest': 'debug',
             'help': "Option: debug (default 'False')"},
  'names': ['-d', '--debug']},
 {'kwargs': {'action': 'store_true',
             'dest': 'no_wrap',
             'help': "Option: no_wrap (default 'True')"},
  'names': ['--no-wrap']},
 {'kwargs': {'dest': 'timeout',
             'help': "Option: timeout (default '10')",
             'nargs': '?',
             'type': <class 'float'>},
  'names': ['-t', '--timeout']},
 {'kwargs': {'dest': 'count',
             'help': "Option: count (default '5')",
             'metavar': 'NUM',
             'nargs': '?',
             'type': <class 'int'>},
  'names': ['--count']},
 {'kwargs': {'default': 111,
             'dest': 'v',
             'help': 'Help from kwargs for v',
             'metavar': 'NUM',
             'nargs': '?',
             'type': <class 'int'>},
  'names': ['--v']},
 {'kwargs': {'default': 222,
             'dest': 'w',
             'help': 'Help from kwargs for w',
             'metavar': 'NUM',
             'nargs': '?',
             'type': <class 'int'>},
  'names': ['--w']},
 {'kwargs': {'default': 333,
             'dest': 'x',
             'help': 'Help from kwargs for x',
             'metavar': 'NUM',
             'nargs': '?',
             'type': <class 'int'>},
  'names': ['--x']},
 {'kwargs': {'default': 444,
             'dest': 'y',
             'help': 'Help from kwargs for y',
             'metavar': 'NUM',
             'nargs': '?',
             'type': <class 'int'>},
  'names': ['--y']},
 {'kwargs': {'default': '555',
             'dest': 'z',
             'help': 'Help from kwargs for z',
             'metavar': 'CHARS',
             'nargs': '?',
             'type': <class 'str'>},
  'names': ['--z']}]
"""
    assert buf == buf_expected
    parser, parsed_args = cli.run_parser(cfg, args, cli_args=[])
    assert repr(parsed_args) == "Namespace(username='Alice', v=111, w=222, x=333, y=444, z='555')"
    assert parsed_args.username == 'Alice'
    assert cfg.v == 111 
    assert cfg.w == 222
    assert cfg.z == '555'


def test_fn_run_parser__defaults():

    schema = [
        Schema("username", default="guest", field_type=str),
        Schema("userrole", domain=("admin", "marketing"), field_type=str),
        Schema("debug|d", default=False, field_type=bool),
        Schema("no_wrap", default=True, field_type=bool),
        Schema("timeout|t", default=10, field_type=(int, float), r_min=1, r_max=60),
        Schema("count", default=5, r_min=1, r_max=10, field_type=int),
        Schema("v", default=1, field_type=int, help_text=None, help_add_default=True),
        Schema("w", default=1, field_type=int, help_text=None, help_add_default=False),
        Schema("x", default=1, field_type=int, help_text="Helptext for option x",),
        Schema("y", default=2, field_type=int, help_text="Helptext for option y", help_add_default=True),
        Schema("z", default="abc", field_type=str, help_text="Helptext for option z", help_add_default=False)
    ]
    cfg = Config.config_factory(schema)
    cfg_copy = cfg.copy_config()
    args = cli.create_args_from_cfg(cfg)
    parser, parsed_args = cli.run_parser(cfg, args, cli_args=[])
    cfg_copy_2 = cfg.copy_config()
    assert cfg_copy_2 == cfg_copy
    



