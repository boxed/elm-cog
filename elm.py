import cog


def parse_list(items):
    if isinstance(items, (tuple, list)):
        return items
    return [x.strip() for x in items.split(',')]


def _list_of(name, items, *, single_line=False, start_char='[', end_char=']', end_of_definition_line='=', item_separator_char=',', prefix=None, suffix='', compact_single_line_form=False, last_item=True):
    newline = '\n' if not single_line else ''
    tab = '    ' if not single_line else ' '
    if single_line and compact_single_line_form:
        tab = ''

    r = ''
    r += f'{newline}{newline}'

    if prefix:
        r += prefix

    if not isinstance(items, list):
        items = parse_list(items)

    if name:
        r += f'{name}'

    if not items:
        r += f' = {start_char}{end_char}{suffix}{newline}'
    else:
        if end_of_definition_line:
            if name:
                r += f' ={" " if not newline else ""}{suffix}{newline}'
            else:
                r += f'{newline}{suffix}'
        else:
            r += f'{newline}{suffix}'

        r += f'{tab}{start_char}{"" if single_line and start_char == "[" else " "}{items[0]}{newline}'

        for item in items[1:]:
            r += f'{tab}{item_separator_char} {item}{newline}'

        if end_char:
            r += f'{tab}{end_char}{newline}'

    if last_item:
        r += f'\n\n\n'

    return r


def list_of(name, items, *, single_line=False, start_char='[', end_char=']', end_of_definition_line='=', item_separator_char=',', compact_single_line_form=True, prefix=None, last_item=True):
    cog.out(_list_of(
        name=name,
        items=items,
        single_line=single_line,
        start_char=start_char,
        end_char=end_char,
        end_of_definition_line=end_of_definition_line,
        item_separator_char=item_separator_char,
        compact_single_line_form=compact_single_line_form,
        prefix=prefix,
        last_item=last_item,
    ))


def _union(name, definition, *, single_line=False, last_item=True):
    return _list_of(
        name=name,
        items=definition,
        prefix='type ',
        start_char='=',
        end_char='',
        end_of_definition_line='',
        item_separator_char='|',
        single_line=single_line,
        last_item=last_item,
    )


def union(name, definition, *, single_line=False, last_item=True):
    cog.out(_union(name=name, definition=definition, single_line=single_line, last_item=last_item))


def _enum(name, definition, *, last_item=True):
    r = _union(name, definition, last_item=False)
    r += '\n\n'
    r += _list_of(name.lower() + '_list', definition, single_line=True, compact_single_line_form=True, last_item=last_item)
    return r


def enum(name, definition, *, last_item=True):
    cog.out(_enum(name=name, definition=definition, last_item=last_item))
    

def _record_alias(name, definition, *, last_item=True):
    return _list_of(
        name=name,
        items=definition,
        start_char='{',
        end_char='}',
        prefix='type alias ',
        last_item=last_item,
    )


def record_alias(name, definition, *, last_item=True):
    cog.out(_record_alias(name=name, definition=definition, last_item=last_item))


def _record(name, definition, *, single_line=False, last_item=True):
    return _list_of(name, definition, single_line=single_line, start_char='{', end_char='}', last_item=last_item)


def record(name, definition, *, single_line=False, last_item=True):
    cog.out(_record(name=name, definition=definition, single_line=single_line, last_item=last_item))


def _enhanced_enum(name, enum_definition, definition, rows, *, last_item=True):
    r = _enum(name, enum_definition, last_item=False)
    assert len(parse_list(enum_definition)) == len(rows.keys())
    r += _record_alias(name + '_row', definition, last_item=False)

    def to_str(value):
        return " ".join([f'"{x}"' if isinstance(x, str) else f'{x}' for x in value])

    items = [f'({key}, {name} {to_str(value)})' for key, value in rows.items()]
    r += _list_of(name=name.lower(), items=items, suffix=' Dict.fromList', last_item=last_item)
    return r


def enhanced_enum(name, enum_definition, definition, rows, last_item=True):
    cog.out(_enhanced_enum(name=name, enum_definition=enum_definition, definition=definition, rows=rows, last_item=last_item))
