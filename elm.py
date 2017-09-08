from typing import *

import cog


String = str
Int = int
Float = float
Bool = bool
Maybe = Optional


def lower_first(s):
    return s[0].lower() + s[1:]


class ElmLiteral:
    def __init__(self, s):
        self.s = s

    def __str__(self):
        return self.s


def elm_literal(s):
    if isinstance(s, ElmLiteral):
        return str(s)

    if isinstance(s, str):
        return f'"{s}"'

    return f'{s}'


def elm_type_by_python_type(t):
    if isinstance(t, ElmLiteral):
        return str(t)

    typing_origin = getattr(t, '__origin__', None)
    if typing_origin is List:
        return f'( List {elm_type_by_python_type(t.__args__[0])} )'

    if typing_origin is Dict:
        return f'( Dict {elm_type_by_python_type(t.__args__[0])} {elm_type_by_python_type(t.__args__[1])} )'

    if typing_origin is Union and t.__args__[1] is type(None):
        return f'( Maybe {elm_type_by_python_type(t.__args__[0])} )'

    if '_ForwardRef' in str(t):
        return t.__forward_arg__

    return {
        int: 'Int',
        float: 'Float',
        str: 'String',
        bool: 'Bool',
    }.get(t, t)


def parse_list(items: Union[tuple, list, str]):
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


def elm_whitespace(f):
    def wrapper(*args, **kwargs):
        cog.out('\n\n')
        f(*args, **kwargs)
        cog.out('\n\n\n\n')
    return wrapper


def _list_single_line(items, *, start_char='[', end_char=']', item_separator_char=','):
    if not isinstance(items, list):
        items = parse_list(items)

    if not items:
        return f'{start_char}{end_char}'

    r = f'{start_char} {items[0]}'

    for item in items[1:]:
        r += f'{item_separator_char} {item}'

    if end_char:
        r += f' {end_char}'

    return r


def _list(items, *, start_char='[', end_char=']', item_separator_char=','):
    if not isinstance(items, list):
        items = parse_list(items)

    if not items:
        return f'{start_char}{end_char}\n'

    r = f'{start_char} {items[0]}'

    for item in items[1:]:
        r += f'\n{item_separator_char} {item}'

    if end_char:
        r += f'\n{end_char}'

    return r


@elm_whitespace
def list_of(name, items, *, start_char='[', end_char=']', item_separator_char=',', single_line=False):
    cog.outl(f'{name} =')
    f = _list_single_line if single_line else _list
    cog.out(indent(f(
        items=items,
        start_char=start_char,
        end_char=end_char,
        item_separator_char=item_separator_char,
    )))


def _union(name, definition):
    return f'type {name}\n' + indent(_list(
        items=definition,
        start_char='=',
        end_char='',
        item_separator_char='|',
    ))


@elm_whitespace
def union(name, definition):
    cog.out(_union(name=name, definition=definition))


def _enum(name, definition):
    return f"""{_union(name, definition)}


{lower_first(name)}_list =
    {_list_single_line(definition)}"""


@elm_whitespace
def enum(name, definition):
    cog.out(_enum(name=name, definition=definition))
    

def _type_alias(name, type_info):
    return f'type alias {name} =\n' + indent(_list(
        items=[f'{item} : {elm_type_by_python_type(type_info[item])}' for item in type_info.keys()],
        start_char='{',
        end_char='}',
    ))


@elm_whitespace
def type_alias(name, type_info):
    cog.out(_type_alias(name=name, type_info=type_info))


def _type_alias_with_json(name, type_info, decoder, encoder):
    r = [_type_alias(name=name, type_info=type_info)]

    if decoder:
        def decoder_name_for_type(t):
            if isinstance(t, str):
                return lower_first(t) + 'Decoder'

            typing_origin = getattr(t, '__origin__', None)
            if typing_origin is List:
                return f'( Json.Decode.list {decoder_name_for_type(t.__args__[0])} )'

            if typing_origin is Dict:
                assert t.__args__[0] is str
                return f'( Json.Decode.dict {decoder_name_for_type(t.__args__[1])} )'

            if typing_origin is Union and t.__args__[1] is type(None):
                return f'( Json.Decode.maybe {decoder_name_for_type(t.__args__[0])} )'

            if '_ForwardRef' in str(t):
                return decoder_name_for_type(t.__forward_arg__)

            return {
                int: 'Json.Decode.int',
                float: 'Json.Decode.float',
                str: 'Json.Decode.string',
                bool: 'Json.Decode.bool',
            }[t]

        decoder_fields = '\n'.join([f'|> Json.Decode.Pipeline.required "{key}" {decoder_name_for_type(value)}' for key, value in type_info.items()])

        decoder_name = f'{lower_first(name)}Decoder'
        r.append(f"""{decoder_name} : Json.Decode.Decoder {name}
{decoder_name} =
    Json.Decode.Pipeline.decode {name}
{indent(decoder_fields, levels=2)}""")

    if encoder:
        def encoder_name_for_type(t):
            return decoder_name_for_type(t).replace("Decode", "Encode")

        encoder_fields = [f'( "{key}", {encoder_name_for_type(value)} record.{key} )' for key, value in type_info.items()]
        encoder_name = f'{lower_first(name)}Encoder'
        r.append(f"""{encoder_name} : {name} -> Json.Encode.Value
{encoder_name} record =
    Json.Encode.object
{indent(_list(encoder_fields), levels=2)}""")

    return '\n\n\n'.join(r)


@elm_whitespace
def type_alias_with_json(name, type_info, decoder=True, encoder=True):
    cog.out(_type_alias_with_json(name=name, type_info=type_info, decoder=decoder, encoder=encoder))


def _record(definition: Dict[str, Any]):
    return _list([f'{key} = {elm_literal(value)}' for key, value in definition.items()], start_char='{', end_char='}')


@elm_whitespace
def record(name, definition: Dict[str, Any]):
    cog.out(f'{name} =\n' + indent(_record(definition=definition)))


def _enhanced_enum(name, rows, type_info):
    enum_definition = list(rows.keys())
    r = _enum(name, enum_definition)

    r += '\n\n\n'

    r += _type_alias(name=name + '_row', type_info={lower_first(k): v for k, v in type_info.items()})

    r += '\n\n\n'

    def to_str(value):
        return " ".join([elm_literal(x) for x in value])

    items = '\n'.join([f'{key} ->\n' + indent(f'{name}_row {to_str(value.values())}\n') for key, value in rows.items()])
    items = items[:-1]  # remove last newline
    r += f"""\
{lower_first(name)}_data input =
    case input of
{indent(items, levels=2)}"""
    return r


@elm_whitespace
def enhanced_enum(name, rows: Dict[str, dict], type_info=None):
    if type_info is None:
        type_info = {key: elm_type_by_python_type(type(value)) for key, value in list(rows.values())[0].items()}
    cog.out(_enhanced_enum(name=name, type_info=type_info, rows=rows))
