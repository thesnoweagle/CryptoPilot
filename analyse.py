from config import FIBO_NIVEAUX, INTERVALLES
from config import RSI_PERIODE, SEUILS_SURACHAT, SEUILS_SURVENTE
from data import get_bougies


def detecter_haussier(df):
    return df["high"].idxmax() > df["low"].idxmin()


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
    """RSI avec le lissage de Wilder (comme TradingView)."""
    variations = df["close"].diff().dropna()
    gains = variations.clip(lower=0)
    pertes = -variations.clip(upper=0)
    moyenne_gain = gains.ewm(alpha=1 / periode, adjust=False).mean().iloc[-1]
    moyenne_pertes = pertes.ewm(alpha=1 / periode, adjust=False).mean().iloc[-1]
    if moyenne_pertes == 0:
        return 100
    rs = moyenne_gain / moyenne_pertes
    return 100 - 100 / (1 + rs)


def analyser(intervalle):
    df = get_bougies(intervalle)
    prix = df["close"].iloc[-1]
    haussier = detecter_haussier(df)
    niveaux = niveaux_fibo(df["high"].max(), df["low"].min(), haussier)
    dessus, dessous = situer_prix(prix, niveaux)
    rsi = calculer_rsi(df, RSI_PERIODE)
    return {
        "prix": prix,
        "haussier": haussier,
        "niveaux": niveaux,
        "dessus": dessus,
        "dessous": dessous,
        "rsi": rsi,
    }


def etat_rsi(rsi):
    if rsi > SEUILS_SURACHAT:
        return "SURACHAT"
    if rsi < SEUILS_SURVENTE:
        return "SURVENTE"
    return "NEUTRE"


def afficher(intervalle, analyse):
    print(f"=== {intervalle.upper()} ===")
    print(f"Prix actuel : {analyse['prix']:.2f} $")
    print(f"RSI({RSI_PERIODE}) : {analyse['rsi']:.2f} ({etat_rsi(analyse['rsi'])})")
    if analyse["haussier"]:
        print("Impulsion haussière")
    else:
        print("Impulsion baissière")
    dessus, dessous = analyse["dessus"], analyse["dessous"]
    if dessus is None:
        print("Position : au-dessus de tous les niveaux")
    elif dessous is None:
        print("Position : en dessous de tous les niveaux")
    else:
        print(
            f"Position : entre {dessous[0]:.1%} ({dessous[1]:.2f} $) "
            f"et {dessus[0]:.1%} ({dessus[1]:.2f} $)"
        )
    for ratio, prix in analyse["niveaux"].items():
        print(f"{ratio:.1%} : {prix:.2f} $")
    print()


if __name__ == "__main__":
    resultat = {}
    for intervalle in INTERVALLES:
        analyse = analyser(intervalle)
        afficher(intervalle, analyse)
        resultat[intervalle] = "haussiere" if analyse["haussier"] else "baissiere"
    print(resultat)
