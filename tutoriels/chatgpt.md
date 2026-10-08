# 🟢 Utiliser une skill avec ChatGPT

[← Tous les tutoriels](README.md) · [Préparer les fichiers](preparer-les-fichiers.md)

**Vérifié dans la documentation officielle le 8 octobre 2026.** Ce guide concerne ChatGPT sur le
Web. Les skills locales de Codex et l'application de bureau ont des règles distinctes.

## 1. Vérifier si votre compte propose l'import

Ouvrez [ChatGPT](https://chatgpt.com), puis cherchez **Plugins → Skills** dans la barre latérale.
L'aide officielle cite les comptes Business, Enterprise, Healthcare et Edu éligibles, sous réserve
des réglages de l'espace. Elle ne garantit pas cet import pour chaque compte personnel Free, Plus
ou Pro. Si le menu manque, passez à la méthode Projet ci-dessous.
[Source : disponibilité des skills](https://help.openai.com/en/articles/20001066-skills-in-chatgpt).

## 2. Si le menu Skills est disponible

1. Ouvrez **Plugins → Skills**.
2. Cliquez sur **Créer / Create** → **Importer depuis votre ordinateur / Upload from your computer**.
3. Sélectionnez le fichier de skill accepté par le sélecteur. Le catalogue fournit des ZIP :
   essayez l'archive contenant un seul dossier complet, préparée avec le guide commun.
4. Attendez l'analyse. Si le statut est **Needs Review**, lisez la demande de vérification ;
   si c'est **Blocked**, la skill ne peut pas être utilisée.
5. Vérifiez qu'elle figure dans **Installed**. Si l'écran propose encore **Install**, terminez
   cette étape. L'import est terminé quand elle apparaît installée, sans blocage.

Le chemin des menus et les statuts sont décrits dans
[l'aide officielle](https://help.openai.com/en/articles/20001066-skills-in-chatgpt).

**Limite de vérification :** cette page ne donne pas la liste des extensions acceptées par
l'importateur. Le partage de skills sous forme de ZIP est décrit ailleurs par OpenAI, mais cela
ne prouve pas que tout ZIP externe sera accepté sur votre compte. Si le fichier est refusé,
conservez le message et utilisez la méthode Projet ; ne rebaptisez pas le ZIP en `.skill`.
[Source : partage d'une skill en ZIP](https://help.openai.com/en/articles/20001518-using-the-data-plugin-in-chatgpt-work-and-codex).

## 3. Si vous n'avez pas Skills : utiliser un Projet

**C'est une adaptation de la méthode, pas une installation native de la skill.**

1. Décompressez le ZIP de Factiva Research sur votre ordinateur.
2. Dans ChatGPT, cliquez sur **Nouveau projet / New project** et nommez-le « Recherche Factiva ».
3. Ajoutez comme fichiers du projet **`SKILL.md`, `syntax.md` et `workflow.md`**, récupérés dans
   le dossier de la skill. Le fichier `openai.yaml` n'est pas nécessaire pour cette adaptation.
4. Ouvrez le menu **••• → Paramètres du projet / Project settings** et ajoutez les consignes ci-dessous.
5. Démarrez une nouvelle conversation **à l'intérieur de ce projet**.

```text
Pour mes demandes Factiva, commence par lire SKILL.md et syntax.md dans les fichiers du projet.
Le renvoi references/syntax.md correspond ici au fichier joint syntax.md.
Le renvoi references/workflow.md correspond au fichier joint workflow.md.
Lis workflow.md si nous examinons des résultats ou préparons une recherche à exécuter.
Si tu ne peux pas lire un fichier, indique-le avant de poursuivre.
Sans accès à ma session Factiva, fournis uniquement une formule à copier-coller.
N'affirme pas avoir consulté des articles que tu n'as pas ouverts.
```

Les projets acceptent des fichiers et des instructions propres au projet ; le nombre de fichiers
dépend du compte. [Source : Projets dans ChatGPT](https://help.openai.com/en/articles/10169521-projects-in-chatgpt).

Pour la légistique, créez un autre projet. Joignez `SKILL.md` et les fiches nécessaires à votre
exercice en conservant une correspondance explicite entre leurs noms et les renvois du texte.
Si les quotas empêchent d'ajouter toutes les références, annoncez que l'adaptation est partielle :
ne considérez pas la skill complète comme installée.

## 4. Vérifier la lecture des références

Dans un compte avec skills, tapez `@` et sélectionnez la skill si elle est proposée. ChatGPT
documente cette sélection ; le `$` concerne notamment Codex.
[Source : Skills & Plugins](https://learn.chatgpt.com/docs/skills-and-plugins).

Puis demandez, ou envoyez directement dans le Projet Factiva :

> Lis le fichier syntax.md fourni avec Factiva Research. Quel est son titre et quelle différence
> fait-il entre « and » et « or » ? Indique le fichier utilisé. Si tu ne peux pas le lire, dis-le.

Comparez avec le fichier sur votre ordinateur, dont le titre est **Factiva Advanced Search Syntax**.
Une réponse générale sans référence au fichier ne suffit pas à vérifier l'accès.

## Si cela bloque

| Ce que vous voyez | Ce qu'il faut faire |
|:---|:---|
| Skills absent | Vérifier l'espace sélectionné et ses droits ; utiliser un Projet si disponible. |
| Import désactivé dans un espace Edu | Demander à l'administrateur si l'import de skills est autorisé. |
| ZIP refusé | Vérifier sa structure, conserver l'erreur, puis utiliser l'adaptation dans un Projet. |
| Une référence n'est pas retrouvée | Vérifier qu'elle a été jointe et que son nom correspond aux consignes. |
| Pas d'accès à Factiva | Demander une formule à copier-coller, puis exécuter vous-même la recherche. |

Une skill ne garantit ni l'exécution de ses scripts ni l'accès à votre navigateur. Vérifiez les
capacités disponibles pour la conversation utilisée.
