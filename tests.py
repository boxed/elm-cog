from cog import reset, result
from elm import *


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
    list_of('foo', 'A, B, C', single_line=True, last_item=False)
    assert """foo = [A, B, C]""" == result()


def test_union():
    reset()
    union('Foo', 'A, B, C')
    assert """

type Foo
    = A
    | B
    | C



""" == result()


def test_union_single_line():
    reset()
    union('Foo', 'A, B, C', single_line=True, last_item=False)
    assert """type Foo = A | B | C""" == result()


def test_enum():
    reset()
    enum('Foo', 'A, B, C')
    assert """

type Foo
    = A
    | B
    | C


foo_list = [A, B, C]


""" == result()


def test_record_alias():
    reset()
    record_alias('Foo', 'A : Int, B : Float, C : String')
    assert """

type alias Foo =
    { A : Int
    , B : Float
    , C : String
    }



""" == result()


def test_record():
    reset()
    record('foo', 'a = 1, b = 1.5, c = "bar"')
    assert """

foo =
    { a = 1
    , b = 1.5
    , c = "bar"
    }



""" == result()


def test_enhanced_enum():
    reset()
    enhanced_enum(
        'Foo',
        'a : Int, b : Float, c : String',
        dict(
            A=(1, 1.5, "3"),
            B=(2, 2.5, "4"),
            C=(3, 3.5, "5"),
        )
    )
    assert """

type Foo
    = A
    | B
    | C


foo_list = [A, B, C]

type alias Foo_row =
    { a : Int
    , b : Float
    , c : String
    }


foo = Dict.fromList
    [ (A, Foo 1 1.5 "3")
    , (B, Foo 2 2.5 "4")
    , (C, Foo 3 3.5 "5")
    ]



""" == result()
