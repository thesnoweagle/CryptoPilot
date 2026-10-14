import requests
import pandas as pd
from config import SYMBOL, NB_BOUGIES

def get_bougies(intervalle):
    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": SYMBOL, "interval": intervalle, "limit": NB_BOUGIES + 1}
    reponse = requests.get(url, params=params, timeout=10)
    reponse.raise_for_status()
    colonnes = ["time", "open", "high", "low", "close", "volume"]
    df = pd.DataFrame([b[:6] for b in reponse.json()], columns=colonnes)
    df[colonnes[1:]] = df[colonnes[1:]].astype(float)
    df["time"] = pd.to_datetime(df["time"], unit="ms")
    # La derniere bougie renvoyee par Binance n'est pas cloturee : on l'ecarte
    return df.iloc[:-1].reset_index(drop=True)

def get_historique(intervalle, nb):
    """Recupere nb bougies cloturees en remontant dans le temps (1000 max par requete)."""
    url = "https://api.binance.com/api/v3/klines"
    colonnes = ["time", "open", "high", "low", "close", "volume"]
    bougies = []
    fin = None
    while len(bougies) < nb + 1:
        params = {"symbol": SYMBOL, "interval": intervalle, "limit": 1000}
        if fin is not None:
            params["endTime"] = fin
        reponse = requests.get(url, params=params, timeout=10)
        reponse.raise_for_status()
        lot = reponse.json()
        if not lot:
            break
        bougies = lot + bougies
        fin = lot[0][0] - 1
    bougies = bougies[-(nb + 1):]
    df = pd.DataFrame([b[:6] for b in bougies], columns=colonnes)
    df[colonnes[1:]] = df[colonnes[1:]].astype(float)
    df["time"] = pd.to_datetime(df["time"], unit="ms")
    return df.iloc[:-1].reset_index(drop=True)


if __name__ == "__main__":
    
    df = get_bougies("15m")
    last = df["close"].iloc[-1]
    highest = df["high"].max()
    lowest = df["low"].min()
    print(f"Dernier prix : {last:.2f} $")
    print(f"Plus haut (200 bougies) : {highest:.2f} $")
    print(f"Plus bas (200 bougies) : {lowest:.2f} $")
