module Login exposing (..)

import Html exposing (Html, button, div, form, input, text)
import Html.Attributes exposing (placeholder, type_, value)
import Html.Events exposing (onClick, onInput, onSubmit)


type alias Model =
    { username : String
    , password : String
    , state : LoginState
    }


type LoginState
    = NotLoggedIn
    | Pending
    | Failed
    | Successful


type Msg
    = GotUsername String
    | GotPassword String
    | SubmittedCredentials
    | SuccessfulLogin


init =
    ( { username = ""
      , password = ""
      , state = NotLoggedIn
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
        , showState model.state
        ]
    }


showState state =
    case state of
        Pending ->
            text "login pending"

        _ ->
            text ""


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
            ( { model | state = Pending }, Cmd.none )

        SuccessfulLogin ->
            ( model, Cmd.none )
