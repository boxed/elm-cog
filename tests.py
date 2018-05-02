from collections import OrderedDict

from elm import indent, _union, _enum, _type_alias, ElmLiteral, _enhanced_enum, _type_alias_with_json, _list_of, _named_record


def test_indent():
    assert indent('') == ''
    assert indent('a\nb') == '    a\n    b'


def test_list_of():
    result = _list_of('foo', 'A, B, C')
    assert """

foo =
    [ A
    , B
    , C
    ]

""".strip() == result


def test_list_of_single_line():
    result = _list_of('foo', 'A, B, C', single_line=True)
    assert """

foo =
    [ A, B, C ]

""".strip() == result


def test_union():
    result = _union('Foo', 'A, B, C')
    assert """

type Foo
    = A
    | B
    | C

""".strip() == result


def test_enum():
    result = _enum('FooBar', 'A, B, C')
    assert """

type FooBar
    = A
    | B
    | C


fooBarList =
    [ A, B, C ]

""".strip() == result


def test_type_alias():
    result = _type_alias('FooBar', type_info=OrderedDict([('a', int), ('b', float), ('c', str)]))
    assert """

type alias FooBar =
    { a : Int
    , b : Float
    , c : String
    }

""".strip() == result


def test_record():
    result = _named_record('foo', OrderedDict([('a', 1), ('b', 1.5), ('c', "bar"), ('d', ElmLiteral('D'))]))
    assert """

foo =
    { a = 1
    , b = 1.5
    , c = "bar"
    , d = D
    }

""".strip() == result


def test_enhanced_enum():
    result = _enhanced_enum(
        'FooBar',
        OrderedDict([
            ('A', OrderedDict([('some_data1', 1), ('some_data2', 1.5), ('display_name', "3")])),
            ('B', OrderedDict([('some_data1', 2), ('some_data2', 2.5), ('display_name', "4")])),
            ('C', OrderedDict([('some_data1', 3), ('some_data2', 3.5), ('display_name', "5")])),
        ])
    )
    assert """

type FooBar
    = A
    | B
    | C


fooBarList =
    [ A, B, C ]


type alias FooBarRow =
    { some_data1 : Int
    , some_data2 : Float
    , display_name : String
    }


fooBarData : FooBar -> FooBarRow
fooBarData input =
    case input of
        A ->
            FooBarRow 1 1.5 "3"

        B ->
            FooBarRow 2 2.5 "4"

        C ->
            FooBarRow 3 3.5 "5"


fooBarToDisplayName : FooBar -> String
fooBarToDisplayName data =
    case data of
        A ->
            "3"

        B ->
            "4"

        C ->
            "5"
""".strip() == result


def test_type_alias_with_json():
    result = _type_alias_with_json('FooBar', type_info=OrderedDict([('a', int), ('b', float), ('c', str), ('d', 'CustomType')]))
    assert """

type alias FooBar =
    { a : Int
    , b : Float
    , c : String
    , d : CustomType
    }


fooBarDecoder : Json.Decode.Decoder FooBar
fooBarDecoder =
    Json.Decode.Pipeline.decode FooBar
        |> Json.Decode.Pipeline.required "a" Json.Decode.int
        |> Json.Decode.Pipeline.required "b" Json.Decode.float
        |> Json.Decode.Pipeline.required "c" Json.Decode.string
        |> Json.Decode.Pipeline.required "d" customTypeDecoder


fooBarEncoder : FooBar -> Json.Encode.Value
fooBarEncoder record =
    Json.Encode.object
        [ ( "a", Json.Encode.int record.a )
        , ( "b", Json.Encode.float record.b )
        , ( "c", Json.Encode.string record.c )
        , ( "d", customTypeEncoder record.d )
        ]

""".strip() == result
