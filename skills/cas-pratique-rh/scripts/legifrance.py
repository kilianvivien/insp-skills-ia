#!/usr/bin/env python3
"""Construit les adresses Légifrance exactes à consulter (aucun accès réseau : Légifrance refuse les scripts).

    python3 scripts/legifrance.py article L530-1 R431-5 [--date 2026-10-13]
        -> pour chaque article du CGFP : existe-t-il ? adresse de la section qui le contient, à la date voulue
    python3 scripts/legifrance.py code penal 222-33-2 [--date AAAA-MM-JJ]
        -> adresse de recherche de l'article dans un autre code (travail, penal, crpa, justice-administrative…)
    python3 scripts/legifrance.py texte teletravail        (ou : texte 86-83)
        -> textes de référence dont l'identifiant est vérifié + adresse datée
    python3 scripts/legifrance.py recherche jurisprudence-administrative "harcèlement moral protection fonctionnelle"
        -> adresse de recherche (fonds : codes, textes, jurisprudence-administrative, jurisprudence-judiciaire,
           constitutionnel, circulaires, jorf, tout)
    python3 scripts/legifrance.py recherche textes 2026-366 --titre
        -> recherche dans les seuls intitulés : le moyen fiable de retrouver un texte par son numéro
           (la recherche plein texte et le champ NUM_DEC renvoient des résultats sans rapport)
    python3 scripts/legifrance.py lien LEGIARTI000044426132 [--date AAAA-MM-JJ] [--decret]
        -> forme canonique du lien direct à partir d'un identifiant relevé sur une page Légifrance
           (--decret : article d'un décret ou d'une loi non codifiés, lien /loda/article_lc/…)

Les adresses produites s'ouvrent ensuite dans le navigateur, moyen principal (attendre 8 s, puis exécuter
scripts/extracteur_legifrance.js), ou à défaut avec WebFetch (voir references/legifrance.md, section 1).
La date par défaut est celle du jour ; pour un cas dont les faits sont datés, passer --date à la date des faits.
"""
import argparse
import datetime
import os
import re
import sys
import unicodedata
from urllib.parse import quote_plus

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://www.legifrance.gouv.fr"
CGFP = "LEGITEXT000044416551"
DATE_TABLE = "2026-10-13"  # date de relevé de data/cgfp_sections.txt
FONDS = {
    "codes": ("/search/code", "code"),
    "textes": ("/search/lois", "lawarticledecree"),
    "jurisprudence-administrative": ("/search/cetat", "cetat"),
    "jurisprudence-judiciaire": ("/search/juri", "juri"),
    "constitutionnel": ("/search/constit", "constit"),
    "circulaires": ("/search/circ", "circ"),
    "jorf": ("/search/jorf", "jorf"),
    "tout": ("/search/all", "all"),
}


def signal_pipe():
    """Sortie propre quand la sortie est coupée (`… | head`)."""
    try:
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (AttributeError, ValueError):
        pass


def sans_accent(s):
    return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")


def cle(art):
    """Clé de tri d'un numéro d'article du CGFP : 'L132-9-3' -> ('L', (132, 9, 3)). R, D et R* sont une même partie."""
    a = art.upper().replace("*", "").replace(".", "").replace(" ", "")
    m = re.match(r"^([LRD])(\d+(?:-\d+)*)([A-Z]?)$", a)
    if not m:
        return None
    nums = [float(x) for x in m.group(2).split("-")]
    if m.group(3):  # « L135-6 A » précède « L135-6 »
        nums[-1] -= 0.5
    return ("L" if m.group(1) == "L" else "R", tuple(nums))


def table():
    out = []
    for l in open(os.path.join(RACINE, "data", "cgfp_sections.txt"), encoding="utf-8"):
        l = l.strip()
        if not l:
            continue
        ident, reste = l.split(" ", 1)
        m = re.findall(r"[LRD]\*?\d+(?:-\d+)*(?: [A-Z](?= |$))?", reste)
        premier, dernier = m[0], m[-1]
        out.append(("LEGISCTA0000" + ident, premier, dernier, cle(premier.replace(" ", "")), cle(dernier.replace(" ", ""))))
    return out


def jour(s):
    if not s:
        return datetime.date.today().isoformat()
    try:
        return datetime.date.fromisoformat(s).isoformat()
    except ValueError:
        sys.exit("Date attendue au format AAAA-MM-JJ.")


def cmd_article(args):
    d = jour(args.date)
    tab = table()
    for art in args.articles:
        k = cle(art)
        aff = art.upper().replace(".", "").replace(" ", "")
        if not k:
            print(f"✗ {art} : numéro illisible (formats attendus : L530-1, R431-5, D311-1).\n")
            continue
        trouve = [t for t in tab if t[3][0] == k[0] and t[3] <= k <= t[4]]
        if not trouve:
            partie = [t for t in tab if t[3][0] == k[0]]
            avant = [t for t in partie if t[4] < k]
            apres = [t for t in partie if t[3] > k]
            print(f"✗ {aff} : aucun article de ce numéro dans le CGFP (table du {DATE_TABLE}).")
            if avant or apres:
                print("  Articles voisins : " + " | ".join(x for x in [avant[-1][2] if avant else "", apres[0][1] if apres else ""] if x))
            if k[0] == "R" and k[1][0] >= 500:
                print("  La partie réglementaire du CGFP s'arrête au livre IV (table du " + DATE_TABLE + ") : pour les livres V à VIII,")
                print("  la règle se trouve encore dans des décrets (commande `texte` ou `recherche textes`).")
            print("  Ne pas citer cet article sans l'avoir retrouvé : vérifier le numéro (cours, sommaire du code) ou chercher par mots clés.")
            print(f"  Sommaire du code à la date voulue : {BASE}/codes/texte_lc/{CGFP}/{d}\n")
            continue
        s = trouve[0]
        plage = s[1] if s[1] == s[2] else f"{s[1]} à {s[2]}"
        print(f"✓ {aff} — CGFP, section couvrant {plage}")
        print(f"  Ouvrir (version au {d}) : {BASE}/codes/section_lc/{CGFP}/{s[0]}/{d}")
        print(f"  Relever : le texte, « Version en vigueur depuis/du… au… », « Modifié par / Création », et l'identifiant LEGIARTI")
        print(f"  Lien à citer une fois l'identifiant relevé : {BASE}/codes/article_lc/LEGIARTI…  (commande `lien`)\n")
    print("Rappel : la présence du numéro dans la table ne dit rien de son contenu. Seule la page ouverte fait foi.")


def cmd_code(args):
    d = jour(args.date)
    codes = {}
    for l in open(os.path.join(RACINE, "data", "textes_cles.tsv"), encoding="utf-8"):
        c = l.rstrip("\n").split("\t")
        if c[0] == "code":
            codes[c[1].lower()] = (c[2], c[3])
    nom = sans_accent(args.code).replace(" ", "-")
    nom = {"csi": "securite-interieure", "cja": "justice-administrative", "cpp": "procedure-penale", "css": "securite-sociale",
           "csp": "sante-publique", "code-penal": "penal", "code-du-travail": "travail"}.get(nom, nom)
    if nom == "cgfp":
        return cmd_article(argparse.Namespace(articles=[args.article], date=args.date))
    if nom not in codes:
        sys.exit("Code inconnu. Codes disponibles : " + ", ".join(sorted(codes)) + ".\nPour un autre code : `recherche codes \"nom du code article N\"`.")
    ident, titre = codes[nom]
    q = quote_plus(f"{titre} article {args.article}")
    print(f"{titre} — article {args.article}")
    print(f"  Recherche de l'article : {BASE}/search/code?tab_selection=code&searchField=ALL&query={q}&searchType=ALL&typePagination=DEFAULT&pageSize=10&page=1")
    print(f"  Sommaire du code (version au {d}) : {BASE}/codes/texte_lc/{ident}/{d}")
    print("  Dans les résultats, ne retenir que la ligne dont le code ET le numéro d'article correspondent exactement ;")
    print("  relever son identifiant LEGIARTI, puis ouvrir le lien direct (commande `lien`) pour lire la version en vigueur.")


def cmd_texte(args):
    q = sans_accent(" ".join(args.mots))
    d = jour(args.date)
    n = 0
    for l in open(os.path.join(RACINE, "data", "textes_cles.tsv"), encoding="utf-8"):
        if l.startswith("#") or not l.strip():
            continue
        typ, num, ident, titre, mots = l.rstrip("\n").split("\t")
        foin = sans_accent(" ".join([num, titre, mots]))
        if all(m in foin for m in q.split()):
            n += 1
            chemin = f"/codes/texte_lc/{ident}/{d}" if typ == "code" else f"/loda/id/{ident}/{d}/"
            print(f"■ {titre}\n  {BASE}{chemin}")
            if typ != "code":
                print("  Vérifier en tête de page si le texte est en vigueur, modifié ou abrogé à cette date.")
                print("  Navigateur : l'extracteur lit la page entière ; filtrer son résultat sur les articles utiles (legifrance.md, section 1).")
                print("  Secours WebFetch : la page longue est tronquée ; ouvrir l'article seul : `lien LEGIARTI… --decret`.")
            print()
    if not n:
        print("Aucun texte de la table ne correspond. Chercher sur Légifrance :")
        numero = re.fullmatch(r"\d{2,4}-\d{1,5}", " ".join(args.mots).strip())
        cmd_recherche(argparse.Namespace(fonds="textes", requete=" ".join(args.mots), titre=bool(numero), recent=False))


def cmd_recherche(args):
    if args.fonds not in FONDS:
        sys.exit("Fonds inconnu. Fonds disponibles : " + ", ".join(FONDS))
    chemin, onglet = FONDS[args.fonds]
    tri = "&sortValue=DATE_DESC" if args.fonds.startswith("jurisprudence") and getattr(args, "recent", False) else ""
    champ = "TITLE" if getattr(args, "titre", False) else "ALL"
    print(f"{BASE}{chemin}?tab_selection={onglet}&searchField={champ}&query={quote_plus(args.requete)}&searchType=ALL&typePagination=DEFAULT{tri}&pageSize=10&page=1")
    if champ == "ALL" and re.search(r"\b\d{2,4}-\d{1,5}\b", args.requete):
        print("Requête contenant un numéro de texte : la recherche plein texte le retrouve mal. Relancer avec --titre")
        print("(recherche dans les intitulés), ou remonter au texte par le lien « Création / Modifié par … » d'un article qu'il a créé.")
    print("Dans la page de résultats, relever pour chaque résultat utile son identifiant (LEGIARTI, JORFTEXT, CETATEXT, JURITEXT…)")
    print("puis ouvrir la page du résultat avant de le citer : un titre de résultat ne suffit pas à fonder une affirmation.")


def cmd_lien(args):
    i = args.identifiant.strip().upper()
    d = f"/{jour(args.date)}" if args.date else ""
    formes = {
        "LEGIARTI": f"/loda/article_lc/{i}{d}" if args.decret else f"/codes/article_lc/{i}{d}",
        "LEGISCTA": f"/codes/section_lc/{CGFP}/{i}{d}",
        "LEGITEXT": f"/codes/texte_lc/{i}{d}",
        "JORFTEXT": f"/loda/id/{i}{d}",
        "CETATEXT": f"/ceta/id/{i}",
        "JURITEXT": f"/juri/id/{i}",
        "CONSTEXT": f"/cons/id/{i}",
    }
    if not re.match(r"^[A-Z]{8}\d{12}$", i) or i[:8] not in formes:
        sys.exit("Identifiant invalide : 8 lettres (LEGIARTI, LEGISCTA, LEGITEXT, JORFTEXT, CETATEXT, JURITEXT, CONSTEXT) suivies de 12 chiffres.")
    print(BASE + formes[i[:8]])
    if i.startswith("LEGIARTI") and not args.decret:
        print("Forme valable pour un article de CODE. Si l'identifiant vient d'un décret ou d'une loi non codifiés, relancer avec --decret :")
        print(f"{BASE}/loda/article_lc/{i}{d}")
    if i.startswith("LEGISCTA"):
        print("(forme valable pour une section du CGFP ; pour un autre code, remplacer l'identifiant LEGITEXT)")


def main():
    signal_pipe()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    a = sp.add_parser("article"); a.add_argument("articles", nargs="+"); a.add_argument("--date")
    a = sp.add_parser("code"); a.add_argument("code"); a.add_argument("article"); a.add_argument("--date")
    a = sp.add_parser("texte"); a.add_argument("mots", nargs="+"); a.add_argument("--date")
    a = sp.add_parser("recherche"); a.add_argument("fonds"); a.add_argument("requete"); a.add_argument("--recent", action="store_true")
    a.add_argument("--titre", action="store_true", help="chercher dans les seuls intitulés (pour retrouver un texte par son numéro)")
    a = sp.add_parser("lien"); a.add_argument("identifiant"); a.add_argument("--date")
    a.add_argument("--decret", action="store_true", help="l'identifiant LEGIARTI est celui d'un article de décret ou de loi non codifié")
    args = ap.parse_args()
    {"article": cmd_article, "code": cmd_code, "texte": cmd_texte, "recherche": cmd_recherche, "lien": cmd_lien}[args.cmd](args)


if __name__ == "__main__":
    main()
