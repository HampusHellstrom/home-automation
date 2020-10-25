module Routing exposing (..)

import Url
import Url.Parser as UP exposing ((</>), (<?>), Parser, int, map, oneOf, parse, s, string)
import Url.Parser.Query as Query


type Route
    = Home
    | Sensor DateQuery
    | SensorGroup DateQuery
    | View


routeParser : Parser (Route -> a) a
routeParser =
    UP.oneOf
        [ map SensorGroup (s "login" </> int <?> Query.string "dateFrom" <?> Query.string "dateTo")
        , map Sensor (s "sensor" </> int "item_id" <?> queryParser)
        , map View (s "view")
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


queryParser : Parser DateQuery
queryParser =
    Query.map2 DateQuery (string "dateFrom") (int "dateTo")
