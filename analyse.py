from config import FIBO_NIVEAUX, INTERVALLES
from config import RSI_PERIODE, SEUILS_SURACHAT, SEUILS_SURVENTE
from data import get_bougies

def detecter_haussier(df):
    haussier = df["high"].idxmax() > df["low"].idxmin()
    return haussier


def niveaux_fibo(plus_haut, plus_bas, haussier):
    amplitude = plus_haut - plus_bas
    niveaux = {}
    for ratio in FIBO_NIVEAUX:
        if haussier:
            niveaux[ratio] = plus_haut - amplitude * ratio
        else:
            niveaux[ratio] = plus_bas + amplitude * ratio
    return niveaux

def situer_prix(prix, niveaux):
    dessus = None
    dessous = None
    for ratio, prix_niveau in niveaux.items():
        if prix_niveau > prix:
            if dessus is None or prix_niveau < dessus[1]:
                dessus = (ratio, prix_niveau)
        else:
            if dessous is None or prix_niveau > dessous[1]:
                dessous = (ratio, prix_niveau)
    return dessus, dessous

def calculer_rsi(df, periode):
    gain = 0
    pertes = 0
    for i in range(len(df) - periode, len(df)):
        var = df["close"].iloc[i] - df["close"].iloc[i-1]
        if var > 0:
            gain += var
        else:
            pertes += var*(-1)
    if pertes != 0:    
        moyenne_gain = gain/periode
        moyenne_pertes = pertes/periode
    else:
        return 100
    rs = moyenne_gain / moyenne_pertes
    rsi = 100 - 100 / (1 + rs)
    return rsi



def analyser(intervalle):  
    per = RSI_PERIODE
    df = get_bougies(intervalle)
    last = df["close"].iloc[-1]
    haut = df["high"].max()
    bas = df["low"].min()
    tend = detecter_haussier(df)
    fibo = niveaux_fibo(haut, bas, tend)
    dessus, dessous = situer_prix(last, fibo)
    rsi = calculer_rsi(df, per)
    return {"prix": last, "haussier": tend, "niveaux": fibo, "dessus": dessus, "dessous": dessous, "rsi": rsi}


if __name__ == "__main__":
    for intervalle in INTERVALLES:
        analyse = analyser(intervalle)
        print(f"=== {intervalle.upper()} ===")
        print(f"Prix actuel : {analyse["prix"]:.2f} $")
        if analyse["rsi"] > SEUILS_SURACHAT:
            print(f"RSI(14) : {analyse["rsi"]:.2f} (SURACHAT)")
        elif analyse["rsi"] < SEUILS_SURVENTE:
            print(f"RSI(14) : {analyse["rsi"]:.2f} (SURVENTE)")
        else:
            print(f"RSI(14) : {analyse["rsi"]:.2f} (NEUTRE)")
        if analyse["haussier"]:
            print("Impulsion haussière")
        else:
            print("Impulsion baissiere")
        if analyse["dessus"] == None:
            print("Position: au-dessus de tous les niveaux")
        elif analyse["dessous"] == None:
            print("Position: en dessous de tout les niveaux")
        else:
            print(f"Position: entre {analyse["dessous"][0]:.1%} ({analyse["dessous"][1]:.2f} $) et {analyse["dessus"][0]:.1%} ({analyse["dessus"][1]:.2f} $)")
        for ratio, prix in analyse["niveaux"].items():
            print(f"{ratio:.1%} : {prix:.2f} $")
        print()