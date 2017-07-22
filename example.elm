module Main exposing (..)

-- [[[cog list_of('foo', '1, 2, 3') ]]]


foo =
    [ 1
    , 2
    , 3
    ]



-- [[[end]]]
-- [[[cog union('Bar', 'A, B, C') ]]]


type Bar
    = A
    | B
    | C



-- [[[end]]]
-- [[[cog enum('Baz', 'D, E, F') ]]]


type Baz
    = D
    | E
    | F


baz_list =
    [ D, E, F ]



-- [[[end]]]
-- [[[cog record_alias('Foobar', 'a : Int, b : String') ]]]


type alias Foobar =
    { a : Int
    , b : String
    }



-- [[[end]]]
-- [[[cog record('quux', 'a = 1, b = 1.5, c = "bar"') ]]]


quux =
    { a = 1
    , b = 1.5
    , c = "bar"
    }



-- [[[end]]]
-- [[[cog
-- enhanced_enum(
--     'EnhancedFoo',
--     'G, H, J',
--     'some_data1 : Int, some_data2 : Float, display_name : String',
--     dict(
--         A=(1, 1.5, "3"),
--         B=(2, 2.5, "4"),
--         C=(3, 3.5, "5"),
--     )
-- )
-- ]]]


type EnhancedFoo
    = G
    | H
    | J


enhancedfoo_list =
    [ G, H, J ]


type alias EnhancedFoo_row =
    { some_data1 : Int
    , some_data2 : Float
    , display_name : String
    }


enhancedfoo_data input =
    case input of
        A ->
            EnhancedFoo_row 1 1.5 "3"

        B ->
            EnhancedFoo_row 2 2.5 "4"

        C ->
            EnhancedFoo_row 3 3.5 "5"



-- [[[end]]]
