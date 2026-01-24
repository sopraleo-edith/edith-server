from fastapi.responses import FileResponse
from pydantic import BaseModel
import datetime
import random
import importlib
import types
from pathlib import Path

# =============================
#     E.D.I.T.H – API Serveur
# =============================

app = FastAPI()
NOM_IA = "E.D.I.T.H"

SKILLS_FILE = Path(__file__).parent / "skills.py"
SKILLS_MODULE_NAME = "skills"
skills_module: types.ModuleType | None = None


class Message(BaseModel):
    message: str


class AddSkillRequest(BaseModel):
    name: str      # nom de la fonction
    code: str      # code Python complet de la fonction


class DeleteSkillRequest(BaseModel):
    name: str      # nom de la fonction à supprimer


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


# =============================
#     Gestion des skills dynamiques
# =============================

def charger_skills():
    global skills_module
    try:
        if SKILLS_MODULE_NAME in globals():
            skills_module = importlib.reload(importlib.import_module(SKILLS_MODULE_NAME))
        else:
            skills_module = importlib.import_module(SKILLS_MODULE_NAME)
    except ModuleNotFoundError:
        # Si le fichier n'existe pas encore, on le crée minimal
        if not SKILLS_FILE.exists():
            SKILLS_FILE.write_text(
                '# Fichier des skills dynamiques pour E.D.I.T.H\n\n',
                encoding="utf-8",
            )
        skills_module = importlib.import_module(SKILLS_MODULE_NAME)


def lister_skills() -> list[str]:
    if skills_module is None:
        return []
    noms = []
    for attr in dir(skills_module):
        if attr.startswith("_"):
            continue
        obj = getattr(skills_module, attr)
        if callable(obj):
            noms.append(attr)
    return noms


def executer_skill(nom: str) -> str:
    if skills_module is None:
        return "Aucune skill chargée pour le moment."
    if not hasattr(skills_module, nom):
        return f"La skill '{nom}' n'existe pas."
    func = getattr(skills_module, nom)
    try:
        result = func()
        return str(result)
    except Exception as e:
        return f"Erreur lors de l'exécution de la skill '{nom}': {e}"


def ajouter_skill_dans_fichier(name: str, code: str):
    """
    Ajoute le code d'une nouvelle skill dans skills.py
    """
    if not SKILLS_FILE.exists():
        SKILLS_FILE.write_text(
            '# Fichier des skills dynamiques pour E.D.I.T.H\n\n',
            encoding="utf-8",
        )

    contenu = SKILLS_FILE.read_text(encoding="utf-8")

    # Sécurité minimale : on évite d'écraser une fonction existante
    if f"def {name}(" in contenu:
        raise ValueError(f"Une skill nommée '{name}' existe déjà.")

    # On ajoute un saut de ligne + le code fourni
    with SKILLS_FILE.open("a", encoding="utf-8") as f:
        f.write("\n\n")
        f.write(code.strip())
        f.write("\n")

    # On recharge le module
    charger_skills()


def supprimer_skill_du_fichier(name: str):
    """
    Supprime une fonction simple 'def name(...)' de skills.py
    (approche naïve mais suffisante pour commencer)
    """
    if not SKILLS_FILE.exists():
        raise ValueError("Le fichier de skills n'existe pas.")

    lignes = SKILLS_FILE.read_text(encoding="utf-8").splitlines()
    nouveau_contenu = []
    inside_target = False

    for ligne in lignes:
        stripped = ligne.lstrip()
        if stripped.startswith(f"def {name}("):
            inside_target = True
            continue
        if inside_target:
            # On considère qu'une fonction se termine sur une ligne vide
            if stripped == "" or stripped.startswith("def "):
                inside_target = False
                # si nouvelle def, on la garde
                if stripped.startswith("def "):
                    nouveau_contenu.append(ligne)
            # sinon on saute les lignes de la fonction
            continue
        else:
            nouveau_contenu.append(ligne)

    SKILLS_FILE.write_text("\n".join(nouveau_contenu) + "\n", encoding="utf-8")
    charger_skills()


# Charger les skills au démarrage
charger_skills()


# =============================
#     Analyse des commandes
# =============================

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

    # =============================
    #     Partie skills dynamiques
    # =============================

    # Lister les skills
    if "liste des skills" in t or "skills ?" in t or "quelles skills" in t:
        noms = lister_skills()
        if not noms:
            return "Aucune skill n'est encore définie."
        return "Skills disponibles : " + ", ".join(noms)

    # Exécuter une skill : "exécute skill NOM"
    if t.startswith("exécute skill ") or t.startswith("execute skill "):
        nom = t.split("skill", 1)[1].strip()
        if not nom:
            return "Précisez le nom de la skill à exécuter."
        return executer_skill(nom)

    # Proposer une nouvelle skill (ici, on simule la génération de code)
    if t.startswith("propose une skill ") or t.startswith("propose une nouvelle skill "):
        # Exemple : "propose une skill bonjour"
        parts = t.split()
        if len(parts) >= 4:
            nom_skill = parts[-1]
            # Ici, on génère un code Python robuste de manière automatique
            code = f'''
def {nom_skill}():
    """
    Skill générée automatiquement par {NOM_IA}.
    """
    try:
        return "Skill '{nom_skill}' exécutée avec succès."
    except Exception as e:
        return f"Erreur dans la skill '{nom_skill}': {{e}}"
'''.strip()
            # On ne l'ajoute pas directement : dans un vrai flux,
            # tu pourrais d'abord afficher ce code côté client
            # et demander "Valides-tu ce code ?"
            return (
                "Je propose la skill suivante :\n\n"
                f"{code}\n\n"
                "Si tu valides, envoie ce code via l'API /api/add_skill."
            )
        else:
            return "Précisez le nom de la skill à proposer. Exemple : 'propose une skill bonjour'."

    # Par défaut
    return reponse_generique()


# =============================
#     Routes HTTP
# =============================

@app.get("/")
def racine():
    return {"message": f"{NOM_IA} en ligne. API opérationnelle."}


@app.post("/api/chat")
def chat(msg: Message):
    reponse = analyse_commande(msg.message)
    return {"response": reponse}


@app.post("/api/add_skill")
def add_skill(req: AddSkillRequest):
    """
    Ajout contrôlé d'une nouvelle skill.
    On suppose que le code a été validé côté humain avant l'appel.
    """
    try:
        ajouter_skill_dans_fichier(req.name, req.code)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'ajout de la skill : {e}")
    return {"status": "ok", "message": f"Skill '{req.name}' ajoutée et rechargée."}


@app.post("/api/delete_skill")
def delete_skill(req: DeleteSkillRequest):
    """
    Suppression contrôlée d'une skill existante.
    """
    try:
        supprimer_skill_du_fichier(req.name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la suppression de la skill : {e}")
    return {"status": "ok", "message": f"Skill '{req.name}' supprimée et rechargée."}

