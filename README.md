# elm-cog

Code generation for Elm, using Ned Batchelder's Cog. This is useful for two main scenarios:

- keeping data from your python server side code in sync with the Elm side
- enhancing Elm in certain areas where you might otherwise end up with error prone copy paste mess

Features:

- Lists (`list_of('a, b, c')` or `list_of('a', 'b', 'c')`)
- Union types (`union('A, B, C')`)
- Enums (A union type + a list that are always in sync) (`enum('A, B, C')`)
- Type alias (`type_alias('FooBar', type_info=dict(a=int, b=float, c=str))`
- Record (`record('foo', dict(a=1, b=1.5, c="bar"))`)
- Enhanced enums: an enum with an associated Dict for extra data (`enhanced_enum('FooBar', dict(A=dict(some_data1=1, some_data2=1.5, display_name="3"), B=dict(some_data1=2, some_data2=2.5, display_name="4"),)`)
- Record alias with generated encoders and decoders (like `enhanced_enum` but you call `type_alias_with_json`)


## Usage

1. Install my fork of Cog: 

```shell
hg clone https://bitbucket.org/boxed/cog
cd cog
python setup.py install
```

(I have sent a pull request for the feature I need, hopefully you can at some point use standard Cog)

2. Copy `elm.py` and `elm-cog` to your source tree.  

3. Run `elm-cog` to do the actual code generation.

I know it's a bit clunky right now, but this tool is still in a prototype stage. Let me know if you find it useful!
