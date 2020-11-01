module Home exposing (..)

import Html exposing (div, text)


type Msg
    = SomeOneClickedSomething


type Model
    = NothingHappend
    | PlaceHolder


init =
    ( NothingHappend, Cmd.none )


view model =
    { title = "Home"
    , body = [ div [] [ text "Home Screen" ], div [] [ text "not much here" ] ]
    }


update msg model =
    ( model, Cmd.none )
