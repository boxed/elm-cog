module Main exposing (..)

import Dict


-- [[[cog list_of('foo', '1, 2, 3') ]]]


foo =
    [ 1
    , 2
    , 3
    ]



-- [[[end]]]
-- [[[cog union('Foo', 'A, B, C') ]]]


type Foo
    = A
    | B
    | C



-- [[[end]]]
-- [[[cog enum('Foo', 'A, B, C') ]]]


type Foo
    = A
    | B
    | C


foo_list =
    [ A, B, C ]



-- [[[end]]]
-- [[[cog record_alias('Foo', 'a : Int, b : String') ]]]


type alias Foo =
    { a : Int
    , b : String
    }



-- [[[end]]]
-- [[[cog record('foo', 'a = 1, b = 1.5, c = "bar"') ]]]


foo =
    { a = 1
    , b = 1.5
    , c = "bar"
    }



-- [[[end]]]
-- [[[cog
-- enhanced_enum(
--     'Foo',
--     'A, B, C',
--     'some_data1 : Int, some_data2 : Float, display_name : String',
--     dict(
--         A=(1, 1.5, "3"),
--         B=(2, 2.5, "4"),
--         C=(3, 3.5, "5"),
--     )
-- )
-- ]]]


type Foo
    = A
    | B
    | C


foo_list =
    [ A, B, C ]


type alias Foo_row =
    { some_data1 : Int
    , some_data2 : Float
    , display_name : String
    }


foo =
    Dict.fromList
        [ ( A, Foo 1 1.5 "3" )
        , ( B, Foo 2 2.5 "4" )
        , ( C, Foo 3 3.5 "5" )
        ]



-- [[[end]]]
