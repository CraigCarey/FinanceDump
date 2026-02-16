#!/usr/bin/env bash
set -euo pipefail

curl -L --compressed "https://www.lse.co.uk/profiles/peoplepower1/?page=2" \
	-H "User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0" \
	-H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
	-H "Accept-Language: en-US,en;q=0.9" \
	-H "Accept-Encoding: gzip, deflate, br, zstd" \
	-H "Alt-Used: www.lse.co.uk" \
	-H "Connection: keep-alive" \
	-H "Cookie: share_recentlyviewed=%5B%22VLRM.PL%22%2C%22JEMA.L%22%2C%22AIC.L%22%2C%22AAVC.L%22%2C%22AADV.L%22%5D; remember_me_code=ba691b45-5334-11f0-b599-fa163ed08d9c; consentUUID=54f2d11b-d11c-439c-b95e-12e3379d6490_46_48; consentUUID=54f2d11b-d11c-439c-b95e-12e3379d6490_46_48_49_52; consentDate=2026-01-30T09:01:15.790Z; rns_is_private_investor=true; _awl=3.1764196384.5-8cf72d54921c0a852dc509cced66ea34-6763652d6575726f70652d7765737431-0; _sharedID=5e954d67-3cae-4f24-bda5-afe9e5844bff; _sharedID_cst=MSzKLLAsgA%3D%3D; quickpicks_dropdown=OPEN; quickpicks_preference=PERCENTAGE; PHPSESSID=93ec34de37343400e83b1b58f8d1af11; ad_block=Y; session_key=c4a24f985f673c6c41fc59dbd7e498e5" \
	-H "Upgrade-Insecure-Requests: 1" \
	-H "Sec-Fetch-Dest: document" \
	-H "Sec-Fetch-Mode: navigate" \
	-H "Sec-Fetch-Site: none" \
	-H "Priority: u=0, i" \
	-H "TE: trailers" \
	-o "2.html"
