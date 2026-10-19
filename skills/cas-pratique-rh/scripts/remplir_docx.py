#!/usr/bin/env python3
"""Remplit le support Word fourni (par l'école, le jury) avec un kit de réponse rédigé en Markdown.

    uv run --with python-docx python scripts/remplir_docx.py support.docx kit.md sortie.docx
        [--sans-liens] [--supprimer "^Exemple"] [--motif "^\\s*Question\\s*(\\d+)"] [--style-puce "List Bullet"] [--analyser]

Le kit est découpé sur ses titres « ## Question N … » ; chaque bloc est inséré dans le support juste
sous le paragraphe qui porte la question N (repéré par --motif, dont le premier groupe est le numéro).
Les puces reprennent la mise en forme des puces du gabarit (premier paragraphe numéroté trouvé),
à défaut le style --style-puce. Les sections du kit qui ne sont pas des questions (« ## Références »,
« ## Charte IA »…) sont ajoutées en fin de document, tableaux compris.
Gras et italique Markdown sont conservés ; un lien [texte](adresse) devient « texte (adresse) »,
ou « texte » seul avec --sans-liens (les adresses restent alors dans la table « Références », qui les
garde toujours). Avec une longueur imposée par question, utiliser --sans-liens : une adresse Légifrance
écrite en entier prend une ligne Word à elle seule (constat de l'évaluation du 17/10/2026).
Le chapeau du kit (lignes entre le titre « # … » et la première question : sources, date de
version, « sans recommandation ») est inséré juste avant la première question du support.
--supprimer MOTIF retire les paragraphes du gabarit dont le texte correspond (puces d'exemple…).
Le support d'origine n'est jamais modifié : la sortie est un nouveau fichier.

--analyser : n'écrit rien ; liste les paragraphes reconnus comme questions et les styles disponibles.
Toujours ouvrir la sortie (ou la convertir en PDF) pour contrôler la mise en page avant de la remettre.
"""
import argparse
import copy
import re
import sys

try:
    import docx
    from docx.oxml.ns import qn
except ImportError:
    sys.exit("python-docx manque : lancer avec `uv run --with python-docx python scripts/remplir_docx.py …`")


def lire_kit(chemin):
    """{numéro: [lignes]} pour les questions, [(titre, [lignes])] pour les autres sections, et le chapeau."""
    questions, autres, chapeau, courant = {}, [], [], None
    for l in open(chemin, encoding="utf-8").read().split("\n"):
        m = re.match(r"^##\s+(.+)$", l)
        if m:
            n = re.match(r"^Question\s*(\d+)", m.group(1), re.I)
            if n:
                courant = questions.setdefault(int(n.group(1)), [])
            else:
                courant = []
                autres.append((m.group(1).strip(), courant))
            continue
        if l.startswith("# "):
            courant = chapeau if not questions and not autres else None
            continue
        if courant is not None:
            courant.append(l)
    return questions, autres, chapeau


SANS_LIENS = False


def runs(par, texte, garder_liens=False):
    """Ajoute le texte au paragraphe en interprétant **gras**, *italique* et [lien](url)."""
    texte = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r"\1" if SANS_LIENS and not garder_liens else r"\1 (\2)", texte)
    for morceau in re.split(r"(\*\*[^*]+\*\*|\*[^*\s][^*]*\*)", texte):
        if not morceau:
            continue
        if morceau.startswith("**") and morceau.endswith("**"):
            par.add_run(morceau[2:-2]).bold = True
        elif morceau.startswith("*") and morceau.endswith("*") and len(morceau) > 2:
            par.add_run(morceau[1:-1]).italic = True
        else:
            par.add_run(morceau)


def tous_paragraphes(doc):
    yield from doc.paragraphs
    for t in doc.tables:
        for ligne in t.rows:
            for cel in ligne.cells:
                yield from cel.paragraphs


def modele_puce(doc, style):
    for p in tous_paragraphes(doc):
        if p._p.pPr is not None and p._p.pPr.find(qn("w:numPr")) is not None and p.text.strip():
            return copy.deepcopy(p._p.pPr)
    for p in tous_paragraphes(doc):  # puces portées par un style de liste du gabarit
        if p.text.strip() and re.search(r"list|puce|liste|bullet", p.style.name, re.I):
            return p.style.name
    noms = {s.name for s in doc.styles}
    return style if style in noms else None


def nouveau_paragraphe(apres, parent, doc, ppr=None, style=None):
    """Crée un paragraphe juste après l'élément XML `apres`, dans `parent` (corps du document ou cellule)."""
    p = docx.text.paragraph.Paragraph(docx.oxml.OxmlElement("w:p"), parent)
    apres.addnext(p._p)
    if isinstance(ppr, str):
        p.style = doc.styles[ppr]
    elif ppr is not None:
        p._p.insert(0, copy.deepcopy(ppr))
    elif style:
        p.style = doc.styles[style]
    return p


def inserer(doc, ancre, lignes, puce):
    """Insère les lignes Markdown après le paragraphe `ancre`, dans l'ordre."""
    dernier, parent = ancre._p, ancre._parent
    tableau = []

    def vider_tableau():
        nonlocal dernier, tableau
        if not tableau:
            return
        lignes_t = [[c.strip() for c in l.strip().strip("|").split("|")] for l in tableau if not re.match(r"^\|?\s*:?-{2,}", l.strip())]
        tableau = []
        if not lignes_t:
            return
        t = doc.add_table(rows=len(lignes_t), cols=max(len(r) for r in lignes_t))
        if "Table Grid" in {s.name for s in doc.styles}:
            t.style = doc.styles["Table Grid"]
        for i, r in enumerate(lignes_t):
            for j, c in enumerate(r):
                cel = t.cell(i, j).paragraphs[0]
                runs(cel, c, garder_liens=True)
                if i == 0:
                    for x in cel.runs:
                        x.bold = True
        dernier.addnext(t._tbl)
        dernier = t._tbl

    for l in lignes:
        s = l.rstrip()
        if s.strip().startswith("|"):
            tableau.append(s)
            continue
        vider_tableau()
        if not s.strip() or s.strip().startswith(("<!--", "---")):
            continue
        m = re.match(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$", s)
        if m:
            p = nouveau_paragraphe(dernier, parent, doc, ppr=puce)
            if m.group(1):  # sous-puce : retrait supplémentaire
                p.paragraph_format.left_indent = docx.shared.Cm(1.27 * (1 + len(m.group(1)) // 2))
            runs(p, m.group(3))
        else:
            h = re.match(r"^#{3,6}\s+(.*)$", s)
            p = nouveau_paragraphe(dernier, parent, doc)
            if h:
                p.add_run(h.group(1)).bold = True
            else:
                runs(p, s.lstrip("> ").strip())
        dernier = p._p
    vider_tableau()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("support")
    ap.add_argument("kit", nargs="?")
    ap.add_argument("sortie", nargs="?")
    ap.add_argument("--motif", default=r"^\s*(?:Question|Q\.?)\s*n?°?\s*(\d+)", help="expression qui repère une question dans le support ; groupe 1 = numéro")
    ap.add_argument("--style-puce", default="List Bullet")
    ap.add_argument("--sans-liens", action="store_true", help="liens en ligne réduits à leur libellé (hors tableaux)")
    ap.add_argument("--supprimer", help="expression : paragraphes du gabarit à retirer (ex. « ^Exemple »)")
    ap.add_argument("--analyser", action="store_true")
    args = ap.parse_args()
    doc = docx.Document(args.support)
    rx = re.compile(args.motif, re.I)
    ancres = {}
    for p in tous_paragraphes(doc):
        m = rx.search(p.text)
        if m and int(m.group(1)) not in ancres:
            ancres[int(m.group(1))] = p
    if args.analyser or not args.kit:
        print(f"{len(ancres)} question(s) repérée(s) dans le support :")
        for n, p in sorted(ancres.items()):
            print(f"  Q{n} [{p.style.name}] {p.text[:100]}")
        puce = modele_puce(doc, args.style_puce)
        print("Puces : " + ("mise en forme du premier paragraphe numéroté du gabarit" if puce is not None and not isinstance(puce, str) else f"style « {puce} »" if puce else "aucun modèle (texte simple précédé d'un tiret)"))
        print("Styles de paragraphe : " + ", ".join(sorted(s.name for s in doc.styles if s.type == 1)))
        return
    if not args.sortie:
        sys.exit("Indiquer le fichier de sortie.")
    if args.sortie == args.support:
        sys.exit("La sortie doit être un nouveau fichier : le support d'origine ne se modifie pas.")
    global SANS_LIENS
    SANS_LIENS = args.sans_liens
    questions, autres, chapeau = lire_kit(args.kit)
    puce = modele_puce(doc, args.style_puce)
    retires = 0
    if args.supprimer:
        rx_sup = re.compile(args.supprimer, re.I)
        for p in list(tous_paragraphes(doc)):
            if p.text.strip() and rx_sup.search(p.text) and p not in ancres.values():
                p._p.getparent().remove(p._p)
                retires += 1
    manquantes = sorted(set(questions) - set(ancres))
    for n in sorted(questions):
        if n in ancres:
            inserer(doc, ancres[n], questions[n], puce)
    if any(l.strip() for l in chapeau) and ancres:
        premiere = ancres[min(ancres)]
        repere = nouveau_paragraphe(premiere._p, premiere._parent, doc)
        premiere._p.addprevious(repere._p)  # paragraphe vide, déplacé avant la première question
        inserer(doc, repere, chapeau, puce)
        repere._p.getparent().remove(repere._p)
    titre2 = "Heading 2" if "Heading 2" in {s.name for s in doc.styles} else None
    for titre, lignes in autres:
        corps = doc.element.body
        dernier = [e for e in corps if e.tag != qn("w:sectPr")][-1]
        h = nouveau_paragraphe(dernier, doc._body, doc, style=titre2)
        h.add_run(titre).bold = True
        inserer(doc, h, lignes, puce)
    doc.save(args.sortie)
    print(f"✓ {len(set(questions) & set(ancres))} question(s) remplie(s) ; {len(autres)} section(s) ajoutée(s) en fin de document → {args.sortie}")
    if args.supprimer:
        print(f"{'✓' if retires else '!'} {retires} paragraphe(s) du gabarit retiré(s) (motif : {args.supprimer}).")
    if not args.sans_liens and any("](http" in l for q in questions.values() for l in q):
        print("! Liens écrits en entier dans les réponses : avec une longueur imposée par question, relancer avec --sans-liens.")
    for n in manquantes:
        print(f"✗ Question {n} du kit introuvable dans le support (motif : {args.motif}) : vérifier avec --analyser.")
    for n in sorted(set(ancres) - set(questions)):
        print(f"! Question {n} du support sans réponse dans le kit.")
    sys.exit(1 if manquantes else 0)


if __name__ == "__main__":
    main()
