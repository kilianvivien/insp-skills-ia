# 🌐 Traduire et mettre en page un PDF

**Traduire un document PDF et produire un PDF propre, avec page de garde et sommaire.**

Créée par [Kilian Vivien](https://github.com/kilianvivien), cette skill guide un agent IA en quatre
phases : conversion du PDF en Markdown, traduction par parties avec un glossaire, ajout d’une page
de garde et d’un sommaire stylé, puis génération du PDF final.

**[⬇ Télécharger Traduction PDF — ZIP](https://raw.githubusercontent.com/kilianvivien/insp-skills-ia/main/downloads/pdf-translate-format-v1.zip)** · **[⬇ .skill pour Claude](https://raw.githubusercontent.com/kilianvivien/insp-skills-ia/main/downloads/pdf-translate-format-v1.skill)**

[Installation](#installation) · [Exemples](#exemples-de-demandes) · [Instructions](SKILL.md)

## Ce qu’elle fait

- Extraire le texte du PDF et retirer les en-têtes répétés et les numéros de page.
- Reconstituer les titres, les paragraphes et le sommaire en Markdown.
- Établir un glossaire (noms propres, sigles, termes récurrents) avant de traduire.
- Traduire par sections de 200 à 300 lignes, en conservant la mise en forme.
- Générer un PDF A4 avec page de garde, sommaire à points de conduite et sauts de page.

## Installation

1. **[Téléchargez la skill au format ZIP](https://raw.githubusercontent.com/kilianvivien/insp-skills-ia/main/downloads/pdf-translate-format-v1.zip)**, ou au **[format .skill](https://raw.githubusercontent.com/kilianvivien/insp-skills-ia/main/downloads/pdf-translate-format-v1.skill)** pour l’importer directement dans Claude.
2. Choisissez votre tutoriel : **[Claude](../../tutoriels/claude.md)** · **[Mistral Vibe](../../tutoriels/mistral-vibe.md)** · [ChatGPT](../../tutoriels/chatgpt.md) · [Gemini](../../tutoriels/gemini.md).
3. Copiez **tout le dossier** `pdf-translate-format/`, avec `SKILL.md`, `scripts/` et `resources/`.

**Prérequis techniques.** Cette skill exécute des commandes : elle demande un agent capable de
lancer Python et Node.js (Claude Code, Claude avec l’exécution de code, Mistral Vibe dans le
terminal…). Il faut `python3` avec `pdfplumber` (`pip install pdfplumber`), `npx` (fourni avec
Node.js) et une connexion internet pendant la génération du PDF (outil `md-to-pdf` et polices Google).
Dans une simple conversation sans exécution de code, elle ne peut pas fonctionner.

Les instructions de la skill sont rédigées en anglais ; vous pouvez lui parler en français.

## Exemples de demandes

> Traduis ce rapport en français et produis un PDF avec page de garde et sommaire : rapport.pdf

> Translate `etude.pdf` into English and generate a formatted PDF.

## Compétences travaillées

Préparer un document pour la traduction, tenir un glossaire terminologique, contrôler la fidélité
d’une traduction et la mise en page d’un document final.

## Limites et attribution

La conversion fonctionne mieux sur des PDF textuels bien structurés ; un PDF scanné, en colonnes
ou très chargé en tableaux demandera des ajustements. Relisez la traduction, en particulier les
termes techniques et juridiques, avant toute diffusion. N’envoyez pas de documents confidentiels
à un outil que votre organisation n’autorise pas.

L’archive ne contient pas de licence explicite ; la licence MIT de la documentation du catalogue
ne lui est pas appliquée automatiquement.
