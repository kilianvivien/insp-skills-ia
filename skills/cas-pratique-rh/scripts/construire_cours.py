#!/usr/bin/env python3
"""Reconstruit le corpus texte du cours INSP à partir des PDF (outil de maintenance).

À relancer seulement si les PDF du cours changent :
    uv run --with pymupdf python scripts/construire_cours.py /chemin/vers/Cours

Produit references/cours/chapitre-N.md (texte page par page, numéros de page = pages du PDF)
et data/plan_cours.json (chapitres > cas > leçons > plages de pages).
"""
import glob
import json
import os
import re
import sys

import pymupdf

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TITRES = {
    1: "L'agent public",
    2: "Le management au quotidien",
    3: "Le management en situation de crise",
    4: "Promouvoir les talents et organiser les carrières",
}
BRUIT = re.compile(r"^(SUBMIT|CONTINUER|TERMINER LE MODULE|QUITTER|1x|Continue|Next Slide|End of Scenario|Scene \d+ Slide \d+)$")
LOREM = re.compile(r"lorem ipsum|consectetur|sollicitudin|tincidunt", re.I)


def nettoyer(texte):
    texte = texte.replace("\u00a0", " ")
    # "(nouvel onglet)" signale un lien hypertexte dans le module ; la mention est parfois coupée en fin de ligne
    texte = re.sub(r"[ \t]*\(\s*nouvel\s+onglet\s*\)", " [lien]", texte)
    texte = re.sub(r"\s*[-–]\s*nouvel\s+onglet\s*\)", ") [lien]", texte)
    lignes = []
    for l in texte.split("\n"):
        s = l.strip()
        if not s or BRUIT.match(s) or LOREM.search(s):
            continue
        lignes.append(s)
    return "\n".join(lignes)


def chapitre(num, pdf):
    doc = pymupdf.open(pdf)
    bruts = [p.get_text() for p in doc]
    pages = [nettoyer(t) for t in bruts]
    quiz = [bool(re.search(r"^SUBMIT$", t, re.M)) for t in bruts]
    # sommaire : pages précédant "Leçon 1 sur N"
    debut = next(i for i, t in enumerate(pages) if re.search(r"Leçon 1 sur \d+", t))
    nb = int(re.search(r"Leçon 1 sur (\d+)", pages[debut]).group(1))
    sommaire = "\n".join(pages[:debut]).split("\n")
    cas, titres, courant, saute = {}, [], None, False
    for l in sommaire:
        m = re.match(r"^(\d+)\.\s+(.*)", l)
        if m:
            courant = int(m.group(1)); cas[courant] = m.group(2); saute = False; continue
        if saute and l[0].islower():  # suite du titre de chapitre coupé sur deux lignes
            saute = False; continue
        saute = l.startswith("Chapitre ")
        if saute or l in ("Fin de chapitre", "COMPLÉMENTS"):
            courant = None; continue
        if courant and l.isupper():
            cas[courant] += " " + l; continue
        courant = None
        titres.append(l)
    # recolle les titres de leçon coupés sur deux lignes
    while len(titres) > nb - (0 if "Liste des abréviations" in titres else 1) and len(titres) > 1:
        k = next((i for i in range(1, len(titres)) if titres[i][0].islower()), None)
        if k is None:
            break
        titres[k - 1] += " " + titres.pop(k)
    plan, lecons = [], []
    num_cas = 0
    for i, t in enumerate(pages):
        m = re.search(r"Leçon (\d+) sur \d+", t)
        if m:
            n = int(m.group(1))
            titre = titres[n - 1] if n - 1 < len(titres) else "Fin de chapitre"
            mc = re.match(r"Contexte partie (\d+)", titre)
            if mc:
                num_cas = int(mc.group(1))
                titre = "Énoncé du cas (contexte)"
            elif titre in ("Liste des abréviations", "Fin de chapitre"):
                num_cas = 0
            lecons.append({"lecon": n, "titre": titre, "cas": num_cas, "debut": i + 1})
    for a, b in zip(lecons, lecons[1:] + [{"debut": len(pages) + 1}]):
        a["fin"] = b["debut"] - 1
    sortie = [f"# INSP — Chapitre {num} : {TITRES[num]}\n",
              f"Texte extrait du PDF du cours ({len(pages)} pages). Les numéros « p. N » sont les numéros de page du PDF.",
              "Les pages de quiz listent des propositions de réponse : ce ne sont pas des affirmations du cours ; la règle figure dans les pages d'explication qui suivent.\n"]
    for i, t in enumerate(pages, 1):
        l = next((x for x in lecons if x["debut"] <= i <= x["fin"]), None)
        if l:
            ctx = (f"Cas {l['cas']} : {cas[l['cas']].capitalize()} — " if l["cas"] else "Annexe — ") + f"Leçon {l['lecon']} : {l['titre']}"
        else:
            ctx = "Sommaire du chapitre"
        if quiz[i - 1]:
            ctx += " | QUIZ (propositions de réponse, pas des affirmations du cours)"
        sortie.append(f"\n## p. {i}\n<!-- {ctx} -->\n{t if t else '[page sans texte : image ou bouton de navigation]'}")
    with open(os.path.join(RACINE, "references", "cours", f"chapitre-{num}.md"), "w") as f:
        f.write("\n".join(sortie) + "\n")
    return {"chapitre": num, "titre": TITRES[num], "pages": len(pages),
            "cas": [{"cas": k, "titre": v.capitalize()} for k, v in sorted(cas.items())], "lecons": lecons}


REFS = [
    r"\b[LRD]\.?\s?\d{3}-\d+(?:-\d+)?(?:\s+(?:à|et)\s+[LRD]\.?\s?\d{3}-\d+(?:-\d+)?)?(?:\s+du\s+(?:CGFP|code [a-zé' ]{4,40}?(?=[,.;:)\[]| \[| et | qui | pr)))?",
    r"[Dd]écret\s+(?:n\s*°\s*)?\d{2,4}-\s?\d+(?: du \d+\w* \w+ \d{4})?",
    r"[Ll]oi\s+(?:organique\s+)?(?:n\s*°\s*\d{2,4}-\d+\s+)?du \d+\w* \w+ \d{4}",
    r"[Oo]rdonnance\s+(?:n\s*°\s*\d{2,4}-\d+\s+)?du \d+\w* \w+ \d{4}",
    r"[Cc]irculaire[^.;\n]{0,40}? du \d+\w* \w+ \d{4}",
    r"(?:Conseil d['’]État|CE|CAA [A-Z]\w+|CEDH),[^.;\n]{0,70}?n\s*°\s*\d[\d\-. ]*\d",
    r"(?:article|art\.)\s+\d+(?:-\d+)*\s+du\s+[Cc]ode\s+[a-zé' ]{4,30}?(?=[,.;:)\[]| \[| et | qui )",
]


def ecrire_plan(plan):
    """references/plan-cours.md : plan détaillé + références juridiques citées par leçon (généré)."""
    out = ["# Plan détaillé du cours INSP et références juridiques citées\n",
           "Fichier généré par `scripts/construire_cours.py` — ne pas modifier à la main.",
           "Pour chaque leçon : pages du PDF, puis les références juridiques que le cours y cite (avec la page).",
           "Ces références sont celles du cours, à la date de sa rédaction : leur état actuel se vérifie sur Légifrance.\n"]
    for c in plan:
        t = open(os.path.join(RACINE, "references", "cours", f"chapitre-{c['chapitre']}.md")).read()
        pages = {int(a): b for a, b in re.findall(r"\n## p\. (\d+)\n<!--.*?-->\n(.*?)(?=\n\n## p\. |\Z)", t, re.S)}
        out.append(f"\n## Chapitre {c['chapitre']} — {c['titre']} ({c['pages']} p.)")
        cas_titres = {k["cas"]: k["titre"] for k in c["cas"]}
        courant = None
        for l in c["lecons"]:
            if l["cas"] != courant:
                courant = l["cas"]
                out.append(f"\n### Cas {courant} — {cas_titres[courant]}" if courant else "\n### Annexes")
            vues, refs = set(), []
            for i in range(l["debut"], l["fin"] + 1):
                txt = pages.get(i, "").replace("\n", " ")
                for rx in REFS:
                    for m in re.finditer(rx, txt):
                        r = re.sub(r"\s+", " ", m.group(0)).strip(" ,")
                        cle = re.sub(r"[.\s°n]", "", r.lower())
                        if cle not in vues:
                            vues.add(cle); refs.append(f"{r} (p. {i})")
            out.append(f"- **Leçon {l['lecon']} — {l['titre']}** : p. {l['debut']}-{l['fin']}" + (" — " + " ; ".join(refs) if refs else ""))
    with open(os.path.join(RACINE, "references", "plan-cours.md"), "w") as f:
        f.write("\n".join(out) + "\n")


def main():
    src = sys.argv[1]
    plan = []
    for pdf in sorted(glob.glob(os.path.join(src, "*.pdf"))):
        num = int(re.search(r"Chapitre\s*(\d)", os.path.basename(pdf)).group(1))
        plan.append(chapitre(num, pdf))
    with open(os.path.join(RACINE, "data", "plan_cours.json"), "w") as f:
        json.dump(plan, f, ensure_ascii=False, indent=1)
    ecrire_plan(plan)
    for c in plan:
        print(f"Chapitre {c['chapitre']} : {c['pages']} pages, {len(c['cas'])} cas, {len(c['lecons'])} leçons")


if __name__ == "__main__":
    main()
