module Main exposing (view)


view model =
    { title = "Home Automation"
    , body =
        [ viewNavBar model
        , viewBody model
        ]
    }
