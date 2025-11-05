# test_config_ipsum.py
# copied from the ipsumheroes project

import pprint
from dataclasses import fields
import re
import pytest
from konvigius import Config, Schema
from konvigius.exceptions import ConfigError, ConfigTypeError, ConfigRangeError

# -----------------------------------------------------------------------------
# Fixtures
# -----------------------------------------------------------------------------

@pytest.fixture
def schema():
    from ipsum_schema import SCHEMA
    return SCHEMA

@pytest.fixture
def cfg_fix(schema):
    return Config.config_factory(schema)

# -----------------------------------------------------------------------------
# Functional Tests: Config Creation
# -----------------------------------------------------------------------------

def test_config_initialization(cfg_fix):

    assert cfg_fix.paragraphs == 1
    assert cfg_fix.sentences == 0
    
    # === Paragraph / Sentence Structure ===
    
    assert cfg_fix.newlines == 1
    assert cfg_fix.min_sentences == 3
    assert cfg_fix.max_sentences == 8
    assert cfg_fix.max_sections == 2
    assert cfg_fix.min_words == 3
    assert cfg_fix.max_words == 12
     
    # === Indentation ===
     
    assert cfg_fix.indent_first == 7
    assert cfg_fix.indent_next == 3
     
    # === Sentence Formatting ===
     
    assert cfg_fix.sentence_ending_punct == "!??......"
    assert cfg_fix.sentence_ending_spaces == 2
     
    # === Wrapping ===
     
    assert cfg_fix.width == 79
    assert cfg_fix.no_wrap == False
     
    # === Luminary Interpolation ===
     
    assert cfg_fix.with_luminaries == False
    assert cfg_fix.luminary_probability == 3
    assert cfg_fix.luminary_lang == "en"
     
    # === Annotation ===
     
    assert cfg_fix.show_annotation == False
    assert cfg_fix.anno_width == 69
    assert cfg_fix.anno_indent_first == 4
    assert cfg_fix.anno_indent_next == 6
    assert cfg_fix.anno_heading_1 == "- Who They Were -"
    assert cfg_fix.anno_heading_2 == "-" * 17
     
    # === HTML/XML Tagging ===
     
    assert cfg_fix.tag_paragraph_start == None
    assert cfg_fix.tag_paragraph_end == None
    assert cfg_fix.tag_sentence_start == None
    assert cfg_fix.tag_sentence_end == None
    assert cfg_fix.tag_luminary_start == " <"
    assert cfg_fix.tag_luminary_end == "> "


def test_config_computed(cfg_fix):
    assert cfg_fix.spaces == '  '


def test_allows_assignment(cfg_fix):
    cfg_fix.sentences = 45
    cfg_fix.no_wrap = True
    assert cfg_fix.sentences == 45
    assert cfg_fix.no_wrap is True


def test_valid_min_max_ranges(cfg_fix):
    """Ensure that all min/max pairs satisfy max ≥ min."""
    for option in cfg_fix._metadata.values():
        # Only validate int fields with min/max constraints
        if (option.r_min is not None and option.r_max is not None):
            assert option.r_max >= option.r_min, f"{option.name=}"


def test_defaultvalue_between_min_max_ranges(cfg_fix):
    """Ensure that all min/max pairs satisfy max ≥ min."""
    for option in cfg_fix._metadata.values():

        # Only validate int fields with min/max constraints
        if (option.r_min is not None):
            assert option.r_min <= option.default_value 
            assert option.r_max >= cfg_fix._values[option.name]

        if (option.r_max is not None):
            assert option.r_max >= option.default_value 
            assert option.r_max >= cfg_fix._values[option.name]


def test_out_of_range_raises(cfg_fix):
    with pytest.raises(ConfigRangeError):
        cfg_fix.paragraphs = -1
    with pytest.raises(ConfigRangeError):
        cfg_fix.paragraphs = 5001 

    with pytest.raises(ConfigRangeError):
        cfg_fix.sentences = -1
    with pytest.raises(ConfigRangeError):
        cfg_fix.sentences = 5001 

    with pytest.raises(ConfigRangeError):
        cfg_fix.min_sentences = 0
    with pytest.raises(ConfigRangeError):
        cfg_fix.min_sentences = 5001 

    with pytest.raises(ConfigRangeError):
        cfg_fix.max_sentences = 0
    with pytest.raises(ConfigRangeError):
        cfg_fix.max_sentences = 5001 

    with pytest.raises(ConfigRangeError):
        cfg_fix.min_words = 0 
    with pytest.raises(ConfigRangeError):
        cfg_fix.min_words = 31 

    with pytest.raises(ConfigRangeError):
        cfg_fix.max_words = 0 
    with pytest.raises(ConfigRangeError):
        cfg_fix.max_words = 31 

    with pytest.raises(ConfigRangeError):
        cfg_fix.max_sections = 0 
    with pytest.raises(ConfigRangeError):
        cfg_fix.max_sections = 6

    with pytest.raises(ConfigRangeError):
        cfg_fix.newlines = -1
    with pytest.raises(ConfigRangeError):
        cfg_fix.newlines = 5001

    with pytest.raises(ConfigRangeError):
        cfg_fix.sentence_ending_spaces = 0 
    with pytest.raises(ConfigRangeError):
        cfg_fix.sentence_ending_spaces = 11

    with pytest.raises(ConfigRangeError):
        cfg_fix.width = 4
    with pytest.raises(ConfigRangeError):
        cfg_fix.width = 5001

    with pytest.raises(ConfigRangeError):
        cfg_fix.indent_first = -1
    with pytest.raises(ConfigRangeError):
        cfg_fix.indent_first = 51

    with pytest.raises(ConfigRangeError):
        cfg_fix.indent_next = -1
    with pytest.raises(ConfigRangeError):
        cfg_fix.indent_next = 51

    with pytest.raises(ConfigRangeError):
        cfg_fix.anno_width = 4
    with pytest.raises(ConfigRangeError):
        cfg_fix.anno_width= 5001

    with pytest.raises(ConfigRangeError):
        cfg_fix.anno_indent_first = -1
    with pytest.raises(ConfigRangeError):
        cfg_fix.anno_indent_first = 51

    with pytest.raises(ConfigRangeError):
        cfg_fix.anno_indent_next = -1
    with pytest.raises(ConfigRangeError):
        cfg_fix.anno_indent_next = 51


def test_wrong_type_raises(cfg_fix):
    with pytest.raises(ConfigTypeError):
        cfg_fix.paragraphs = "goodmorning"
    with pytest.raises(ConfigTypeError):
        cfg_fix.sentence_ending_punct = 123


def test_tag_fields_optional(cfg_fix):
    """Ensure that optional tag fields can be left unset."""
    assert cfg_fix.tag_paragraph_start is None
    assert cfg_fix.tag_paragraph_end is None
    assert cfg_fix.tag_sentence_start is None
    assert cfg_fix.tag_sentence_end is None


def test_default_strings(cfg_fix):
    assert cfg_fix.sentence_ending_punct == "!??......"
    assert cfg_fix.luminary_lang == "en"
    assert cfg_fix.anno_heading_1 == "- Who They Were -"
    assert cfg_fix.anno_heading_2 == "-" * 17
    assert cfg_fix.tag_luminary_start == " <"
    assert cfg_fix.tag_luminary_end == "> "


def test_assign_to_computed_field_raises(cfg_fix):
    with pytest.raises(AttributeError):
        cfg_fix.spaces = 'x'


def test_create_config_from_dict_1(schema):
    cfg = Config.from_dict(schema, {'sentence_ending_spaces' : 5, 'max_words' : 27})
    assert cfg.sentence_ending_spaces == 5
    assert cfg.spaces == '     '
    assert cfg.max_words == 27


def test_create_config_from_dict_2(schema):
    cfg = Config.from_dict(schema, {"no_wrap" : True, "min_sentences" : 13, 'max_sentences' : 15})
    assert cfg.wrap is False
    assert cfg.no_wrap is True
    assert cfg.min_sentences == 13 
    assert cfg.max_sentences == 15 


@pytest.mark.parametrize('args', [(1,2), (1,3), (10,11), (10,12), (13, 13)])
def test_min_sentences_lt_max_sentences(schema, args):
    cfg = Config.from_dict(schema, {'min_sentences': args[0], 'max_sentences': args[1]})
    assert cfg.min_sentences <= cfg.max_sentences 


@pytest.mark.parametrize('args', [(10,9), (11,10)])
def test_min_sentences_gt_max_sentences_raises(schema, args):
    with pytest.raises(ConfigRangeError):
        cfg = Config.from_dict(schema, {'min_sentences': args[0], 'max_sentences': args[1]})

# === END ===

