module Main exposing (..)

import Json.Decode
import Json.Decode.Pipeline
import Json.Encode


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
-- [[[cog type_alias('Foobar', type_info=dict(a=int, b=str)) ]]]


type alias Foobar =
    { a : Int
    , b : String
    }



-- [[[end]]]
-- [[[cog type_alias_with_json('Foobar2', type_info=dict(a=int, b=str)) ]]]


type alias Foobar2 =
    { a : Int
    , b : String
    }


foobar2Decoder : Json.Decode.Decoder Foobar2
foobar2Decoder =
    Json.Decode.Pipeline.decode Foobar2
        |> Json.Decode.Pipeline.required "a" Json.Decode.int
        |> Json.Decode.Pipeline.required "b" Json.Decode.string


foobar2Encoder : Foobar2 -> Json.Encode.Value
foobar2Encoder record =
    Json.Encode.object
        [ ( "a", Json.Encode.int record.a )
        , ( "b", Json.Encode.string record.b )
        ]



-- [[[end]]]
-- [[[cog record('quux', dict(a=1, b=1.5, c="bar", d=ElmLiteral('D'))) ]]]


quux =
    { a = 1
    , b = 1.5
    , c = "bar"
    , d = D
    }



-- [[[end]]]
-- [[[cog
-- enhanced_enum(
--     'EnhancedFoo',
--     dict(
--         G=dict(some_data1=1, some_data2=1.5, display_name="3"),
--         H=dict(some_data1=2, some_data2=2.5, display_name="4"),
--         J=dict(some_data1=3, some_data2=3.5, display_name="5"),
--     ),
-- )
-- ]]]


type EnhancedFoo
    = G
    | H
    | J


enhancedFoo_list =
    [ G, H, J ]


type alias EnhancedFoo_row =
    { some_data1 : Int
    , some_data2 : Float
    , display_name : String
    }


enhancedFoo_data input =
    case input of
        G ->
            EnhancedFoo_row 1 1.5 "3"

        H ->
            EnhancedFoo_row 2 2.5 "4"

        J ->
            EnhancedFoo_row 3 3.5 "5"



-- [[[end]]]
