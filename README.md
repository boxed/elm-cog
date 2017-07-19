# elm-cog

Code generation for Elm, using Ned Batchelder's Cog. This is useful for two main scenarios:

- keeping data from your python server side code in sync with the Elm side
- enhancing Elm in certain areas where you might otherwise end up with error prone copy paste mess

Features:

- Lists
- Union types
- Enums (A union type + a list that are always in sync)
- Record alias
- Record
- Enhanced enums: an enum with an associated Dict for extra data
