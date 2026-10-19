#!/usr/bin/env python3
"""Contrôle une réponse rédigée (fichier Markdown) avant de la remettre.

    python3 scripts/verifier_reponse.py reponse.md [--mode complet|chrono|kit|libre]
        [--enonce enonce.md] [--lignes-par-section 10-15] [--max-mots-par-section N] [--ignorer-mention]

Ce que le contrôle attrape :
  - pages du cours citées qui n'existent pas, ou qui sont un énoncé / un quiz et non une règle ;
  - citations entre guillemets attribuées au cours mais introuvables dans les pages citées ;
  - articles du CGFP cités qui n'existent pas dans le code ;
  - liens hors des sources autorisées, liens Légifrance mal formés, liens de recherche, liens « à compléter » ;
  - références Légifrance sans lien (sauf simple mention de périmètre : « non traité ici », « hors champ »…),
    et articles du CGFP cités sans être liés nulle part dans la réponse ;
  - lien [L530-1](…LEGIARTI…) dont l'identifiant appartient à un autre article (table data/cgfp_articles.tsv) ;
  - plan ou longueur non conformes au format demandé, y compris par question (--lignes-par-section, --max-mots-par-section) ;
  - en mode kit : blocs « Dans la situation », « Règles », « Options » absents d'une question, recommandation glissée ;
  - avec --enonce : section qui ne reprend aucun élément de l'énoncé (réponse récitée, non ancrée).
Ce qu'il ne fait pas : juger le fond, ni confirmer qu'un article dit bien ce que la réponse lui fait dire.
Code de sortie 1 s'il reste des erreurs (✗) ; les avertissements (!) se corrigent ou se justifient.
"""
import argparse
import importlib.util
import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))


def module(nom):
    spec = importlib.util.spec_from_file_location(nom, os.path.join(ICI, nom + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


VIDES_ENONCE = set("""alors aussi autre autres avant avec avoir bien cela celle celui cette comme dans depuis donc elle elles entre est être
fait faire font leur leurs mais même moins notre nous parce pendant peut plus pour quand quel quelle quelles quels sans selon
sera sont sous tout toute toutes tous très vous votre vos avez avait ainsi après chez dont encore lors lorsque puis votre
question questions situation agent agents service services cas vous-même madame monsieur chef bureau""".split())
PERIMETRE = re.compile(r"non trait[ée]|hors (du )?champ|non applicable|sans objet|non abord[ée]|pour m[ée]moire|non v[ée]rifi[ée]|ne s'applique pas|non concern[ée]|n'est pas trait[ée]", re.I)
SECTIONS_ANNEXES = re.compile(r"r[ée]f[ée]rences|sources|table|annexe|charte|synth[èe]se|en bref|sommaire|avertissement|m[ée]thode", re.I)


def table_articles():
    """{article: LEGIARTI} relevés dans le navigateur (data/cgfp_articles.tsv)."""
    chemin = os.path.join(ICI, "..", "data", "cgfp_articles.tsv")
    out = {}
    if os.path.exists(chemin):
        for l in open(chemin, encoding="utf-8"):
            c = l.rstrip("\n").split("\t")
            if len(c) >= 2 and not l.startswith("#"):
                out[c[0].strip()] = c[1].strip()
    return out


def sections(texte, niveau):
    """Découpe le texte en (titre, corps) sur les titres Markdown du niveau donné (2 = « ## »)."""
    rx = re.compile(r"^#{%d}\s+(.+)$" % niveau, re.M)
    marques = list(rx.finditer(texte))
    out = []
    for i, m in enumerate(marques):
        fin = marques[i + 1].start() if i + 1 < len(marques) else len(texte)
        corps = texte[m.end():fin]
        # le corps s'arrête au titre de niveau supérieur suivant
        sup = re.search(r"^#{1,%d}\s" % (niveau - 1), corps, re.M) if niveau > 1 else None
        out.append((m.group(1).strip(), corps[: sup.start()] if sup else corps))
    return out


def lignes_imprimees(corps, largeur):
    """Estimation du nombre de lignes une fois le texte mis en page (Word, A4, police 11 : environ 95 caractères)."""
    n = 0
    for l in corps.split("\n"):
        l = l.strip()
        if not l or l.startswith(("|", "#", ">", "<!--")):
            continue
        puce = bool(re.match(r"^([-*+]|\d+[.)])\s", l))
        l = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", l)
        l = re.sub(r"https?://\S+", "", l).replace("**", "").replace("*", "")
        n += max(1, -(-len(l) // (largeur - (5 if puce else 0))))
    return n


def vocabulaire(t):
    """Mots d'au moins cinq lettres, sans accents ni mots vides : sert à repérer qu'une section reprend l'énoncé."""
    return {w for w in (x.split("'")[-1] for x in re.findall(r"[a-z0-9][a-z0-9'-]{4,}", cours.norm(t))) if len(w) >= 5 and w not in VIDES_ENONCE}


cours = module("cours")
legi = module("legifrance")

DOMAINES = ("legifrance.gouv.fr", "fonction-publique.gouv.fr")
AUTRES_CODES = re.compile(
    r"^.{0,90}?(code (du travail|pénal|de justice administrative|de procédure pénale|des relations entre le public|de la sécurité sociale|"
    r"des pensions|général des collectivités|de l'éducation|des juridictions financières|de la défense|civil|de commerce|de la santé publique)|\b(CJA|CRPA|CGCT|CPP|CSS)\b)",
    re.I | re.S,
)
LIENS_OK = [
    r"^/codes/article_lc/LEGIARTI\d{12}(/\d{4}-\d{2}-\d{2})?/?$",
    r"^/codes/section_lc/LEGITEXT\d{12}/LEGISCTA\d{12}(/\d{4}-\d{2}-\d{2})?/?(#LEGI(ARTI|SCTA)\d{12})?$",
    r"^/codes/texte_lc/LEGITEXT\d{12}(/\d{4}-\d{2}-\d{2})?/?$",
    r"^/codes/id/LEGI(ARTI|SCTA|TEXT)\d{12}(/\d{4}-\d{2}-\d{2})?/?$",
    r"^/loda/id/(JORFTEXT|LEGITEXT)\d{12}(/\d{4}-\d{2}-\d{2})?/?$",
    r"^/loda/article_lc/LEGIARTI\d{12}(/\d{4}-\d{2}-\d{2})?/?$",
    r"^/jorf/id/JORFTEXT\d{12}/?$",
    r"^/jorf/article_jo/JORFARTI\d{12}/?$",
    r"^/(ceta|juri|cons)/id/(CETATEXT|JURITEXT|CONSTEXT)\d{12}/?$",
    r"^/circulaire/id/\d+/?$",
    r"^/download/pdf/circ\?id=\d+$",
]


def main():
    try:  # sortie propre quand la sortie est coupée (`… | head`)
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("fichier")
    ap.add_argument("--mode", choices=["complet", "chrono", "kit", "libre"], default="libre")
    ap.add_argument("--domaine", action="append", default=[], help="domaine supplémentaire expressément autorisé par l'utilisateur")
    ap.add_argument("--ignorer", action="append", default=[], help="article cité à dessein alors qu'il n'existe pas (ex. : --ignorer R532-4, pour une réponse qui le réfute)")
    ap.add_argument("--max-mots", type=int, help="plafond de longueur fixé par l'utilisateur (remplace la borne haute du mode chrono)")
    ap.add_argument("--enonce", help="fichier contenant l'énoncé : avertit quand une section ne reprend aucun de ses éléments")
    ap.add_argument("--niveau-section", type=int, default=2, help="niveau de titre qui délimite une question ou une partie (défaut : 2, « ## »)")
    ap.add_argument("--lignes-par-section", help="longueur attendue par section, en lignes imprimées : « 15 » (plafond) ou « 10-15 » (fourchette)")
    ap.add_argument("--largeur-ligne", type=int, default=95, help="caractères par ligne imprimée pour l'estimation (défaut : 95, Word A4 en police 11)")
    ap.add_argument("--max-mots-par-section", type=int, help="plafond de mots par section")
    ap.add_argument("--ignorer-mention", action="store_true", help="ne pas signaler les textes mentionnés sans lien (mentions de périmètre)")
    args = ap.parse_args()
    texte = open(args.fichier, encoding="utf-8").read()
    plan, pages = cours.charger()
    par_page = {(p["ch"], p["p"]): p for p in pages}
    nb_pages = {c["chapitre"]: c["pages"] for c in plan}
    tout_cours = " ".join(p["n"] for p in pages)
    err, warn, ok = [], [], []

    # 1. Citations du cours ------------------------------------------------------------------
    # Une mention « chapitre N » vaut pour les « p. … » qui la suivent, jusqu'à la mention de chapitre suivante.
    chap_rx = re.compile(r"(?:chapitre|chap\.|ch\.)\s*(\d)\b", re.I)
    page_rx = re.compile(r"\bpp?\.\s*(\d{1,3}(?:\s*(?:-|–|à|,|et)\s*\d{1,3})*)")
    vues, courant = set(), None
    for ligne in texte.split("\n"):
        cites = []
        reperes = sorted([(m.start(), "c", m) for m in chap_rx.finditer(ligne)] + [(m.start(), "p", m) for m in page_rx.finditer(ligne)], key=lambda x: x[0])
        for _, typ, m in reperes:
            if typ == "c":
                courant = int(m.group(1))
                if courant not in nb_pages:
                    err.append(f"Chapitre {courant} cité : le cours n'a que les chapitres 1 à 4.")
                    courant = None
                continue
            if courant is None:
                continue
            ch = courant
            for a, sep, b in re.findall(r"(\d{1,3})(?:\s*(-|–|à)\s*(\d{1,3}))?", m.group(1)):
                a = int(a); b = int(b) if b else a
                if a > b or b > nb_pages[ch] or a < 1:
                    err.append(f"Chapitre {ch}, p. {a}{'-' + str(b) if b != a else ''} : hors du PDF ({nb_pages[ch]} pages).")
                    continue
                cites.append((ch, a, b))
                for p in range(a, b + 1):
                    if (ch, p) in vues:
                        continue
                    vues.add((ch, p))
                    ctx = par_page[(ch, p)]["ctx"]
                    if a == b and "QUIZ" in ctx:
                        warn.append(f"Ch. {ch} p. {p} comporte un quiz : vérifier que l'élément cité est bien du texte de cours et non une proposition de réponse (sinon citer la page d'explication qui suit).")
                    if a == b and "Sommaire" in ctx:
                        warn.append(f"Ch. {ch} p. {p} est le sommaire du chapitre, pas un développement.")
                    if len(par_page[(ch, p)]["txt"]) < 40 and a == b:
                        warn.append(f"Ch. {ch} p. {p} ne contient presque pas de texte : vérifier le numéro de page.")
        # 2. citations littérales attribuées au cours
        if cites:
            for q in re.findall(r"«\s*([^»]{40,})\s*»", ligne):
                if re.search(r"^(Le|La|L'|Les)?\s*[A-ZÉ][^.]{0,90}$", q) and len(q) < 100 and q.strip() in " ".join(c["titre"] for c in plan):
                    continue
                nq = re.sub(r"\s+", " ", cours.norm(q)).strip(" .…")
                morceaux = [x.strip() for x in re.split(r"\[\.\.\.\]|\(\.\.\.\)|…", nq) if len(x.strip()) > 15]
                zone = " ".join(re.sub(r"\s+", " ", par_page[(ch, p)]["n"]) for ch, a, b in cites for p in range(max(1, a - 1), min(nb_pages[ch], b + 1) + 1))
                if all(m_ in zone for m_ in morceaux):
                    continue
                partout = re.sub(r"\s+", " ", tout_cours)
                if all(m_ in partout for m_ in morceaux):
                    warn.append(f"Citation présente dans le cours mais pas aux pages indiquées : « {q[:70]}… » — corriger la page.")
                else:
                    err.append(f"Citation attribuée au cours mais introuvable dans le cours : « {q[:80]}… » — reformuler sans guillemets ou recopier le texte exact.")
    if vues:
        ok.append(f"{len(vues)} page(s) du cours citée(s), toutes existantes : " + ", ".join(f"ch.{c} p.{p}" for c, p in sorted(vues)[:40]) + ("…" if len(vues) > 40 else ""))
    else:
        warn.append("Aucune référence au cours INSP (chapitre + page) : le cours est la source prioritaire.")

    # 3. Articles du CGFP ---------------------------------------------------------------------
    tab = legi.table()
    absents, presents = set(), set()
    nom_code = AUTRES_CODES.pattern[len("^.{0,90}?("):-1]
    for m in re.finditer(r"\b([LRD])\.?\s?(\d{3}-\d+(?:-\d+)*)\b", texte):
        # le code est nommé juste après le numéro (« L521-1 du code de justice administrative »)
        if re.match(r"^(?:\s*(?:et suivants|et s\.|à [LRD]\.?\s?[\d-]+|et [LRD]\.?\s?[\d-]+))?\s*,?\s*(?:du|de la|des)?\s*(?:" + nom_code + ")", texte[m.end(): m.end() + 110], re.I):
            continue
        # ou juste avant, dans la même proposition (« code du travail L4121-1 »)
        avant = re.split(r"[;.(\n]", texte[max(0, m.start() - 110): m.start()].replace(". ", "§ ").replace("§", ";"))[-1]
        codes = list(re.finditer(r"CGFP|code g[ée]n[ée]ral de la fonction publique|" + nom_code, avant, re.I))
        if codes and not re.match(r"CGFP|code g[ée]n[ée]ral de la fonction publique", codes[-1].group(0), re.I):
            continue
        num = m.group(1) + m.group(2)
        k = legi.cle(num)
        if any(t[3][0] == k[0] and t[3] <= k <= t[4] for t in tab):
            presents.add(num)
        else:
            absents.add(num)
    ignores = {x.upper().replace(".", "").replace(" ", "") for x in args.ignorer}
    for a in sorted(absents):
        if a in ignores:
            ok.append(f"Article {a} : absent du CGFP, cité à dessein (--ignorer).")
            continue
        err.append(f"Article {a} : n'existe pas dans le CGFP (table du {legi.DATE_TABLE}). S'il relève d'un autre code, nommer ce code juste après le numéro ; sinon corriger.")
    if presents:
        ok.append(f"{len(presents)} article(s) du CGFP cité(s), tous présents au sommaire du code (le contenu reste à avoir été lu).")

    # 4. Liens --------------------------------------------------------------------------------
    urls = set(re.findall(r"https?://[^\s)\]>\"']+", texte))
    n_legi = 0
    for u in sorted(urls):
        u = u.rstrip(".,;")
        m = re.match(r"https?://([^/]+)(/.*)?$", u)
        dom, chemin = m.group(1).lower(), m.group(2) or "/"
        if not any(dom == d or dom.endswith("." + d) for d in DOMAINES + tuple(args.domaine)):
            err.append(f"Lien hors des sources autorisées (cours INSP, Légifrance, fonction-publique.gouv.fr) : {u}")
            continue
        if "legifrance" not in dom:
            continue
        n_legi += 1
        if "…" in u or re.search(r"X{2,}|\.\.\.", u):
            err.append(f"Lien Légifrance incomplet (identifiant à compléter) : {u}")
        elif chemin.startswith("/search"):
            warn.append(f"Lien de recherche Légifrance, pas un lien direct vers le texte : {u}")
        elif re.search(r"[?&](query|fonds|searchField|page)=", chemin):
            warn.append(f"Lien Légifrance contenant des paramètres de recherche à retirer : {u}")
        elif not any(re.match(rx, chemin.split("?anchor")[0]) for rx in LIENS_OK):
            warn.append(f"Forme de lien Légifrance inhabituelle, à rouvrir pour vérifier : {u}")
    if n_legi:
        ok.append(f"{n_legi} lien(s) Légifrance.")
    # Identifiant LEGIARTI rapproché du numéro d'article affiché dans le libellé du lien
    ids = table_articles()
    par_id = {v: k for k, v in ids.items()}
    n_ctrl = 0
    for lib, u in re.findall(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", texte):
        nums = {a + b for a, b in re.findall(r"\b([LR])\.?\s?(\d{3}-\d+(?:-\d+)*)\b", lib)}
        i = re.search(r"LEGIARTI\d{12}", u)
        if len(nums) != 1 or not i or "/codes/" not in u:
            continue
        num, idf = nums.pop(), i.group(0)
        if num in ids and ids[num] != idf:
            err.append(f"Lien [{lib}] : {idf} n'est pas l'identifiant de {num} ({ids[num]}, data/cgfp_articles.tsv)" + (f" ; c'est celui de {par_id[idf]}." if idf in par_id else "."))
        elif idf in par_id and par_id[idf] != num:
            err.append(f"Lien [{lib}] : {idf} est l'identifiant de {par_id[idf]}, pas de {num}.")
        elif num in ids:
            n_ctrl += 1
    if n_ctrl:
        ok.append(f"{n_ctrl} lien(s) d'article du CGFP rapproché(s) de la table des identifiants relevés.")
    # Articles du CGFP cités mais liés nulle part (une source par affirmation, au même endroit)
    lies = {a + b for lib, _ in re.findall(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", texte) for a, b in re.findall(r"\b([LR])\.?\s?(\d{3}-\d+(?:-\d+)*)\b", lib)}
    lies |= {a + b for l in texte.split("\n") if "http" in l for a, b in re.findall(r"\b([LR])\.?\s?(\d{3}-\d+(?:-\d+)*)\b", l)}
    cites = {a + b for l in texte.split("\n") if not PERIMETRE.search(l) and not l.lstrip().startswith("#") for a, b in re.findall(r"\b([LR])\.?\s?(\d{3}-\d+(?:-\d+)*)\b", l)}
    non_lies = sorted((cites & presents) - lies)
    if non_lies and not args.ignorer_mention:
        warn.append(f"Article(s) du CGFP cité(s) sans lien nulle part dans la réponse : {', '.join(non_lies)} (lien direct au moins une fois, ou --ignorer-mention pour une simple mention de périmètre).")
    sans_lien = [l.strip()[:110] for l in texte.split("\n") if re.search(r"L[ée]gifrance", l) and re.search(r"\b(article|art\.|décret|loi|n°)\b", l, re.I) and "http" not in l and not l.lstrip().startswith(("#", "|")) and not PERIMETRE.search(l)]
    for l in ([] if args.ignorer_mention else sans_lien[:8]):
        warn.append(f"Référence Légifrance sans lien sur la ligne : « {l}… »")
    if re.search(r"non v[ée]rifi[ée]", texte, re.I):
        ok.append("La réponse signale au moins un point non vérifié (transparence conservée).")

    # 5. Mentions à compléter -------------------------------------------------------------------
    for motif, msg in [(r"\bp\.\s*X+\b", "numéro de page « XX »"), (r"article\s+X+\b", "numéro d'article « XX »"), (r"\[lien[^\]]*\](?!\()", "« [lien] » sans adresse"), (r"\[COLLER ICI", "énoncé non collé"), (r"TODO|À COMPLÉTER", "mention à compléter")]:
        if re.search(motif, texte):
            err.append(f"Mention laissée en blanc : {msg}.")

    # 6. Format -------------------------------------------------------------------------------
    mots = len(re.findall(r"\b[\wÀ-ÿ'’-]+\b", re.sub(r"https?://\S+", "", texte)))
    if args.mode == "complet":
        for num, nom in [("I", "Diagnostic"), ("II", "Cadre juridique"), ("III", "solutions"), ("IV", "Plan d'action"), ("V", "Recommandation")]:
            if not re.search(rf"^#+\s*{num}\s*[.—–-]", texte, re.M):
                err.append(f"Partie {num} ({nom}) absente ou non titrée « {num}. … ».")
        if not re.search(r"^\|.*\|.*\|.*\|\s*$", texte, re.M):
            err.append("Tableau récapitulatif final (enjeu / réponse / sources) absent.")
        if not re.search(r"synth[èe]se", texte, re.I):
            warn.append("Pas de synthèse finale des décisions essentielles.")
        for mot, quoi in [(r"imm[ée]diat", "mesures immédiates"), (r"court terme", "court terme"), (r"moyen terme", "moyen terme")]:
            if not re.search(mot, texte, re.I):
                warn.append(f"Plan d'action : horizon « {quoi} » non repéré.")
        if not re.search(r"(à vérifier|informations? manquantes?|éléments? manquants?)", texte, re.I):
            warn.append("Aucune mention des informations manquantes ou à vérifier dans le diagnostic.")
        if not re.search(r"(analyse personnelle|déduction|proposition managériale|\bAnalyse\s*:)", texte, re.I):
            warn.append("Aucune affirmation n'est signalée comme déduction ou proposition managériale : vérifier que la provenance de chaque affirmation est distinguée.")
    if args.mode == "chrono":
        haut = args.max_mots or 800
        bas = min(500, haut - 150)
        (ok if bas <= mots <= haut else err).append(f"Longueur : {mots} mots (attendu : {bas} à {haut}).")
    elif args.max_mots:
        (ok if mots <= args.max_mots else err).append(f"Longueur : {mots} mots (plafond demandé : {args.max_mots}).")
    else:
        ok.append(f"Longueur : {mots} mots.")
    if re.search(r"d[ée]cret\s+n", texte, re.I) or "/loda/" in texte:
        ok.append("Rappel : les numéros d'articles de décrets et les identifiants des liens ne sont pas contrôlables hors ligne ; ils doivent tous provenir d'une page ouverte.")

    if args.mode == "kit":
        questions = [(t, c) for t, c in sections(texte, args.niveau_section) if not SECTIONS_ANNEXES.search(t)]
        if not questions:
            err.append(f"Mode kit : aucune question repérée (titres de niveau {args.niveau_section}, « {'#' * args.niveau_section} Question 1 … »).")
        for t, c in questions:
            for bloc, rx in [("Dans la situation", r"dans la situation"), ("Règles", r"r[èe]gles?|cadre juridique|droit applicable"), ("Options", r"options?|pistes?|choix [àa] (faire|trancher)")]:
                if not re.search(r"^\s*(?:[-*]\s*)?(?:\*\*|#+\s*)?" + rx, c, re.I | re.M):
                    err.append(f"Kit, « {t[:50]} » : bloc « {bloc} » absent.")
            if not re.search(r"qui d[ée]cide", c, re.I):
                warn.append(f"Kit, « {t[:50]} » : pas de bloc « Qui décide, qui propose » (compétence de l'autorité).")
            if re.search(r"\bje (d[ée]cide|recommande|retiens)\b|recommandation (finale)?\s*:", c, re.I):
                warn.append(f"Kit, « {t[:50]} » : une recommandation apparaît, alors que le kit présente les options sans trancher (sauf demande expresse).")
        if not re.search(r"^#+\s*.*(r[ée]f[ée]rences|sources)", texte, re.I | re.M):
            warn.append("Kit : pas de table des références (Légifrance, cours) en fin de document.")
        if args.lignes_par_section:
            ok.append("Support Word : remplir avec `remplir_docx.py … --sans-liens`, sinon chaque adresse écrite en entier allonge la question (l'estimation ci-dessous ne compte pas les adresses).")
    if args.enonce or args.lignes_par_section or args.max_mots_par_section:
        parts = [(t, c) for t, c in sections(texte, args.niveau_section) if not SECTIONS_ANNEXES.search(t)]
        if not parts:
            warn.append(f"Contrôles par section : aucune section de niveau {args.niveau_section} repérée.")
        vocab = vocabulaire(open(args.enonce, encoding="utf-8").read()) if args.enonce else set()
        bas = haut = None
        if args.lignes_par_section:
            m = re.fullmatch(r"\s*(\d+)\s*(?:-\s*(\d+))?\s*", args.lignes_par_section)
            if not m:
                sys.exit("--lignes-par-section : « 15 » ou « 10-15 ».")
            bas, haut = (int(m.group(1)), int(m.group(2))) if m.group(2) else (None, int(m.group(1)))
        for t, c in parts:
            if vocab:
                communs = vocab & vocabulaire(c)
                if not communs:
                    warn.append(f"« {t[:50]} » ne reprend aucun élément de l'énoncé : ancrer la réponse dans les faits (bloc « Dans la situation »).")
            if haut:
                n = lignes_imprimees(c, args.largeur_ligne)
                if n > haut or (bas and n < bas):
                    err.append(f"« {t[:50]} » : environ {n} lignes (attendu : {str(bas) + ' à ' if bas else 'au plus '}{haut}).")
                else:
                    ok.append(f"« {t[:50]} » : environ {n} lignes.")
            if args.max_mots_par_section:
                n = len(re.findall(r"\b[\wÀ-ÿ'’-]+\b", re.sub(r"https?://\S+", "", c)))
                (ok if n <= args.max_mots_par_section else err).append(f"« {t[:50]} » : {n} mots (plafond : {args.max_mots_par_section}).")
        if haut:
            ok.append(f"Lignes estimées à {args.largeur_ligne} caractères par ligne (puces : 5 de moins) ; vérifier dans le document final.")

    for x in ok:
        print("✓", x)
    for x in dict.fromkeys(warn):
        print("!", x)
    for x in dict.fromkeys(err):
        print("✗", x)
    print(f"\n{len(set(err))} erreur(s), {len(set(warn))} avertissement(s).")
    sys.exit(1 if err else 0)


if __name__ == "__main__":
    main()
