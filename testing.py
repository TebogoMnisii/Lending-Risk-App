from tiingo import TiingoClient
import pandas as pd

config = {
    'session': True,
    'api_key': '272e1e82e3f41dcfd3a096fbd5939a024a02ff98'
}
client = TiingoClient(config)

# Download daily GLD data
df = client.get_dataframe("GLD",
                          frequency="daily",
                          startDate="2023-01-01",
                          endDate="2024-01-01")
print(df.head())
