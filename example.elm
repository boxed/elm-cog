-- [[[cog import elm; elm.enum('Foo', 'A, B, C') ]]]


type Foo
    = A
    | B
    | C


foo_list =
    [ A
    , B
    , C
    ]



-- [[[end]]]

-- [[[cog import elm; elm.list('foo', 'A, B, C') ]]]
-- [[[end]]]

-- [[[cog import elm; elm.record_alias('foo', 'a : Int, b: String') ]]]
-- [[[end]]]