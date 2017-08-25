from cog import reset, result
from elm import *


def test_indent():
    assert indent('') == ''
    assert indent('a\nb') == '    a\n    b'


def test_list_of():
    reset()
    list_of('foo', 'A, B, C')
    assert """

foo =
    [ A
    , B
    , C
    ]



""" == result()


def test_list_of_single_line():
    reset()
    list_of('foo', 'A, B, C', single_line=True)
    assert """

foo =
    [ A, B, C ]



""" == result()


def test_union():
    reset()
    union('Foo', 'A, B, C')
    assert """

type Foo
    = A
    | B
    | C



""" == result()


def test_enum():
    reset()
    enum('FooBar', 'A, B, C')
    assert """

type FooBar
    = A
    | B
    | C


fooBar_list =
    [ A, B, C ]



""" == result()


def test_record_alias():
    reset()
    record_alias('FooBar', type_info=dict(a=int, b=float, c=str))
    assert """

type alias FooBar =
    { a : Int
    , b : Float
    , c : String
    }



""" == result()


def test_record():
    reset()
    record('foo', dict(a=1, b=1.5, c="bar", d=ElmLiteral('D')))
    assert """

foo =
    { a = 1
    , b = 1.5
    , c = "bar"
    , d = D
    }



""" == result()


def test_enhanced_enum():
    reset()
    enhanced_enum(
        'FooBar',
        dict(
            A=dict(some_data1=1, some_data2=1.5, display_name="3"),
            B=dict(some_data1=2, some_data2=2.5, display_name="4"),
            C=dict(some_data1=3, some_data2=3.5, display_name="5"),
        )
    )
    assert """

type FooBar
    = A
    | B
    | C


fooBar_list =
    [ A, B, C ]


type alias FooBar_row =
    { some_data1 : Int
    , some_data2 : Float
    , display_name : String
    }


fooBar_data input =
    case input of
        A ->
            FooBar_row 1 1.5 "3"

        B ->
            FooBar_row 2 2.5 "4"

        C ->
            FooBar_row 3 3.5 "5"



""" == result()


def test_record_alias_with_json():
    reset()
    record_alias_with_json('FooBar', type_info=dict(a=int, b=float, c=str, d='CustomType'))
    assert """

type alias FooBar =
    { a : Int
    , b : Float
    , c : String
    , d : CustomType
    }


fooBarDecoder : Decoder FooBar
fooBarDecoder =
    decode FooBar
        |> required "a" Json.int
        |> required "b" Json.float
        |> required "c" Json.string
        |> required "d" customTypeDecoder



""" == result()