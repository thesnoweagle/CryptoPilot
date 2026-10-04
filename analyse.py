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



def analyser(intervalle):  
    df = get_bougies(intervalle)
    last = df["close"].iloc[-1]
    haut = df["high"].max()
    bas = df["low"].min()
    tend = detecter_haussier(df)
    fibo = niveaux_fibo(haut, bas, tend)
    return {"prix": last, "haussier": tend, "niveaux": fibo}


if __name__ == "__main__":
    for intervalle in INTERVALLES:
        analyse = analyser(intervalle)
        print(f"=== {intervalle.upper()} ===")
        print(f"Prix actuel : {analyse["prix"]:.2f} $")
        if analyse["haussier"]:
            print("Impulsion haussière")
        else:
            print("Impulsion baissiere")
        for ratio, prix in analyse["niveaux"].items():
            print(f"{ratio:.1%} : {prix:.2f} $")
        print()