import cog


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


{name.lower()}_list =
    {_list_single_line(definition)}"""


@elm_whitespace
def enum(name, definition):
    cog.out(_enum(name=name, definition=definition))
    

def _record_alias(name, definition):
    return f'type alias {name} =\n' + indent(_list(
        items=definition,
        start_char='{',
        end_char='}',
    ))


@elm_whitespace
def record_alias(name, definition):
    cog.out(_record_alias(name=name, definition=definition))


def _record(name, definition):
    return _list(definition, start_char='{', end_char='}')


@elm_whitespace
def record(name, definition):
    cog.out(f'{name} =\n' + indent(_record(name=name, definition=definition)))


def _enhanced_enum(name, enum_definition, definition, rows):
    r = _enum(name, enum_definition)
    assert len(parse_list(enum_definition)) == len(rows.keys())

    r += '\n\n\n'

    r += _record_alias(name + '_row', definition)

    r += '\n\n\n'

    def to_str(value):
        return " ".join([f'"{x}"' if isinstance(x, str) else f'{x}' for x in value])

    items = '\n'.join([f'{key} ->\n' + indent(f'{name}_row {to_str(value)}\n') for key, value in rows.items()])
    items = items[:-1]  # remove last newline
    r += f"""\
{name.lower()}_data input =
    case input of
{indent(items, levels=2)}"""
    return r


@elm_whitespace
def enhanced_enum(name, enum_definition, definition, rows):
    cog.out(_enhanced_enum(name=name, enum_definition=enum_definition, definition=definition, rows=rows))
