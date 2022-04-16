"""
scrape_tweets got kinda messy and didn't work so trying with twint here :)
"""
import requests
import twint

## following this blog post: https://pielco11.ovh/posts/twint-osint/
c = twint.Config()
c.Username = "RooTroopNFT"
c.Search = "#RootyRoo"

twint.run.Search(c)
