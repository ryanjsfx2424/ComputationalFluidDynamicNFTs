curl -X GET -H "Authorization: Bearer $APP_ACCESS_TOKEN" "https://api.twitter.com/2/tweets/search/stream?tweet.fields=created_at&expansions=author_id&user.fields=created_at"
