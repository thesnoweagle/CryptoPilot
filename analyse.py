from config import FIBO_NIVEAUX

def niveaux_fibo(plus_haut, plus_bas):
    amplitude = plus_haut - plus_bas
    niveaux = {}
    for ratio in FIBO_NIVEAUX:
        niveaux[ratio] = plus_haut - amplitude * ratio
    return niveaux

if __name__ == "__main__":
    from data import get_bougies
    df = get_bougies("15m")
    niveaux = niveaux_fibo(df["high"].max(), df["low"].min())
    for ratio, prix in niveaux.items():
        print(f"{ratio:.1%} : {prix:.2f} $")