#! /usr/bin/env bash

curl -X POST \
     -H "Content-Type: application/json" \
     -d '[
           {
             "idType": "ID_SEDOL",
             "idValue": "0263494"
           }
         ]' \
     https://api.openfigi.com/v3/mapping \
     | jq > "0263494.json"
