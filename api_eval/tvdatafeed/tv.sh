#! /usr/bin/env bash

set -eux

# Search for a stock by symbol / name - returns json
# curl 'https://symbol-search.tradingview.com/symbol_search/v3/?text=GAZP&search_type=stocks' \
#     --compressed \
#     -H 'Origin: https://www.tradingview.com' \
#     | jq

# price (lp: 132.84) isin over websocket
# wss://data.tradingview.com/socket.io/websocket?from=symbols%2FRUS-GAZP%2F&date=2024_10_25-15_29
# ~m~5748~m~{
#     "m": "qsd",
#     "p": [
#         "qs_bneYvnhccjby",
#         {
#             "n": "={\"session\":\"extended\",\"symbol\":\"RUS:GAZP\"}",
#             "s": "ok",
#             "v": {
#                 "lp_time": 1729889100,
#                 "regular_close_time": 1729889100,
#                 "earnings_release_next_date": 1732536000,
#                 "beta_1_year": 0.51075876,
#                 "first_bar_time_1d": 1137974400,
#                 "open_price": 134.15,
#                 "volume": 54791420,
#                 "source2": {
#                     "country": "RU",
#                     "description": "Russian Exchange",
#                     "exchange-type": "exchange",
#                     "id": "RUS",
#                     "name": "Russian Exchange",
#                     "url": "www.moex.com"
#                 },
#                 "pro_name": "RUS:GAZP",
#                 "allowed_adjustment": "any",
#                 "pricescale": 100,
#                 "rates_mc": {
#                     "time": 1729987200,
#                     "to_aud": 0.015591,
#                     "to_cad": 0.014342,
#                     "to_chf": 0.008971,
#                     "to_cny": 0.073707,
#                     "to_eur": 0.009559,
#                     "to_gbp": 0.00798,
#                     "to_jpy": 1.572948,
#                     "to_market": 1,
#                     "to_symbol": 1,
#                     "to_usd": 0.01035
#                 },
#                 "isin": "RU0007661625",
#                 "subsession_id": "extended",
#                 "rates_fy": {
#                     "time": 1703980800,
#                     "to_aud": 0.016377,
#                     "to_cad": 0.014777,
#                     "to_chf": 0.009387,
#                     "to_cny": 0.079155,
#                     "to_eur": 0.010101,
#                     "to_gbp": 0.008758,
#                     "to_jpy": 1.573162,
#                     "to_market": 1,
#                     "to_symbol": 1,
#                     "to_usd": 0.011149
#                 },
#                 "minmov": 1,
#                 "ch": -1.35,
#                 "rchp": null,
#                 "symbol-primaryname": "RUS:GAZP",
#                 "first_bar_time_1s": 1660719594,
#                 "local_description": "\"ÐÐ°Ð·Ð¿ÑÐ¾Ð¼\" (ÐÐÐ) - Ð¾Ð±ÑÐºÐ½.",
#                 "logoid": "gazprom",
#                 "typespecs": [
#                     "common"
#                 ],
#                 "rtc": null,
#                 "minmove2": 0,
#                 "short_description": "Gazprom",
#                 "low_price": 132.0,
#                 "all_time_low": 84,
#                 "variable_tick_size": "0.01",
#                 "rtc_time": null,
#                 "short_name": "GAZP",
#                 "provider_id": "moex",
#                 "is_tradable": true,
#                 "earnings_release_date": 1725364800,
#                 "all_time_high_day": 1633478400,
#                 "currency_id": "RUB",
#                 "hub_rt_loaded": true,
#                 "subsessions": [
#                     {
#                         "description": "Regular Trading Hours",
#                         "id": "regular",
#                         "private": false,
#                         "session": "0700-2350",
#                         "session-correction": "0700-2350:20240427,20241102,20241228;1000-2350:20210220;dayoff:20220228,20220301,20220302,20220303,20220304,20220309,20220310,20220311,20220314,20220315,20220316,20220317,20220318",
#                         "session-display": "0700-2350"
#                     },
#                     {
#                         "description": "Extended Trading Hours",
#                         "id": "extended",
#                         "private": false,
#                         "session": "0600-2350",
#                         "session-correction": "0600-2350:20240427,20241102,20241228;0900-2350:20210220;dayoff:20220228,20220301,20220302,20220303,20220304,20220309,20220310,20220311,20220314,20220315,20220316,20220317,20220318",
#                         "session-display": "0600-2350"
#                     },
#                     {
#                         "description": "Premarket",
#                         "id": "premarket",
#                         "private": true,
#                         "session": "0600-0700",
#                         "session-correction": "0600-0700:20240427,20241102,20241228;0900-1000:20210220;dayoff:20220228,20220301,20220302,20220303,20220304,20220309,20220310,20220311,20220314,20220315,20220316,20220317,20220318",
#                         "session-display": "0600-0700"
#                     }
#                 ],
#                 "first_bar_time_1m": 1373263200,
#                 "source-logoid": "source/RUS",
#                 "session_holidays": "20010101,20010102,20010108,20010308,20010309,20010501,20010502,20010509,20010611,20010612,20011107,20011212,20020101,20020102,20020107,20020225,20020308,20020501,20020502,20020503,20020509,20020510,20020612,20021107,20021108,20021212,20021213,20030101,20030102,20030103,20030106,20030107,20030224,20030310,20030501,20030502,20030509,20030612,20030613,20031107,20031212,20040101,20040102,20040107,20040223,20040308,20040503,20040504,20040510,20040614,20041108,20041213,20050103,20050104,20050105,20050106,20050107,20050110,20050223,20050307,20050308,20050502,20050509,20050510,20050613,20051104,20060102,20060103,20060104,20060105,20060106,20060109,20060223,20060224,20060308,20060501,20060508,20060509,20060612,20061106,20070101,20070102,20070103,20070104,20070107,20070108,20070225,20070308,20070501,20070509,20070611,20070612,20071105,20080101,20080102,20080103,20080104,20080107,20080108,20080225,20080310,20080501,20080502,20080509,20080612,20080613,20081103,20081104,20090101,20090102,20090105,20090106,20090107,20090108,20090109,20090223,20090309,20090501,20090511,20090612,20091104,20100101,20100104,20100105,20100106,20100107,20100108,20100222,20100223,20100308,20100503,20100510,20100614,20101104,20101105,20110103,20110104,20110105,20110106,20110107,20110223,20110307,20110308,20110502,20110509,20110613,20111104,20120102,20120223,20120308,20120309,20120430,20120501,20120509,20120611,20120612,20121105,20121231,20130101,20130102,20130103,20130104,20130105,20130107,20130308,20130501,20130509,20130612,20131104,20131231,20140101,20140102,20140103,20140107,20140310,20140501,20140509,20140612,20141104,20141231,20150101,20150102,20150107,20150223,20150309,20150501,20150504,20150511,20150612,20151104,20151231,20160101,20160107,20160108,20160223,20160308,20160502,20160503,20160509,20160613,20161104,20170102,20170223,20170308,20170501,20170508,20170509,20170612,20171106,20180101,20180102,20180108,20180223,20180308,20180501,20180509,20180612,20181105,20181231,20190101,20190102,20190107,20190308,20190501,20190509,20190612,20191104,20191231,20200101,20200102,20200107,20200224,20200309,20200501,20200511,20200612,20200624,20200701,20201104,20201231,20210101,20210107,20210223,20210308,20210503,20211104,20211231,20220107,20220223,20220305,20220307,20220308,20220502,20220509,20220613,20221104,20230102,20230223,20230308,20230501,20230509,20230612,20240101,20240102,20240107,20240223,20240308,20240501,20240509,20240612,20241104",
#                 "pro_perm": "moex",
#                 "current_session": "out_of_session",
#                 "base_name": [
#                     "RUS_DLY:GAZP"
#                 ],
#                 "visible-plots-set": "ohlcv",
#                 "high_price": 136.5,
#                 "all_time_high": 397.64,
#                 "lp": 132.84,
#                 "market_cap_basic": 3148577215700,
#                 "timezone": "Europe/Moscow",
#                 "isin-displayed": "RU0007661625",
#                 "listed_exchange": "RUS",
#                 "all_time_low_day": 1224806400,
#                 "days_to_maturity": null,
#                 "currency_code": "RUB",
#                 "language": "ru",
#                 "update_mode": "delayed_streaming_900",
#                 "country_code": "RU",
#                 "prev_close_price": 134.19,
#                 "fundamental_currency_code": "RUB",
#                 "fractional": false,
#                 "regular_close": 132.84,
#                 "open_time": 1729814400,
#                 "measure": "price",
#                 "type": "stock",
#                 "chp": -1.01,
#                 "broker_names": {
#                     "alor": "GAZP"
#                 },
#                 "exchange": "RUS",
#                 "trading-by": "last",
#                 "pointvalue": 1,
#                 "rch": null,
#                 "description": "Gazprom",
#                 "average_volume": 41146721,
#                 "source_id": "RUS",
#                 "original_name": "RUS_DLY:GAZP"
#             }
#         }
#     ]
# }