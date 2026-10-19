# 🏛️ Cas pratiques RH (INSP)

**Résoudre, corriger et travailler les cas pratiques de management et de ressources humaines de la fonction publique.**

Créée par [Kilian Vivien](https://github.com/kilianvivien) à partir d'un prompt de **Faustin Chabagno**,
cette skill aide un agent IA à traiter une situation RH comme l'attend un correcteur de l'INSP :
juridiquement exacte, sourcée à la page du cours et à l'article près, ancrée dans les faits de
l'énoncé, et décidée par la bonne autorité.

**[⬇ Télécharger Cas pratiques RH — ZIP](https://raw.githubusercontent.com/kilianvivien/insp-skills-ia/main/downloads/cas-pratique-rh-v2.1.zip)**

[Installation](#installation) · [Le cours INSP](#le-cours-insp-à-ajouter-vous-même) · [Exemples](#exemples-de-demandes) · [Instructions](SKILL.md)

## Ce qu'elle fait

- Trouver le « cas jumeau » du cours INSP et en reprendre le raisonnement, cité à la page.
- Vérifier et dater chaque texte sur Légifrance (CGFP, décrets, jurisprudence), avec un lien direct.
- Signaler les écarts entre le cours et le droit en vigueur (textes abrogés, modifiés ou codifiés).
- Identifier qui décide et qui propose, avant toute recommandation.
- Contrôler la réponse avant remise : pages inexistantes, articles absents du code, liens incomplets, longueur.

## Neuf façons de l'utiliser

| Mode | Ce que vous obtenez |
|---|---|
| **Analyse complète** | Réponse en cinq parties avec tableau récapitulatif. |
| **Chrono** | Version de 500 à 800 mots, pour l'entraînement en temps limité. |
| **Oral** | Plan d'exposé et questions probables du jury. |
| **Correction de copie** | Erreurs, oublis, points réussis, priorités et passages réécrits. |
| **Entraînement** | Cas inédits, puis correction. |
| **Fiche de révision** | Synthèse d'un thème (télétravail, discipline, etc.). |
| **Vérification** | Ce que dit un article du CGFP, et si le cours est à jour. |
| **Pièces opérationnelles** | Note, courrier, trame d'entretien, calendrier. |
| **Kit de réponse** | Règles sourcées et options sans recommandation, éventuellement dans le support Word de l'école. |

## Les trois sources, dans cet ordre

1. **Le cours INSP** (quatre chapitres, 26 cas) : le référentiel du correcteur.
2. **Légifrance** : la source de vérité juridique.
3. **fonction-publique.gouv.fr** (DGAFP) : la doctrine de l'administration.

Aucune autre source n'est utilisée sans votre autorisation.

## Le cours INSP, à ajouter vous-même

Le texte du cours appartient à l'INSP : **il n'est pas inclus dans le ZIP**. La skill contient le plan
du cours et les références juridiques citées par leçon, mais pas son contenu. Pour citer le cours
à la page, générez le texte à partir de vos propres PDF :

```bash
uv run --with pymupdf python scripts/construire_cours.py /chemin/vers/Cours
```

Le détail est dans [references/cours/README.md](references/cours/README.md). Sans le cours, la skill
le dit, travaille avec Légifrance et la DGAFP, et ne cite aucune page. Vous pouvez aussi joindre
les PDF à la conversation.

## Installation

1. **[Téléchargez la skill au format ZIP](https://raw.githubusercontent.com/kilianvivien/insp-skills-ia/main/downloads/cas-pratique-rh-v2.1.zip)**.
2. Choisissez votre tutoriel : **[ChatGPT](../../tutoriels/chatgpt.md)** · **[Claude](../../tutoriels/claude.md)** · **[Gemini](../../tutoriels/gemini.md)** · **[Mistral Vibe](../../tutoriels/mistral-vibe.md)**.
3. Si votre outil le permet, ajoutez le texte du cours (voir ci-dessus).

**Prérequis :** la skill est conçue pour un agent qui peut lancer des scripts Python
(`python3`, sans dépendance ; `uv` pour remplir un fichier Word et générer le cours) et
consulter Légifrance dans un navigateur, comme Claude Code ou Claude avec l'exécution de code.
Dans un assistant sans scripts ni navigateur, la méthode et les gabarits restent utilisables,
mais les vérifications automatiques ne le sont pas.

## Exemples de demandes

> Voici un cas pratique RH, traite-le. [énoncé collé]

> Même cas, version chronométrée de 600 mots.

> Entraîne-moi sur la discipline et la protection fonctionnelle.

> Que dit le CGFP sur le temps partiel de droit ? Le cours est-il à jour ?

Utilisez des cas publics ou fictifs.

## Compétences travaillées

- Qualifier juridiquement une situation de management à partir des faits.
- Identifier l'autorité compétente et la procédure applicable.
- Vérifier un texte et sa version en vigueur sur Légifrance.
- Construire une décision défendable et la rédiger dans un temps limité.

## Contenu

```
cas-pratique-rh/
├── SKILL.md                     instructions principales
├── references/
│   ├── cours/                   texte du cours à générer (non fourni)
│   ├── plan-cours.md            plan et références juridiques citées par leçon
│   ├── themes.md                entrée par thème : cours, mots clés, points d'entrée Légifrance
│   ├── legifrance.md            consulter Légifrance et le portail DGAFP
│   ├── methode.md               raisonnement attendu, réflexes du cours, pièges
│   ├── formats.md               gabarits des neuf modes
│   └── grille-evaluation.md     barème indicatif sur 20
├── scripts/
│   ├── cours.py                 plan, recherche, lecture de pages, citation
│   ├── legifrance.py            adresses exactes des articles, textes et décisions
│   ├── extracteur_legifrance.js à exécuter dans la page Légifrance ouverte
│   ├── verifier_reponse.py      contrôle d'une réponse avant remise
│   ├── delais.py                calcul d'échéances
│   ├── remplir_docx.py          remplit le support Word fourni avec un kit de réponse
│   └── construire_cours.py      génère le texte du cours depuis les PDF
└── data/                        table du CGFP, plan du cours, textes clés
```

## Limites

- Le cours porte sur la **fonction publique de l'État** ; les autres versants sont signalés, pas traités en détail.
- Légifrance bloque souvent les accès automatiques : la consultation passe par le navigateur de l'agent. Une validation anti-robot éventuelle reste à faire par vous.
- Le barème est indicatif : ce n'est pas celui de l'INSP.
- Données juridiques vérifiées le 17/10/2026 (table du CGFP au 13/10/2026). Le droit évolue : vérifiez les textes cités.
- Vérifiez toujours la réponse avant de l'utiliser.

## Versions

- **2.1 (17/10/2026)** — longueur réelle dans le Word (`--sans-liens`), identifiants Légifrance contrôlés, droit de se taire (L532-4, décision n° 2024-1105 QPC), modifications du CGFP programmées au 01/01/2029.
- **2 (17/10/2026)** — mode « Kit de réponse » et remplissage du support Word, bloc « Dans la situation », étape « qui décide, qui propose », consultation de Légifrance par le navigateur, données mises à jour (décret 2026-705, jour de carence).
- **1 (13/10/2026)** — première version, testée sur cinq cas.

## Crédits et licence

- **Prompt d'origine : Faustin Chabagno** (« Prompt d'analyse d'un cas pratique RH — INSP »). La skill en reprend la hiérarchie des sources, l'exigence de provenance, la structure en cinq parties et la variante chronométrée.
- **Cours de référence : INSP.** Son texte reste la propriété de l'INSP et n'est pas rediffusé ici.
- **Sources juridiques :** Légifrance et fonction-publique.gouv.fr (DGAFP).
- Transformation en skill : Kilian Vivien, avec Claude.

Licence : non indiquée. La licence MIT du catalogue ne s'applique pas automatiquement à cette skill.
