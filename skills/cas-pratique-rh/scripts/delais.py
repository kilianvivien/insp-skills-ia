#!/usr/bin/env python3
"""Calcule une échéance à partir d'une date et d'une durée (le script calcule ; il ne connaît aucune règle).

    python3 scripts/delais.py 2026-03-12 2m              deux mois de date à date
    python3 scripts/delais.py 2026-03-12 2m --franc      délai franc : ni le jour de départ ni le jour d'échéance ne comptent
    python3 scripts/delais.py 2026-03-12 15j             quinze jours calendaires
    python3 scripts/delais.py 2026-10-12 3a              trois ans en avant (ex. : faits connus le 12/10/2026, jusqu'à quand agir ?)
    python3 scripts/delais.py 2026-03-12 3a --avant      trois ans en ARRIÈRE (ex. : à partir de quelle date des faits sont-ils trop anciens ?)

Durées : Nj (jours), Ns (semaines), Nm (mois), Na (années). Le script signale si l'échéance tombe un samedi,
un dimanche ou un jour férié et donne alors le premier jour ouvrable suivant (report utile pour les délais de recours).
La durée du délai, son point de départ et l'existence d'un report se justifient par une source (cours, Légifrance).
"""
import argparse
import calendar
import datetime as dt
import re
import sys

JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]


def paques(a):
    g = a % 19; c = a // 100; h = (c - c // 4 - (8 * c + 13) // 25 + 19 * g + 15) % 30
    i = h - (h // 28) * (1 - (h // 28) * (29 // (h + 1)) * ((21 - g) // 11))
    j = (a + a // 4 + i + 2 - c + c // 4) % 7
    l = i - j
    mois = 3 + (l + 40) // 44
    return dt.date(a, mois, l + 28 - 31 * (mois // 4))


def feries(a):
    p = paques(a)
    fixes = [(1, 1), (5, 1), (5, 8), (7, 14), (8, 15), (11, 1), (11, 11), (12, 25)]
    return {dt.date(a, m, j) for m, j in fixes} | {p + dt.timedelta(days=x) for x in (1, 39, 50)}


def ajoute_mois(d, n):
    m = d.month - 1 + n
    a, m = d.year + m // 12, m % 12 + 1
    return dt.date(a, m, min(d.day, calendar.monthrange(a, m)[1]))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("depart"); ap.add_argument("duree")
    ap.add_argument("--franc", action="store_true"); ap.add_argument("--avant", action="store_true")
    args = ap.parse_args()
    try:
        d0 = dt.date.fromisoformat(args.depart)
    except ValueError:
        sys.exit("Date de départ attendue au format AAAA-MM-JJ.")
    m = re.match(r"^(\d+)\s*([jsma])$", args.duree.lower())
    if not m:
        sys.exit("Durée attendue : 15j, 2s, 2m ou 3a.")
    n, u = int(m.group(1)) * (-1 if args.avant else 1), m.group(2)
    d = {"j": lambda: d0 + dt.timedelta(days=n), "s": lambda: d0 + dt.timedelta(weeks=n), "m": lambda: ajoute_mois(d0, n), "a": lambda: ajoute_mois(d0, 12 * n)}[u]()
    if args.franc and not args.avant:
        d += dt.timedelta(days=1)
    print(f"Départ   : {JOURS[d0.weekday()]} {d0.strftime('%d/%m/%Y')}")
    print(f"Échéance : {JOURS[d.weekday()]} {d.strftime('%d/%m/%Y')}" + (" (délai franc : dernier jour utile)" if args.franc else ""))
    r = d
    while r.weekday() >= 5 or r in feries(r.year):
        r += dt.timedelta(days=1)
    if r != d and not args.avant:
        print(f"Ce jour est un samedi, un dimanche ou un jour férié ; premier jour ouvrable suivant : {JOURS[r.weekday()]} {r.strftime('%d/%m/%Y')}")
    auj = dt.date.today()
    print(f"Par rapport à aujourd'hui ({auj.strftime('%d/%m/%Y')}) : " + (f"dans {(d - auj).days} jour(s)" if d >= auj else f"dépassée depuis {(auj - d).days} jour(s)"))


if __name__ == "__main__":
    main()
