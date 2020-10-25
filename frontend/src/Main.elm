module Main exposing (..)

import Browser
import Browser.Navigation as Nav
import Html exposing (Html, a, div, nav, table, td, text, th, tr)
import Html.Events exposing (onClick)
import Http
import Json.Decode as JD exposing (Decoder, field, int, list, map5, string)
import Routing exposing (Route, urlParse)
import Url




-- MAIN


main =
    Browser.application
        { init = init
        , update = update
        , subscriptions = subscriptions
        , view = view
        , onUrlChange = UrlChanged
        , onUrlRequest = LinkClicked
        }



-- MODEL


type alias Model =
    { user :  Maybe User
    , route : Route
    , url : Url.Url
    , key : Nav.Key
    }

type alias user =
    { token : String
    , defaultView : String
    }


-- UPDATE


type Msg
    = LoadingData
    | GotData (Result Http.Error (List Player))
    | SortData Column
    | LinkClicked Browser.UrlRequest
    | UrlChanged Url.Url


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    (model , Cmd.none)

-- VIEW


view : Model -> Browser.Document Msg
view model =
    { title = "A title"
    , body =
        [ div []
            [ navBar model
            , contentDisplay model
            ]
        ]
    }



-- SUBSCRIPTIONS


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.none
