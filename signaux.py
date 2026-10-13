from analyse import analyser
from config import INTERVALLES, SEUILS_SURACHAT, SEUILS_SURVENTE, TOLERANCE_FIBO


def generer_signal(analyse):
    dessus, dessous = analyse["dessus"], analyse["dessous"]
    prix = analyse["prix"]
    tendance = analyse["haussier"]
    rsi = analyse["rsi"]

    # Distance (en fraction du prix) jusqu'aux niveaux voisins.
    # Si un niveau n'existe pas, on met l'infini : il ne sera jamais "proche".
    calc1 = float("inf")
    calc2 = float("inf")
    if dessus is not None:
        calc1 = (dessus[1] - prix) / prix
    if dessous is not None:
        calc2 = (prix - dessous[1]) / prix

    proche = calc1 < TOLERANCE_FIBO or calc2 < TOLERANCE_FIBO

    if proche and tendance and rsi < SEUILS_SURVENTE:
        return "ACHAT"
    elif proche and not tendance and rsi > SEUILS_SURACHAT:
        return "VENTE"
    else:
        return "ATTENDRE"


if __name__ == "__main__":
    for intervalle in INTERVALLES:
        print(intervalle, generer_signal(analyser(intervalle)))
