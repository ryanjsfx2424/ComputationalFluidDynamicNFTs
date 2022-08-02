import pandas as pd

scraper = pd.read_html("https://opensea.io/collection/roo-troop/activity")

print(scraper)
