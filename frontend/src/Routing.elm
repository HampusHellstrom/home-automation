module Routing exposing (..)

import Url
import Url.Parser as UP exposing ((</>), (<?>), Parser, int, map, oneOf, parse, s, string)
import Url.Parser.Query as Query


type Route
    = Login
    | Home


routeParser : Parser (Route -> a) a
routeParser =
    UP.oneOf
        [ map Login (s "login")

        --, map Sensor (s "sensor" </> int "item_id" <?> queryParser)
        --, map View (s "view")
        ]


urlParse : Url.Url -> Route
urlParse url =
    case parse routeParser url of
        Just route ->
            route

        Nothing ->
            Home


type alias DateQuery =
    { dateFrom : Maybe Int
    , dateTo : Maybe Int
    }



--queryParser : Query.Parser DateQuery
--queryParser =
--    Query.map2 DateQuery (string "dateFrom") (int "dateTo")
