# 📰 Factiva Research

**Transformer une question de recherche en recherche de presse reproductible.**

Créée par [Kilian Vivien](https://github.com/kilianvivien), cette skill aide un agent IA à préparer,
exécuter lorsque les outils le permettent, affiner et documenter des recherches avancées dans Factiva.
Elle est publiée ici à partir de l’archive `factiva-research-v3.zip` fournie par l’auteur.

[Lire les instructions](SKILL.md) · [Syntaxe des requêtes](references/syntax.md) · [Méthode de recherche](references/workflow.md)

## Ce qu’elle fait

- Décomposer une question en concepts, entités, synonymes, langues et période.
- Construire une requête booléenne avec des contraintes de proximité et de champs adaptées.
- Affiner une recherche à partir de la pertinence des résultats et des faux positifs.
- Consigner la requête, les filtres et les étapes pour rendre la recherche reproductible.
- Présenter les résultats avec leurs sources et leurs limites lorsque la recherche a pu être exécutée.

## Deux modes d’utilisation

| Mode | Conditions | Résultat attendu |
|---|---|---|
| **Recherche dans Factiva** | Un accès Factiva valide, une session déjà authentifiée et un agent capable de contrôler le navigateur. | Recherche exécutée, requête et filtres documentés, synthèse sourcée des résultats consultés. |
| **Requête à copier-coller** | Vous demandez uniquement une requête, ou le contrôle du navigateur est indisponible. | Une requête booléenne à utiliser vous-même dans Factiva, sans prétendre avoir consulté des résultats. |

La skill ne fournit pas d’abonnement Factiva. La consultation des articles nécessite votre propre
accès. Les possibilités de contrôle du navigateur dépendent de votre agent et de ses outils.

## Installation

1. Téléchargez [le dépôt au format ZIP](https://github.com/kilianvivien/insp-skills-ia/archive/refs/heads/main.zip).
2. Décompressez-le et récupérez uniquement le dossier `skills/factiva-research/`.
3. Copiez ce dossier dans le répertoire de skills indiqué par la documentation de votre agent.
4. Vérifiez que `factiva-research/SKILL.md`, `references/` et `agents/` ont conservé leur structure.

Le dossier contient des instructions Markdown, deux fiches de référence et une configuration
d’interface dans `agents/openai.yaml`. Il ne contient aucun script ni dépendance à installer.
La présence de cette configuration ne garantit pas la compatibilité avec tous les agents :
vérifiez que votre outil prend en charge les skills et, pour l’exécution, le contrôle du navigateur.

## Exemples de demandes

> Utilise la skill factiva-research pour préparer une requête sur la couverture de la rénovation
> énergétique des bâtiments publics dans la presse française, du 1er au 30 septembre 2026.
> Je veux uniquement la requête à copier-coller dans Factiva.

> Dans ma session Factiva déjà connectée, recherche la couverture d’une réforme sur la période
> indiquée. Documente la requête, les filtres et les affinements, puis synthétise les articles
> pertinents effectivement consultés.

Ces exemples illustrent les usages ; ils ne constituent pas des recherches exécutées.

## Compétences travaillées

Cadrer une recherche documentaire, construire une équation de recherche, équilibrer précision et
couverture, évaluer les sources, distinguer les résultats observés des hypothèses et documenter
une méthode reproductible.

## Limites et attribution

La skill cible Factiva et ne remplace pas une recherche web générale. Les synthèses doivent porter
sur les résultats effectivement consultés. Elle prévoit le respect des conditions de l’accès
Factiva et n’autorise pas la redistribution d’articles complets.

L’archive fournie ne contient pas de licence explicite. Le référencement et la publication ne lui
attribuent pas automatiquement la licence MIT de la documentation du catalogue.

Les quatre fichiers issus de l’archive sont conservés sans modification :
`SKILL.md`, `references/syntax.md`, `references/workflow.md` et `agents/openai.yaml`.
