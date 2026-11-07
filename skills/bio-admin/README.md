# 👤 Biographies administratives

**Rédiger une note biographique sourcée, au format Word, pour préparer un entretien ou une visite.**

Créée par [Kilian Vivien](https://github.com/kilianvivien), cette skill aide un agent IA à rechercher,
vérifier et rédiger des biographies en français pour tout service de l’administration : préfecture,
cabinet ministériel, administration centrale, collectivité ou opérateur.

**[⬇ Télécharger Biographies administratives — ZIP](https://raw.githubusercontent.com/kilianvivien/insp-skills-ia/main/downloads/bio-admin-v1.zip)** · **[⬇ .skill pour Claude](https://raw.githubusercontent.com/kilianvivien/insp-skills-ia/main/downloads/bio-admin-v1.skill)**

[Installation](#installation) · [Exemples](#exemples-de-demandes) · [Instructions](SKILL.md)

## Ce qu’elle fait

- Identifier la personne et lever les homonymies par la fonction ou la ville.
- Choisir les sources selon le profil : Journal officiel pour un agent public, sites des assemblées
  pour un parlementaire, site de l’entreprise pour un dirigeant, langue du pays pour une personnalité étrangère.
- Rédiger un récit chronologique de 20 à 30 lignes, en prose continue, avec les intitulés officiels de l’époque.
- Recouper les faits essentiels (naissance, formation, nominations, fonction actuelle) avec une seconde source.
- Produire un document .docx mis en forme (Times New Roman, A4), avec une ligne des sources.

## Installation

1. **[Téléchargez la skill au format ZIP](https://raw.githubusercontent.com/kilianvivien/insp-skills-ia/main/downloads/bio-admin-v1.zip)**, ou au **[format .skill](https://raw.githubusercontent.com/kilianvivien/insp-skills-ia/main/downloads/bio-admin-v1.skill)** pour l’importer directement dans Claude.
2. Choisissez votre tutoriel : **[ChatGPT](../../tutoriels/chatgpt.md)** · **[Claude](../../tutoriels/claude.md)** · **[Gemini](../../tutoriels/gemini.md)** · **[Mistral Vibe](../../tutoriels/mistral-vibe.md)**.
3. Suivez sa méthode : import d’archive, import de dossier ou adaptation selon les fonctions de votre compte.

Le dossier contient un seul fichier, `SKILL.md`. Pour fonctionner pleinement, l’assistant doit
pouvoir **chercher sur le web** et **créer un fichier Word** (dans Claude, la skill s’appuie sur la
skill docx intégrée). Sans ces fonctions, il peut seulement rédiger le texte à partir des éléments
que vous fournissez.

## Exemples de demandes

> Fais-moi une bio de la préfète de la Somme pour l’entretien de lundi.

> Prépare les biographies des trois participants à la réunion, à partir du programme joint.

> Qui est le président de la chambre de commerce et d’industrie de Lyon ? Fais-en une fiche bio.

## Compétences travaillées

Rechercher dans les sources officielles (Journal officiel, organigrammes, sites des assemblées),
hiérarchiser et recouper les informations, distinguer corps, grade et fonction, rédiger dans le
style administratif.

## Limites et attribution

Une biographie générée peut contenir une date erronée, une fonction dépassée ou une confusion
entre homonymes : relisez-la et vérifiez les faits essentiels avant de la diffuser. Pour une
personne peu exposée, la skill produit un texte plus court plutôt que de combler par des suppositions.
Respectez les règles de votre service sur les données personnelles.

La skill mentionne `diplo-bio`, une variante pour le réseau diplomatique, qui n’est pas publiée ici.
L’archive ne contient pas de licence explicite ; la licence MIT de la documentation du catalogue
ne lui est pas appliquée automatiquement.
