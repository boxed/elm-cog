from collections import OrderedDict
from contextlib import contextmanager
import re

from typing import Optional, List, Union, Dict

try:
    import cog
except:
    # For tests
    cog = None

NoneType = type(None)  # types.NoneType does not exist in python 3
String = str
Int = int
Float = float
Bool = bool
Maybe = Optional


class ElmLiteral:
    def __init__(self, s):
        self.s = s

    def __str__(self):
        return self.s


def snake_to_camel(s):
    return re.sub(r'(?:^|_)(\w)', lambda x: x.group(1).upper(), s)


def lower_first(s):
    return s[0].lower() + s[1:]


def upper_first(s):
    return s[0].upper() + s[1:]


def elm_literal(s):
    if isinstance(s, ElmLiteral):
        return str(s)

    if isinstance(s, str):
        return '"{}"'.format(s)

    return '{}'.format(s)


def elm_type_by_python_type(t, is_nested=False):
    def wrap_if_nested(x):
        if is_nested:
            return "(" + x + ")"
        else:
            return x

    if isinstance(t, ElmLiteral):
        return str(t)

    if isinstance(t, str):
        return t

    typing_origin = getattr(t, '__origin__', None)
    if typing_origin is List:
        return wrap_if_nested('List {}'.format(elm_type_by_python_type(t.__args__[0], is_nested=True)))

    if typing_origin is Dict:
        return wrap_if_nested('Dict {} {}'.format(elm_type_by_python_type(t.__args__[0], is_nested=True), elm_type_by_python_type(t.__args__[1], is_nested=True)))

    if typing_origin is Union and t.__args__[1] is NoneType:
        return wrap_if_nested('Maybe {}'.format(elm_type_by_python_type(t.__args__[0], is_nested=True)))

    if '_ForwardRef' in str(t):
        return t.__forward_arg__

    return {
        int: 'Int',
        float: 'Float',
        str: 'String',
        bool: 'Bool',
    }.get(t, t.__name__)


def parse_list(items):
    if isinstance(items, (tuple, list)):
        return items
    return [x.strip() for x in items.split(',')]


def _indent(s):
    lines = s.split('\n')
    return '\n'.join(['    ' + x if x else '' for x in lines])


def indent(s, levels=1):
    result = s
    for i in range(levels):
        result = _indent(result)
    return result


_has_started_whitespace = False


@contextmanager
def whitespace():
    global _has_started_whitespace
    if not _has_started_whitespace:
        should_surround = True
        _has_started_whitespace = True
    else:
        should_surround = False

    cog.out('\n\n')

    yield

    if should_surround:
        cog.out('\n\n\n\n')
    else:
        cog.out('\n')

    if should_surround:
        _has_started_whitespace = False


# decorator
def elm_whitespace(f):
    def wrapper(*args, **kwargs):
        with whitespace():
            r = f(*args, **kwargs)
        return r
    return wrapper


def _list_single_line(items, start_char='[', end_char=']', item_separator_char=','):
    if not isinstance(items, list):
        items = parse_list(items)

    if not items:
        return '{}{}'.format(start_char, end_char)

    r = '{} {}'.format(start_char, items[0])

    for item in items[1:]:
        r += '{} {}'.format(item_separator_char, item)

    if end_char:
        r += ' {}'.format(end_char)

    return r


def _list(items, start_char='[', end_char=']', item_separator_char=','):
    if not isinstance(items, list):
        items = parse_list(items)

    if not items:
        return '{}{}\n'.format(start_char, end_char)

    r = '{} {}'.format(start_char, items[0])

    for item in items[1:]:
        r += '\n{} {}'.format(item_separator_char, item)

    if end_char:
        r += '\n{}'.format(end_char)

    return r


def _list_of(name, items, start_char='[', end_char=']', item_separator_char=',', single_line=False):
    f = _list_single_line if single_line else _list
    l = f(
        items=items,
        start_char=start_char,
        end_char=end_char,
        item_separator_char=item_separator_char,
    )
    if name:
        return '{} =\n'.format(name) + indent(l)
    else:
        return l


@elm_whitespace
def list_of(name, items, start_char='[', end_char=']', item_separator_char=',', single_line=False):
    cog.out(_list_of(
        name=name,
        items=items,
        start_char=start_char,
        end_char=end_char,
        item_separator_char=item_separator_char,
        single_line=single_line,
    ))


def _union(name, definition):
    r = ''
    if name:
        r = 'type {}\n'.format(name)
    return r + indent(_list(
        items=definition,
        start_char='=',
        end_char='',
        item_separator_char='|',
    ))


@elm_whitespace
def union(name, definition):
    cog.out(_union(name=name, definition=definition))


def _enum(name, definition):
    return """{}


{}List =
    {}""".format(_union(name, definition), lower_first(name), _list_single_line(definition))


@elm_whitespace
def enum(name, definition):
    cog.out(_enum(name=name, definition=definition))


def _type_alias(name, type_info):
    return 'type alias {} =\n'.format(name) + indent(_list(
        items=['{} : {}'.format(item, elm_type_by_python_type(type_info[item])) for item in type_info.keys()],
        start_char='{',
        end_char='}',
    ))


@elm_whitespace
def type_alias(name, type_info):
    cog.out(_type_alias(name=name, type_info=type_info))
    return dict(name=name, type_info=type_info)


def _type_alias_with_json(name, type_info, decoder=True, encoder=True):
    r = [_type_alias(name=name, type_info=type_info)]

    if decoder:
        r.append(_decoder(name, type_info))

    if encoder:
        r.append(_encoder(name, type_info))

    return '\n\n\n'.join(r)


def _decoder_name_for_type(t):
    if isinstance(t, str):
        return lower_first(t) + 'Decoder'

    if isinstance(t, ElmLiteral):
        return lower_first(str(t)) + 'Decoder'

    typing_origin = getattr(t, '__origin__', None)
    if typing_origin is List:
        return '(Json.Decode.list {})'.format(_decoder_name_for_type(t.__args__[0]))

    if typing_origin is Dict:
        assert t.__args__[0] is str
        return '(Json.Decode.dict {})'.format(_decoder_name_for_type(t.__args__[1]))

    if typing_origin is Union and t.__args__[1] is NoneType:
        return '(Json.Decode.maybe {})'.format(_decoder_name_for_type(t.__args__[0]))

    if '_ForwardRef' in str(t):
        return _decoder_name_for_type(t.__forward_arg__)

    return {
        int: 'Json.Decode.int',
        float: 'Json.Decode.float',
        str: 'Json.Decode.string',
        bool: 'Json.Decode.bool',
    }.get(t, lower_first(t.__name__) + 'Decoder')


def _encoder(name, type_info):
    def encoder_name_for_type(t):
        return _decoder_name_for_type(t).replace("Decode", "Encode")

    encoder_fields = ['( "{}", {} record.{} )'.format(key, encoder_name_for_type(value), key) for key, value in type_info.items()]
    encoder_name = '{}Encoder'.format(lower_first(name))
    return """{} : {} -> Json.Encode.Value
{} record =
    Json.Encode.object
{}""".format(encoder_name, name, encoder_name, indent(_list(encoder_fields), levels=2))


def _decoder(name, type_info):
    decoder_fields = '\n'.join(['|> Json.Decode.Pipeline.required "{}" {}'.format(key, _decoder_name_for_type(value)) for key, value in type_info.items()])
    decoder_name = '{}Decoder'.format(lower_first(name))
    return """{} : Json.Decode.Decoder {}
{} =
    Json.Decode.Pipeline.decode {}
{}""".format(decoder_name, name, decoder_name, name, indent(decoder_fields, levels=2))


@elm_whitespace
def decoder_for_type_alias(name, type_info):
    cog.out(_decoder(name=name, type_info=type_info))


@elm_whitespace
def encoder_for_type_alias(name, type_info):
    cog.out(_encoder(name=name, type_info=type_info))


@elm_whitespace
def type_alias_with_json(name, type_info, decoder=True, encoder=True):
    cog.out(_type_alias_with_json(name=name, type_info=type_info, decoder=decoder, encoder=encoder))


def _record(definition):
    return _list(['{} = {}'.format(key, elm_literal(value)) for key, value in definition.items()], start_char='{', end_char='}')


def _named_record(name, definition):
    return '{} =\n'.format(name) + indent(_record(definition=definition))


@elm_whitespace
def record(name, definition):
    cog.out(_named_record(name=name, definition=definition))


def _enhanced_enum(name, rows, type_info=None):
    if type_info is None:
        type_info = OrderedDict([(key, elm_type_by_python_type(type(value))) for key, value in list(rows.values())[0].items()])

    enum_definition = list(rows.keys())
    r = _enum(name, enum_definition)

    r += '\n\n\n'

    r += _type_alias(name=name + 'Row', type_info=OrderedDict([(lower_first(k), v) for k, v in type_info.items()]))

    r += '\n\n\n'

    def to_str(value):
        return " ".join([elm_literal(x) for x in value])

    items = '\n'.join(['{} ->\n'.format(key) + indent('{}Row {}\n'.format(name, to_str(list(value.values())))) for key, value in rows.items()])
    items = items[:-1]  # remove last newline
    r += """\
{}Data : {} -> {}
{}Data input =
    case input of
{}""".format(lower_first(name), name, name + 'Row', lower_first(name), indent(items, levels=2))

    if 'display_name' in type_info:
        r += '\n\n\n'

        items = '\n'.join(['{} ->\n'.format(key) + indent('{}\n'.format(elm_literal(value['display_name']))) for key, value in rows.items()])
        items = items[:-1]  # remove last newline

        r += """\
{}ToDisplayName : {} -> String
{}ToDisplayName data =
    case data of
{}""".format(lower_first(name), name, lower_first(name), indent(items, levels=2))

    if 'name' in type_info:
        r += '\n\n\n'

        items = '\n'.join(['{} ->\n'.format(elm_literal(value['name'])) + indent('{}\n'.format(key)) for key, value in rows.items()])

        default_item = list(rows.items())[0]

        r += """\
{}ByName : String -> {}
{}ByName name =
    case name of
{}
        _ ->
{}""".format(lower_first(name), name, lower_first(name), indent(items, levels=2), indent(default_item[0], levels=3))
    return r


@elm_whitespace
def enhanced_enum(name, rows, type_info=None):
    cog.out(_enhanced_enum(name=name, type_info=type_info, rows=rows))
