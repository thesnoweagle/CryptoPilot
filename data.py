import requests
import pandas as pd
from config import SYMBOL, NB_BOUGIES

def get_bougies(intervalle):
    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": SYMBOL, "interval": intervalle, "limit": NB_BOUGIES}
    reponse = requests.get(url, params=params, timeout=10)
    reponse.raise_for_status()
    colonnes = ["time", "open", "high", "low", "close", "volume"]
    df = pd.DataFrame([b[:6] for b in reponse.json()], columns=colonnes)
    df[colonnes[1:]] = df[colonnes[1:]].astype(float)
    df["time"] = pd.to_datetime(df["time"], unit="ms")
    return df

if __name__ == "__main__":
    
    df = get_bougies("15m")
    last = df["close"].iloc[-1]
    highest = df["high"].max()
    lowest = df["low"].min()
    print(f"Dernier prix : {last:.2f} $")
    print(f"Plus haut (200 bougies) : {highest:.2f} $")
    print(f"Plus bas (200 bougies) : {lowest:.2f} $")
    