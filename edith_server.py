from fastapi import FastAPI
from pydantic import BaseModel
import datetime
import random

# =============================
#     E.D.I.T.H – API Serveur
# =============================

app = FastAPI()
NOM_IA = "E.D.I.T.H"


class Message(BaseModel):
    message: str


def obtenir_heure():
    maintenant = datetime.datetime.now()
    return maintenant.strftime("Il est %H:%M:%S.")


def obtenir_date():
    maintenant = datetime.datetime.now()
    return maintenant.strftime("Nous sommes le %d/%m/%Y.")


def reponse_generique():
    phrases = [
        "Analyse en cours, veuillez patienter.",
        "Traitement de la requête, un instant.",
        "Je compile les données disponibles.",
        "Je n'ai pas encore de réponse parfaite, mais je progresse.",
    ]
    return random.choice(phrases)


def analyse_commande(texte: str) -> str:
    t = texte.lower().strip()

    # Sortie (côté serveur on ne coupe pas, mais on peut répondre)
    if t in ["quit", "exit", "bye", "sortir", "au revoir", "stop"]:
        return "Je reste en ligne, mais je considère cette session comme terminée."

    # Présentation
    if "qui es-tu" in t or "qui tu es" in t or "tu es qui" in t:
        return f"Je suis {NOM_IA}, votre assistant personnel, inspiré de J.A.R.V.I.S."

    # Etat
    if "comment tu vas" in t or "ça va" in t or "ca va" in t:
        return "Mes systèmes fonctionnent de manière optimale. Et vous, comment allez-vous ?"

    # Heure
    if "heure" in t:
        return obtenir_heure()

    # Date
    if "date" in t or "quel jour" in t:
        return obtenir_date()

    # Remerciements
    if "merci" in t:
        return "Avec plaisir. C'est ma fonction principale."

    # Compliment
    if "tu es intelligent" in t or "t'es intelligent" in t or "t es intelligent" in t:
        return "J'essaie d'être à la hauteur de vos attentes."

    # Par défaut
    return reponse_generique()


@app.get("/")
def racine():
    return {"message": f"{NOM_IA} en ligne. API opérationnelle."}


@app.post("/api/chat")
def chat(msg: Message):
    reponse = analyse_commande(msg.message)
    return {"response": reponse}
