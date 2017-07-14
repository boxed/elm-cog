import cog


def parse_list(items):
    return [x.strip() for x in items.split(',')]


def list_of(name, items, start_char='[', end_char=']', end_of_definition_line='=', item_separator_char=',', prefix=None, last_item=True):
    cog.out('\n\n')

    if prefix:
        cog.out(prefix)

    if not isinstance(items, list):
        items = parse_list(items)

    if not items:
        cog.outl(f'{name} = {start_char}{end_char}')
    else:
        if end_of_definition_line:
            cog.outl(f'{name} =')
        else:
            cog.outl(f'{name}')

        cog.outl(f'    {start_char} {items[0]}')

        for item in items[1:]:
            cog.outl(f'    {item_separator_char} {item}')

        if end_char:
            cog.outl(f'    {end_char}')

    if last_item:
        cog.out('\n\n\n')


def union(name, definition, last_item=True):
    list_of(name, definition, prefix='type ', start_char='=', end_char='', end_of_definition_line='', item_separator_char='|', last_item=last_item)


def enum(name, definition, last_item=True):
    union(name, definition, last_item=False)
    list_of(name.lower() + '_list', definition, last_item=last_item)
    

def record_alias(name, definition, last_item=True):
    list_of(name, definition, start_char='{', end_char='}', prefix='type alias ', last_item=last_item)

