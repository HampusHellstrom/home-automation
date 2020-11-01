module Login exposing (..)

import Html exposing (Html, button, div, form, input, text)
import Html.Attributes exposing (placeholder, type_, value)
import Html.Events exposing (onClick, onInput, onSubmit)


type alias Model =
    { username : String
    , password : String
    }


type Msg
    = GotUsername String
    | GotPassword String
    | SubmittedCredentials
    | SuccessfulLogin


init =
    ( { username = ""
      , password = ""
      }
    , Cmd.none
    )


view : Model -> { title : String, body : List (Html Msg) }
view model =
    { title = "Login"
    , body =
        [ viewInputField "username" "Username" model.username GotUsername
        , viewInputField "password" "Password" model.password GotPassword
        , button [ onClick SubmittedCredentials ] [ text "Login" ]
        ]
    }


viewInputField : String -> String -> String -> (String -> Msg) -> Html Msg
viewInputField t p v toMsg =
    input [ type_ t, placeholder p, value v, onInput toMsg ] []


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        GotPassword str ->
            ( { model | password = str }, Cmd.none )

        GotUsername str ->
            ( { model | username = str }, Cmd.none )

        SubmittedCredentials ->
            ( model, Cmd.none )

        SuccessfulLogin ->
            ( model, Cmd.none )
