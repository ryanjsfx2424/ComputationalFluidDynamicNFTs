import requests


url = "https://opensea.io/__api/graphql/"

headers = {
"authority": "opensea.io",
"scheme":"https",
"accept":"*/*",
"accept-encoding":"gzip, deflate, br",
"accept-language":"en-GB,en-US;q=0.9,en;q=0.8",
"cookie": "ajs_anonymous_id=5c0de0f0-ac0e-40d9-bf4c-a4e2c80751f3; assets_card_variant=%22compact%22; ajs_user_id=0xc7d7cc95ded3b8c81f17af0e65def2d4abb366f7; amp_d28823=DXqmYjf1kTRYsjd2F6x-N4.MHhjN2Q3Y2M5NWRlZDNiOGM4MWYxN2FmMGU2NWRlZjJkNGFiYjM2NmY3..1g4hju5je.1g4hk08qb.1m.5.1r; __os_session=eyJpZCI6ImIxNDU4NWQxLWQxOGMtNGIzYy05MGU1LTQ1MmJjODE1YzI0OSJ9; __os_session.sig=rPocGX0vTwJ2-zGzqVA0Kj_KOxg_NYq0zuy7CP4t_8A; ajs_user_id=0xc7d7cc95ded3b8c81f17af0e65def2d4abb366f7; ajs_anonymous_id=5c0de0f0-ac0e-40d9-bf4c-a4e2c80751f3; wallet={%22accounts%22:[{%22walletName%22:%22MetaMask%22%2C%22address%22:%220xc7d7cc95ded3b8c81f17af0e65def2d4abb366f7%22%2C%22imageUrl%22:%22https://lh3.googleusercontent.com/8onaIBBV1Mna8xwCvo02nezcWvYfmddqcndn_CXRrYArYw5wJ4HlMcC5wlRstaAfuJVAPal4M2IWrDOu7eZHSvFFdHkzWNjKeHdxQqU=s100%22%2C%22nickname%22:null%2C%22relayId%22:%22QWNjb3VudFR5cGU6NDM5NzgyNDQz%22%2C%22isCompromised%22:false%2C%22isStaff%22:false%2C%22user%22:{%22relayId%22:%22VXNlclR5cGU6MzQyODQxMTc=%22%2C%22username%22:%22knightscastlewtf%22%2C%22publicUsername%22:%22knightscastlewtf%22%2C%22hasAffirmativelyAcceptedOpenseaTerms%22:false%2C%22email%22:null}%2C%22metadata%22:{%22isBanned%22:false}}]%2C%22activeAccount%22:{%22walletName%22:%22MetaMask%22%2C%22address%22:%220xc7d7cc95ded3b8c81f17af0e65def2d4abb366f7%22%2C%22imageUrl%22:%22https://lh3.googleusercontent.com/8onaIBBV1Mna8xwCvo02nezcWvYfmddqcndn_CXRrYArYw5wJ4HlMcC5wlRstaAfuJVAPal4M2IWrDOu7eZHSvFFdHkzWNjKeHdxQqU=s100%22%2C%22nickname%22:null%2C%22relayId%22:%22QWNjb3VudFR5cGU6NDM5NzgyNDQz%22%2C%22isCompromised%22:false%2C%22isStaff%22:false%2C%22user%22:{%22relayId%22:%22VXNlclR5cGU6MzQyODQxMTc=%22%2C%22username%22:%22knightscastlewtf%22%2C%22publicUsername%22:%22knightscastlewtf%22%2C%22hasAffirmativelyAcceptedOpenseaTerms%22:false%2C%22email%22:null}%2C%22metadata%22:{%22isBanned%22:false}}}; opensea_logged_out=true; SFaSaPpU=AwVcXwaCAQAAbpotLwtUxsgIeO_glEtarRWIdLSj-Xhod0xo2Fj7R4DBjsDHAYK3WLCuci7ywH9eCOfvosJeCA|1|0|75747616999002f0a7aaeea3ddc90ec4e6844bd0; amp_ddd6ec=KPwN6rwiXta3sVgOJFDbk9.MHhjN2Q3Y2M5NWRlZDNiOGM4MWYxN2FmMGU2NWRlZjJkNGFiYjM2NmY3..1g835upgv.1g838mq94.1ng.11.1oh; sessionid=eyJzZXNzaW9uSWQiOiJiMTQ1ODVkMS1kMThjLTRiM2MtOTBlNS00NTJiYzgxNWMyNDkifQ:1oCf04:Yj2dxbJR7XmuY6ADc8QJ8rG00J2CzrMGRUjE5SuG09s; csrftoken=wef3er3KNP93miN6dAzOb0PvIdu98OZGkc9zE47I6kFQuLlavUPR1IEL9B8Jufm0; __cf_bm=mcm9llmmPKUBObp4_.9XfN46HYgdDovXZ28Io_Gxq1o-1657968339-0-AYjAO3fOfBSVJUexipMzMxjdMynhlG93mlRVepvDCB5IGwRvWph6NszaaKUP9wbwCVk2uU+w+nvN+yb04irP0r4=; _dd_s=rum=0&expire=1657969231761",
"referer":"https://opensea.io/",
"sec-fetch-dest": "empty",
"sec-fetch-mode": "cors",
"sec-fetch-site": "same-origin",
"sec-gpc": "1",
"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36"}

headers = {
"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36",
"Authority": "opensea.io"
}

query = "limit:100"

resp = requests.post(url, headers=headers, json={"query":query})
print("resp: ", resp)
print("resp.text: ", resp.text)
