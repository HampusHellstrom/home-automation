module Main exposing (..)

import Browser
import Browser.Navigation as Nav
import Home
import Html exposing (Html, a, div, nav, table, td, text, th, tr)
import Html.Attributes exposing (href)
import Html.Events exposing (onClick)
import Http
import Json.Decode as JD exposing (Decoder, field, int, list, map5, string)
import Login
import Routing exposing (Route(..), urlParse)
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
    { page : CurrentPage
    , key : Nav.Key
    }


type CurrentPage
    = LoginPage Login.Model
    | HomePage Home.Model


type alias User =
    { token : String
    }


init : () -> Url.Url -> Nav.Key -> ( Model, Cmd Msg )
init flags url key =
    ( { page = HomePage Home.NothingHappend, key = key }
    , Cmd.none
    )



-- UPDATE


type Msg
    = LinkClicked Browser.UrlRequest
    | UrlChanged Url.Url
    | GotLoginMsg Login.Msg
    | GotHomeMsg Home.Msg


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case ( msg, model.page ) of
        ( LinkClicked urlRequest, _ ) ->
            case urlRequest of
                Browser.Internal url ->
                    ( model, Nav.pushUrl model.key (Url.toString url) )

                Browser.External href ->
                    ( model, Nav.load href )

        ( UrlChanged url, _ ) ->
            changePageTo model (urlParse url)

        ( GotHomeMsg subMsg, HomePage subModel ) ->
            Home.update subMsg subModel
                |> updateModelWith model HomePage GotHomeMsg

        ( GotLoginMsg subMsg, LoginPage subModel ) ->
            Login.update subMsg subModel
                |> updateModelWith model LoginPage GotLoginMsg

        ( _, _ ) ->
            ( model, Cmd.none )


updateModelWith model toPage toMsg ( subModel, subCmd ) =
    ( { model | page = toPage subModel }, Cmd.map toMsg subCmd )



--changePageTo : Model -> Route -> ( Model, Cmd Msg )


changePageTo model newPage =
    case newPage of
        Home ->
            updateModelWith model HomePage GotHomeMsg Home.init

        Login ->
            updateModelWith model LoginPage GotLoginMsg Login.init



-- VIEW


view : Model -> Browser.Document Msg
view model =
    let
        { title, body } =
            viewContent model
    in
    { title = "Home Automation - " ++ title
    , body = [ viewNavBar model ] ++ body
    }


viewNavBar : Model -> Html Msg
viewNavBar model =
    nav []
        [ a [ href "/" ] [ text "Home" ]
        , a [ href "/login" ] [ text "Login" ]
        ]


viewContent : Model -> Browser.Document Msg
viewContent model =
    let
        viewPage toMsg config =
            let
                { title, body } =
                    config
            in
            { title = title
            , body = List.map (Html.map toMsg) body
            }
    in
    case model.page of
        LoginPage subModel ->
            viewPage GotLoginMsg (Login.view subModel)

        HomePage subModel ->
            viewPage GotHomeMsg (Home.view subModel)



--SUBSCRIPTIONS


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.none
