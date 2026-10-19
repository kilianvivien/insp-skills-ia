#!/usr/bin/env python3
"""Recherche dans le cours INSP (4 chapitres, texte page par page).

    python3 scripts/cours.py plan [chapitre]            plan : cas, leçons, plages de pages
    python3 scripts/cours.py chercher mots clés ...      pages les plus pertinentes + extraits
    python3 scripts/cours.py page 3 21-24                texte intégral des pages (à lire avant de citer ; liste : 19,27-29)
    python3 scripts/cours.py citation 3 24               référence prête à coller dans la réponse
    python3 scripts/cours.py enonces [-c 3] [--complet]  les énoncés de cas du cours (modèles pour l'entraînement)

Options de `chercher` : -c N (limiter à un chapitre), -n N (nombre de résultats, défaut 10),
--ou (un seul terme suffit ; par défaut les pages contenant tous les termes passent en tête),
"expression entre guillemets" pour une expression exacte.
La recherche ignore la casse et les accents ; « L. 530-1 » et « L530-1 » sont équivalents.
"""
import argparse
import json
import math
import os
import re
import sys
import unicodedata

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIDES = {"le", "la", "les", "de", "des", "du", "un", "une", "et", "en", "au", "aux", "d", "l", "a", "à", "pour", "par", "sur", "dans", "que", "qui", "est", "ce"}


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = s.replace("’", "'").replace("œ", "oe")
    # « L. 530-1 », « L 530-1 » -> « l530-1 »
    return re.sub(r"\b([lrd])\.?\s?(\d{2,3}-\d)", r"\1\2", s)


def charger():
    plan = json.load(open(os.path.join(RACINE, "data", "plan_cours.json"), encoding="utf-8"))
    pages = []
    for c in plan:
        chemin = os.path.join(RACINE, "references", "cours", f"chapitre-{c['chapitre']}.md")
        if not os.path.exists(chemin):
            sys.exit(f"ERREUR : {chemin} introuvable. Le texte du cours n'est pas fourni avec la compétence ; "
                     "le générer depuis les PDF du cours : uv run --with pymupdf python scripts/construire_cours.py /chemin/vers/Cours "
                     "(voir references/cours/README.md).")
        t = open(chemin, encoding="utf-8").read()
        for num, ctx, txt in re.findall(r"\n## p\. (\d+)\n<!-- (.*?) -->\n(.*?)(?=\n\n## p\. |\Z)", t, re.S):
            pages.append({"ch": c["chapitre"], "p": int(num), "ctx": ctx, "txt": txt, "n": norm(txt)})
    return plan, pages


def lecon_de(plan, ch, p):
    c = next(x for x in plan if x["chapitre"] == ch)
    l = next((x for x in c["lecons"] if x["debut"] <= p <= x["fin"]), None)
    cas = next((k["titre"] for k in c["cas"] if l and k["cas"] == l["cas"]), None)
    return c, l, cas


def citation(plan, ch, p):
    c, l, cas = lecon_de(plan, ch, p)
    if not 1 <= p <= c["pages"]:
        return f"ERREUR : le chapitre {ch} compte {c['pages']} pages ; la page {p} n'existe pas."
    if not l:
        return f"INSP, chapitre {ch} « {c['titre']} », sommaire, p. {p} du PDF"
    partie = f"cas {l['cas']} « {cas} », " if cas else ""
    return f"INSP, chapitre {ch} « {c['titre']} », {partie}leçon {l['lecon']} « {l['titre']} », p. {p} du PDF"


def cmd_plan(plan, args):
    for c in plan:
        if args.chapitre and c["chapitre"] != args.chapitre:
            continue
        print(f"\nCHAPITRE {c['chapitre']} — {c['titre']} ({c['pages']} p.)")
        courant = None
        for l in c["lecons"]:
            if l["cas"] != courant:
                courant = l["cas"]
                t = next((k["titre"] for k in c["cas"] if k["cas"] == courant), "Annexes")
                print(f"  Cas {courant} — {t}" if courant else "  Annexes")
            print(f"    L{l['lecon']:<2} p. {l['debut']}-{l['fin']:<4} {l['titre']}")


def cmd_chercher(plan, pages, args):
    termes = [norm(t) for t in args.termes if norm(t) not in VIDES]
    if not termes:
        sys.exit("Aucun terme de recherche utile.")
    corpus = [p for p in pages if not args.chapitre or p["ch"] == args.chapitre]
    df = {t: sum(1 for p in corpus if t in p["n"]) for t in termes}
    res = []
    for p in corpus:
        hits = {t: p["n"].count(t) for t in termes}
        presents = [t for t in termes if hits[t]]
        if not presents or (not args.ou and len(termes) > 1 and len(presents) < max(1, len(termes) - 1)):
            continue
        score = sum(min(hits[t], 4) * math.log(1 + len(corpus) / (1 + df[t])) for t in presents)
        score *= 1 + len(presents) / len(termes)
        if len(presents) == len(termes):
            score *= 1.5
        if "QUIZ" in p["ctx"]:
            score *= 0.6  # les pages de quiz ne portent pas la règle
        if "Énoncé du cas" in p["ctx"]:
            score *= 0.8
        res.append((score, p, presents))
    res.sort(key=lambda x: -x[0])
    if not res:
        print("Aucune page ne correspond. Essayer des synonymes, moins de termes, ou --ou.")
        print("Si le cours ne traite pas le point : le dire dans la réponse plutôt que d'extrapoler.")
        return
    print(f"{len(res)} page(s) trouvée(s) ; {min(len(res), args.n)} affichée(s). Lire la page entière (commande `page`) avant de citer.\n")
    for score, p, presents in res[: args.n]:
        manquants = [t for t in termes if t not in presents]
        print(f"■ Ch. {p['ch']} p. {p['p']} — {p['ctx']}" + (f"   [absent : {', '.join(manquants)}]" if manquants else ""))
        lignes = p["txt"].split("\n")
        gardees = [i for i, l in enumerate(lignes) if any(t in norm(l) for t in termes)]
        montre = sorted({j for i in gardees[:4] for j in (i - 1, i, i + 1) if 0 <= j < len(lignes)})
        for j in montre:
            print("    " + lignes[j][:220])
        print()


def cmd_page(plan, pages, args):
    voulues = set()
    c = next((x for x in plan if x["chapitre"] == args.chapitre), None)
    for morceau in args.pages.replace(" ", "").split(","):
        m = re.match(r"^(\d+)(?:-(\d+))?$", morceau)
        if not m:
            sys.exit("Format attendu : 24, 21-24 ou une liste : 19,27-29,163")
        a, b = int(m.group(1)), int(m.group(2) or m.group(1))
        if not c or a < 1 or b > c["pages"] or a > b:
            sys.exit(f"Plage invalide : le chapitre {args.chapitre} va de la p. 1 à la p. {c['pages'] if c else '?'}.")
        voulues |= set(range(a, b + 1))
    if len(voulues) > 41:
        sys.exit("Trop de pages (40 au plus par appel).")
    for p in pages:
        if p["ch"] == args.chapitre and p["p"] in voulues:
            print(f"\n===== {citation(plan, p['ch'], p['p'])} =====")
            if "QUIZ" in p["ctx"]:
                print("[QUIZ : les lignes ci-dessous sont des propositions de réponse, pas des affirmations du cours]")
            print(p["txt"])


def cmd_enonces(plan, pages, args):
    for c in plan:
        if args.chapitre and c["chapitre"] != args.chapitre:
            continue
        for l in c["lecons"]:
            if not l["titre"].startswith("Énoncé"):
                continue
            cas = next(k["titre"] for k in c["cas"] if k["cas"] == l["cas"])
            txt = " ".join(p["txt"].replace("\n", " ") for p in pages if p["ch"] == c["chapitre"] and l["debut"] <= p["p"] <= l["fin"])
            txt = re.sub(r"\[page sans texte[^\]]*\]", "", txt)
            txt = re.sub(r"^Leçon \d+ sur \d+ Contexte partie \d+ ", "", txt).replace("Transcription ", "", 1)
            print(f"\n■ Ch. {c['chapitre']} cas {l['cas']} — {cas} (énoncé p. {l['debut']}-{l['fin']})")
            print("  " + (txt if args.complet else txt[:600] + ("…" if len(txt) > 600 else "")))


def main():
    try:  # sortie propre quand la sortie est coupée (`… | head`)
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    a = sp.add_parser("plan"); a.add_argument("chapitre", nargs="?", type=int)
    a = sp.add_parser("chercher"); a.add_argument("termes", nargs="+"); a.add_argument("-c", "--chapitre", type=int)
    a.add_argument("-n", type=int, default=10); a.add_argument("--ou", action="store_true")
    a = sp.add_parser("page"); a.add_argument("chapitre", type=int); a.add_argument("pages")
    a = sp.add_parser("citation"); a.add_argument("chapitre", type=int); a.add_argument("page", type=int)
    a = sp.add_parser("enonces"); a.add_argument("--complet", action="store_true"); a.add_argument("-c", "--chapitre", type=int)
    args = ap.parse_args()
    plan, pages = charger()
    if args.cmd == "plan":
        cmd_plan(plan, args)
    elif args.cmd == "chercher":
        cmd_chercher(plan, pages, args)
    elif args.cmd == "page":
        cmd_page(plan, pages, args)
    elif args.cmd == "citation":
        print(citation(plan, args.chapitre, args.page))
    elif args.cmd == "enonces":
        cmd_enonces(plan, pages, args)


if __name__ == "__main__":
    main()
