# 📦 Préparer les fichiers d'une skill

[← Tous les tutoriels](README.md)

**Une skill comprend un dossier, pas seulement un fichier.** Gardez ses documents de référence
avec ses instructions : ils font partie de la méthode.

## 1. Télécharger le bon fichier

| Skill | Téléchargement | Dossier à récupérer après décompression |
|:---|:---|:---|
| Légistique française | [⬇ ZIP de la dernière version](https://github.com/kilianvivien/skill-legistique-fr/releases/latest/download/legistique-fr.zip) | `legistique-fr` |
| Factiva Research | [⬇ ZIP de la version fournie par l'auteur](https://raw.githubusercontent.com/kilianvivien/insp-skills-ia/main/downloads/factiva-research-v3.zip) | `factiva-research` |

Le ZIP regroupe plusieurs fichiers en un seul téléchargement. Choisissez ici **ZIP**, plutôt que
`.skill`, pour suivre les mêmes étapes sur les quatre outils. Ne changez pas simplement l'extension
d'un fichier pour tenter de le rendre compatible.

## 2. Ouvrir l'archive

- **Sur Mac :** double-cliquez sur le ZIP dans Téléchargements. Finder affiche le contenu extrait.
- **Sur Windows :** clic droit sur le ZIP → **Extraire tout**. Ouvrez le dossier obtenu.
- **Sur Linux :** ouvrez le ZIP avec le gestionnaire d'archives et choisissez **Extraire**.

Le logiciel de décompression peut ajouter un dossier portant le nom de l'archive. Ouvrez-le si
nécessaire : le dossier à installer est celui dans lequel vous voyez directement `SKILL.md`.

## 3. Vérifier que vous avez tous les éléments

Factiva Research doit présenter **exactement ces quatre fichiers** issus de l'archive :

```text
factiva-research/
├── SKILL.md
├── references/
│   ├── syntax.md
│   └── workflow.md
└── agents/
    └── openai.yaml
```

`SKILL.md` contient les instructions principales. `syntax.md` décrit les règles des recherches
Factiva ; `workflow.md` décrit la méthode de recherche. `openai.yaml` fournit des informations
d'interface pour les outils qui les prennent en charge. Conservez-les ensemble.

Légistique française contient davantage de références. **Copiez tout le dossier `legistique-fr`,
y compris ses sous-dossiers et leurs fichiers.** L'arborescence ci-dessous est un aperçu :

```text
legistique-fr/
├── SKILL.md
├── references/
│   └── … toutes les fiches fournies
└── … autres fichiers et sous-dossiers fournis
```

Ces structures ont été contrôlées sur Factiva v3 et Légistique v0.5.1 le 8 octobre 2026. Une prochaine
version peut ajouter des fichiers : gardez toujours l'ensemble du dossier téléchargé.

## 4. Choisir ce que vous allez importer

| Votre destination | Ce que vous utilisez |
|:---|:---|
| Claude | Un ZIP contenant **un seul dossier de skill complet**. |
| Gemini avec le menu Compétences | Le dossier complet ; c'est la méthode conseillée ici pour conserver les références. |
| Mistral Vibe dans le terminal | Le dossier complet **décompressé**, copié sur votre ordinateur. |
| ChatGPT avec le menu Skills | Le fichier accepté par son importateur ; voir le guide pour les limites documentées. |
| ChatGPT sans Skills / Gemini sans Compétences | Les instructions et les documents utiles à adapter dans un Projet ou un Gem. |

## 5. Si vous devez refaire un ZIP

Le ZIP de Légistique v0.5.1 contient aussi un `README.md` d'installation à côté du dossier
`legistique-fr`. Pour un import qui demande un seul dossier, créez un nouveau ZIP contenant
**uniquement `legistique-fr`**. Factiva v3 contient déjà un seul dossier.

1. Repérez le dossier dont le premier niveau contient `SKILL.md`.
2. Cliquez droit sur **ce dossier**, sans sélectionner seulement son contenu.
3. Sur Mac, choisissez **Compresser**. Sur Windows, choisissez **Compresser dans un fichier ZIP**
   ou **Envoyer vers → Dossier compressé**, selon votre version.
4. Ouvrez le nouveau ZIP pour vérifier : vous devez voir le dossier de la skill, puis `SKILL.md`
   et ses sous-dossiers à l'intérieur.

La [documentation Claude](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)
demande cette structure avec un dossier de skill à la racine de l'archive.

## Les erreurs à éviter

```text
CORRECT : factiva-research/SKILL.md
CORRECT : factiva-research/references/syntax.md

INCORRECT : factiva-research/factiva-research/SKILL.md
INCORRECT : SKILL.md isolé, sans les références
INCORRECT : tous les fichiers déplacés dans un seul dossier sans sous-dossiers
```

Ne renommez pas les documents de référence. Un renvoi vers `references/syntax.md` suppose que
le fichier reste dans `references/`, à côté du fichier principal dans la structure ci-dessus.

[ChatGPT](chatgpt.md) · [Claude](claude.md) · [Gemini](gemini.md) · [Mistral Vibe](mistral-vibe.md)
