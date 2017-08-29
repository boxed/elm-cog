# elm-cog

Code generation for Elm, using Ned Batchelder's Cog. This is useful for two main scenarios:

- keeping data from your python server side code in sync with the Elm side
- enhancing Elm in certain areas where you might otherwise end up with error prone copy paste mess

Features:

- Lists 
  - Example: (`list_of('a, b, c')` or `list_of('a', 'b', 'c')`)
- Union types 
  - Example: (`union('A, B, C')`)
- Enums (A union type + a list that are always in sync) 
  - Example: (`enum('A, B, C')`)
- Type alias 
  - Example: (`type_alias('FooBar', type_info=dict(a=int, b=float, c=str))`
- Record 
  - Example: (`record('foo', dict(a=1, b=1.5, c="bar"))`)
- Enhanced enums: an enum with an associated Dict for extra data 
  - Example: (`enhanced_enum('FooBar', dict(A=dict(some_data1=1, some_data2=1.5, display_name="3"), B=dict(some_data1=2, some_data2=2.5, display_name="4"),)`)
- Record alias with generated encoders and decoders (like `enhanced_enum` but you call `type_alias_with_json`)


## Usage

1. Install my fork of Cog: 

```shell
hg clone https://bitbucket.org/boxed/cog
cd cog
python3 setup.py install
```

(I have sent a pull request for the feature I need, hopefully you can at some point use standard Cog)

2. Copy `elm.py` and `elm-cog` to your source tree.  

3. Run `elm-cog` to do the actual code generation.

I know it's a bit clunky right now, but this tool is still in a prototype stage. Let me know if you find it useful!

## Full example of code generation

You write this in your elm code:

```elm
-- [[[cog type_alias_with_json('Foobar2', type_info=dict(a=int, b=str, c='CustomType')) ]]]
-- [[[end]]]
```

then run `elm-cog` and it will update your file in place to replace the above with:

```elm
-- [[[cog type_alias_with_json('Foobar2', type_info=dict(a=int, b=str, c='CustomType')) ]]]


type alias Foobar2 =
    { a : Int
    , b : String
    , c : CustomType
    }


foobar2Decoder : Json.Decode.Decoder Foobar2
foobar2Decoder =
    Json.Decode.Pipeline.decode Foobar2
        |> Json.Decode.Pipeline.required "a" Json.Decode.int
        |> Json.Decode.Pipeline.required "b" Json.Decode.string
        |> Json.Decode.Pipeline.required "c" customTypeDecoder


foobar2Encoder : Foobar2 -> Json.Encode.Value
foobar2Encoder record =
    Json.Encode.object
        [ ( "a", Json.Encode.int record.a )
        , ( "b", Json.Encode.string record.b )
        , ( "c", customTypeEncoder record.c )
        ]



-- [[[end]]]

```

The output is formatted accordning to `elm-format` already, so no need to run it after.
