# 🟣 Installer tous les fichiers d'une skill dans Mistral Vibe

[← Tous les tutoriels](README.md) · [Préparer les fichiers](preparer-les-fichiers.md)

**Vérifié le 8 octobre 2026.** Ce guide concerne **Vibe Code dans le terminal**, aussi appelé
Vibe CLI. Les interfaces Vibe Work et Vibe sur le Web ont leur propre fonctionnement.

> **Le geste essentiel : copier le dossier entier.**
> Vibe CLI découvre des dossiers contenant `SKILL.md`. Il ne faut pas déposer le ZIP ou le
> fichier `.skill` dans son répertoire de skills, ni joindre les références une par une au chat.
> Décompressez d'abord le ZIP, puis copiez le dossier avec tous ses sous-dossiers.

La [documentation Mistral](https://docs.mistral.ai/vibe/code/cli/skills) décrit cette découverte
par dossiers. Les manipulations de fichiers ci-dessous l'appliquent aux archives de notre catalogue.

## 1. Vérifier que Vibe fonctionne déjà

Ouvrez votre terminal et saisissez :

```sh
vibe --version
```

Vous devez obtenir un numéro de version. Si la commande est introuvable, suivez d'abord
[l'installation officielle de Vibe](https://docs.mistral.ai/getting-started/quickstarts/vibe-code/install-cli).
Sur Mac et Linux, Mistral fournit un installateur ; pour une installation manuelle, Python 3.12+
et `uv tool install mistral-vibe` sont documentés, y compris sur Windows. Au premier lancement,
suivez l'assistant de connexion ou de clé API ; les limites d'usage dépendent de votre accès.
[Source : installation et configuration](https://docs.mistral.ai/vibe/code/cli/install-setup).

## 2. Récupérer le dossier complet

1. [Téléchargez Factiva Research en ZIP](https://raw.githubusercontent.com/kilianvivien/insp-skills-ia/main/downloads/factiva-research-v3.zip).
2. Décompressez l'archive dans Téléchargements.
3. Ouvrez les éventuels dossiers intermédiaires, jusqu'à voir le dossier **`factiva-research`**
   avec **`SKILL.md` directement à l'intérieur**.
4. Vérifiez les quatre fichiers présentés ci-dessous. Gardez ce dossier ouvert.

```text
factiva-research/
├── SKILL.md
├── references/
│   ├── syntax.md
│   └── workflow.md
└── agents/
    └── openai.yaml
```

**Ne déplacez pas `syntax.md` ni `workflow.md` hors de `references/`.** Quand les instructions
renvoient à `references/syntax.md`, Vibe doit pouvoir retrouver ce chemin dans le dossier de skill.
Conservez aussi `agents/`, même si ce fichier n'est pas nécessaire à toutes les interfaces.

## 3. Copier le dossier dans le répertoire de Vibe

Le dossier personnel `~/.vibe/skills/` rend les skills disponibles dans vos différents projets.
Le signe `~` désigne votre dossier utilisateur. Nous utilisons l'emplacement par défaut de Vibe.

### Sur Mac : une commande, puis Finder

1. Dans Terminal, copiez cette commande et appuyez sur Entrée :

   ```sh
   mkdir -p ~/.vibe/skills
   ```

2. Dans Finder, choisissez **Aller → Aller au dossier** (`⌘ Maj G`).
3. Collez **`~/.vibe/skills`** et validez.
4. Dans votre fenêtre Téléchargements, sélectionnez le dossier complet **`factiva-research`**
   et copiez-le (`⌘ C`).
5. Revenez dans la fenêtre **skills** et collez (`⌘ V`). Vous collez **un dossier**, pas un ZIP
   et pas seulement le fichier `SKILL.md`.

### Sur Windows : PowerShell, puis l'Explorateur

Pour Vibe installé directement sous Windows, ouvrez PowerShell et exécutez :

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.vibe\skills" | Out-Null
```

Dans la barre d'adresse de l'Explorateur, collez **`%USERPROFILE%\.vibe\skills`**.
Copiez-y le dossier complet `factiva-research` avec `Ctrl C`, puis `Ctrl V`.

**Si vous lancez Vibe dans WSL :** utilisez les dossiers de cet environnement Linux et la méthode
Linux ci-dessous. Le dossier utilisateur Windows peut être différent de celui lu par Vibe dans WSL.

### Sur Linux

Dans le terminal :

```sh
mkdir -p ~/.vibe/skills
```

Dans le gestionnaire de fichiers, ouvrez votre dossier personnel, affichez les fichiers cachés,
puis ouvrez `.vibe/skills`. Copiez-y le dossier complet `factiva-research`.

**Si le dossier existe déjà :** fermez Vibe et sauvegardez l'ancienne copie hors de `skills/`
avant de la remplacer. Évitez de fusionner deux versions ou de conserver deux copies du même nom.

## 4. Vérifier les fichiers à leur emplacement final

Après la copie, vous devez avoir :

```text
~/.vibe/skills/
└── factiva-research/
    ├── SKILL.md
    ├── references/
    │   ├── syntax.md
    │   └── workflow.md
    └── agents/
        └── openai.yaml
```

Ces chemins sont incorrects :

```text
~/.vibe/skills/SKILL.md
~/.vibe/skills/factiva-research-v3.zip
~/.vibe/skills/factiva-research/factiva-research/SKILL.md
```

Sur Mac ou Linux, contrôlez les références avec :

```sh
ls ~/.vibe/skills/factiva-research/references
```

Le résultat doit contenir **`syntax.md`** et **`workflow.md`**. Sous Windows, ouvrez le sous-dossier
correspondant dans l'Explorateur. La présence des fichiers vérifie la copie ; le test suivant
vérifie que Vibe les lit.

## 5. Relancer Vibe et tester les références

Fermez la session en cours et relancez `vibe`. Tapez `/` : cherchez `factiva-research` dans les
propositions. Le nom vient du champ `name` dans `SKILL.md`, pas du nom du ZIP.
La version actuelle permet l'appel utilisateur par défaut, sauf restriction de la skill.
[Source : système de skills](https://github.com/mistralai/mistral-vibe/blob/main/README.md#skills-system).

Sélectionnez la skill, ou écrivez cette demande dans Vibe :

```text
Utilise la skill factiva-research installée.
Sans ouvrir Factiva, lis réellement references/syntax.md et references/workflow.md
dans son dossier. Donne le titre de chaque document et indique les chemins lus.
Si un fichier est inaccessible, signale-le au lieu de répondre de mémoire.
```

Vérifiez les opérations de lecture affichées par Vibe. Si une autorisation de lecture de ces
fichiers est demandée, contrôlez le chemin avant de l'accepter. La réponse doit retrouver :

- `syntax.md` : **Factiva Advanced Search Syntax** ;
- `workflow.md` : **Factiva Execution and Refinement Workflow**.

**Une réponse « je connais la skill » ne suffit pas.** Cherchez une lecture effective des deux
fichiers dans le déroulé de la session, puis comparez les titres aux documents téléchargés.

## 6. Faire la même chose avec Légistique française

Décompressez [son ZIP](https://github.com/kilianvivien/skill-legistique-fr/releases/latest/download/legistique-fr.zip),
puis copiez **tout le dossier `legistique-fr`** dans `.vibe/skills`. Ne copiez pas le `README.md`
d'installation placé à côté, et ne choisissez pas seulement quelques fiches de `references/`.

Le chemin final est **`~/.vibe/skills/legistique-fr/SKILL.md`**. Ses autres fichiers restent
à leur place, dans `legistique-fr/`. Relancez Vibe et cherchez `/legistique-fr`.

## Si cela ne fonctionne pas

| Problème | Vérification |
|:---|:---|
| La skill n'apparaît pas | Vérifier le dossier, le nom `SKILL.md`, les messages de démarrage et relancer Vibe. |
| La skill apparaît mais une référence manque | Ouvrir son dossier final : les sous-dossiers doivent être identiques à ceux de l'archive. |
| Vibe demande une permission de lecture | Examiner le chemin ; une skill globale peut se trouver hors du dossier de travail. |
| Vous utilisez `.vibe/skills` dans un projet | Le projet doit être reconnu comme dossier de confiance. La copie globale évite cette condition de découverte locale. |
| Vous avez configuré `VIBE_HOME` | Utiliser le répertoire de skills de ce Vibe personnel, qui peut différer de `~/.vibe/skills`. |
| La skill est masquée par la configuration | Vérifier `enabled_skills` et `disabled_skills` ; ne pas modifier ces filtres sans comprendre leur usage. |

Mistral distingue la confiance accordée au projet et les permissions des outils. Copier une skill
ne supprime pas ces contrôles. [Source : confiance et permissions](https://docs.mistral.ai/vibe/code/safety-approvals-permissions).
Les répertoires et filtres sont décrits dans [la documentation des skills](https://docs.mistral.ai/vibe/code/cli/skills).

## Limite importante pour Factiva

Vibe peut lire la méthode et préparer une formule de recherche. Pour agir dans Factiva, il lui
faut aussi un outil de contrôle du navigateur et votre session connectée. Copier le dossier
n'ajoute aucun de ces accès : utilisez le mode « formule à copier-coller » si ces capacités manquent.
