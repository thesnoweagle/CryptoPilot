from config import FIBO_NIVEAUX, INTERVALLES
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


def analyser(intervalle):  
    df = get_bougies(intervalle)
    last = df["close"].iloc[-1]
    haut = df["high"].max()
    bas = df["low"].min()
    tend = detecter_haussier(df)
    fibo = niveaux_fibo(haut, bas, tend)
    dessus, dessous = situer_prix(last, fibo)
    return {"prix": last, "haussier": tend, "niveaux": fibo, "dessus": dessus, "dessous": dessous}


if __name__ == "__main__":
    for intervalle in INTERVALLES:
        analyse = analyser(intervalle)
        print(f"=== {intervalle.upper()} ===")
        print(f"Prix actuel : {analyse["prix"]:.2f} $")
        if analyse["haussier"]:
            print("Impulsion haussière")
        else:
            print("Impulsion baissiere")
        if analyse["dessus"] == None:
            print("Position: au-dessus de tous les niveaux")
        elif analyse["dessous"] == None:
            print("Position: en dessous de tout les niveaux")
        else:
            print(f"Position: entre {analyse["dessous"][0]:.1%} ({analyse["dessous"][1]:.2f}) et {analyse["dessus"][0]:.1%} ({analyse["dessus"][1]:.2f})")
        for ratio, prix in analyse["niveaux"].items():
            print(f"{ratio:.1%} : {prix:.2f} $")
        print()