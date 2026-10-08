# 🧭 Installer une skill, pas à pas

**Choisissez votre outil et suivez le guide correspondant.** Chaque guide explique quoi télécharger,
où le placer, comment vérifier l'installation et quoi faire si une option manque.

**Documentation officielle consultée le 8 octobre 2026.** Les comptes, menus et possibilités évoluent.
Les procédures ci-dessous sont vérifiées dans les sources citées et sur les fichiers du catalogue ;
elles n'ont pas été testées avec tous les abonnements ni tous les comptes institutionnels.

## Quel guide choisir ?

| Votre outil | La méthode | Le point à vérifier | Tutoriel |
|:---|:---|:---|:---|
| **ChatGPT** | Import depuis la page Skills si votre compte le permet ; sinon, adaptation dans un Projet. | L'accès aux skills et à leur import dépend du compte et de l'espace utilisé. | [Suivre le guide](chatgpt.md) |
| **Claude** | Importer le ZIP dans la rubrique Skills, puis activer la skill. | L'exécution de code doit être activée ; des restrictions peuvent venir de l'organisation. | [Suivre le guide](claude.md) |
| **Gemini** | Importer un dossier complet dans Compétences, lorsque ce menu est disponible. | Déploiement progressif sur les comptes personnels ; un compte scolaire peut encore proposer uniquement les Gems. | [Suivre le guide](gemini.md) |
| **Mistral Vibe — terminal** | Décompresser le ZIP et copier le **dossier entier** dans le répertoire de skills. | Conserver `SKILL.md` **et tous ses sous-dossiers**, à leur place. | [Suivre le guide](mistral-vibe.md) |

Les conditions ChatGPT, Claude et Gemini proviennent respectivement de leurs aides officielles :
[OpenAI](https://help.openai.com/en/articles/20001066-skills-in-chatgpt),
[Anthropic](https://support.claude.com/en/articles/12512180-use-skills-in-claude) et
[Google](https://support.google.com/gemini/answer/17094296?hl=fr).
Pour Vibe, la méthode vise le [CLI de Vibe Code](https://docs.mistral.ai/vibe/code/cli/skills).

## Avant de commencer

👉 **[Préparer les fichiers : ZIP, dossier, SKILL.md et références](preparer-les-fichiers.md)**

Ce guide commun montre le contenu exact de Factiva Research et explique comment reconnaître
le dossier de Légistique française. Il est particulièrement utile si vous n'avez jamais installé
de skill.

## Trois choses différentes

- **Installer une skill** : votre assistant reconnaît un ensemble d'instructions et de fichiers comme un outil réutilisable.
- **Adapter une méthode dans un Projet ou un Gem** : vous ajoutez des consignes et des documents à un espace de travail. Cette solution peut être utile, mais ne reproduit pas nécessairement toute la skill.
- **Donner des capacités à l'assistant** : naviguer sur un site connecté, exécuter un programme ou accéder à des fichiers demande des outils et des autorisations supplémentaires. Une skill ne les fournit pas à elle seule.

**Pour Factiva Research :** commencez par demander une formule de recherche à copier-coller.
L'installation ne connecte pas votre compte Factiva et ne donne pas accès aux articles. La recherche
automatique exige aussi un navigateur contrôlable et une session Factiva déjà connectée.

## Comment savoir si cela fonctionne ?

Ne vous contentez pas d'une réponse « la skill est installée ». Vérifiez sa présence dans la liste
de l'outil, puis demandez un essai qui utilise une référence fournie. Chaque tutoriel propose un test.

## Si votre écran diffère du guide

Notez votre outil, votre type de compte, la date et le message affiché, puis
[signalez le problème](https://github.com/kilianvivien/insp-skills-ia/issues/new).
Les noms anglais des principaux boutons sont indiqués pour faciliter la comparaison.

[← Revenir au catalogue](../README.md)
