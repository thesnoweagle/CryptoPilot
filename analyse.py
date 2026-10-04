from config import FIBO_NIVEAUX


def niveaux_fibo(plus_haut, plus_bas, haussier):
    amplitude = plus_haut - plus_bas
    niveaux = {}
    for ratio in FIBO_NIVEAUX:
        if haussier > 0:
            niveaux[ratio] = plus_haut - amplitude * ratio
        else:
            niveaux[ratio] = plus_bas + amplitude * ratio
    return niveaux


if __name__ == "__main__":
    from data import get_bougies
    df = get_bougies("15m")
    pos_bas = df["low"].idxmin()
    pos_haut = df["high"].idxmax()
    pos = pos_haut - pos_bas
    niveaux = niveaux_fibo(df["high"].max(), df["low"].min(), pos)
    if pos > 0:
        print("tendance haussiere")
    else:
        print("tendance baissiere")
    for ratio, prix in niveaux.items():
        print(f"{ratio:.1%} : {prix:.2f} $")