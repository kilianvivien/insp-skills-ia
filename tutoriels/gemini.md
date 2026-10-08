# 🔵 Installer une compétence dans Gemini

[← Tous les tutoriels](README.md) · [Préparer les fichiers](preparer-les-fichiers.md)

**Vérifié dans la documentation officielle le 8 octobre 2026.** Ce guide concerne
[l'application Gemini sur le Web](https://gemini.google.com), pas Gemini CLI.

## 1. Vérifier le type de compte et le menu

Google déploie les **Compétences / Skills** progressivement : compte personnel, 18 ans minimum
et option **Conserver l'activité** activée. Elles peuvent manquer sur certains comptes ; l'aide
consultée exclut encore les comptes professionnels et scolaires de cette fonction. Les skills
de chat ne nécessitent pas un abonnement Google AI.
[Source : créer et gérer les compétences](https://support.google.com/gemini/answer/17094296?hl=fr).

Si vous utilisez un compte de l'école et voyez seulement **Gems**, suivez l'adaptation plus bas.
Ne changez pas de compte et n'activez pas de réglage contraire aux consignes de votre organisation.

## 2. Si vous voyez Paramètres → Compétences

1. Téléchargez le ZIP de la skill et décompressez-le.
2. Repérez le dossier `factiva-research` ou `legistique-fr`, contenant directement `SKILL.md`.
3. Sur votre ordinateur, ouvrez Gemini → **Paramètres → Compétences / Settings → Skills**.
4. Cliquez sur **Importer / Upload**, puis choisissez le **dossier complet** de la skill.
5. Validez avec **Ouvrir / Open**, examinez la proposition, puis cliquez sur **Créer / Create**.

Google accepte aussi un ZIP ou un `SKILL.md`. Ici, choisissez le dossier complet pour inclure les
références. Le total ne doit pas dépasser **100 Mo** ; les scripts avec accès Internet et certains
fichiers binaires ne sont pas pris en charge. Les références doivent être importées avec la skill.
[Source : exigences d'importation](https://support.google.com/gemini/answer/17094296?hl=fr).

## 3. Vérifier la compétence

Dans un nouveau chat, tapez `/` et sélectionnez la compétence si elle apparaît. Google annonce
un passage prochain à `@` : utilisez le sélecteur proposé par votre interface.
La même aide précise que l'import de fichiers se fait actuellement sur le Web ou l'application Mac.
[Source : transition vers les compétences](https://support.google.com/gemini/answer/18560919?hl=fr).

Demandez ensuite :

> Utilise factiva-research. Lis la référence syntax.md jointe à la compétence et donne son titre.
> Puis prépare une formule en français sur la rénovation énergétique des bâtiments publics,
> du 1er au 30 septembre 2026, à copier-coller dans Factiva.

Le titre à comparer avec votre fichier est **Factiva Advanced Search Syntax**. Vérifiez aussi
la langue et la période. Si Gemini ne peut pas lire la référence, reprenez l'import du dossier
entier ; ne considérez pas un simple acquiescement comme une preuve d'installation complète.

## 4. Si vous voyez seulement Gems

**Un Gem est une adaptation avec instructions et documents, pas l'importation du dossier de skill.**

Pour un premier essai avec Factiva Research :

1. Décompressez son ZIP et ouvrez `SKILL.md` dans un éditeur de texte.
2. Dans Gemini sur ordinateur, ouvrez **Gems → Nouveau Gem**.
3. Donnez-lui le nom « Recherche Factiva ».
4. Dans **Instructions**, copiez le texte de `SKILL.md` situé **après** le deuxième `---`.
5. Ajoutez à la fin ces consignes d'adaptation :

```text
Les documents joints syntax.md et workflow.md correspondent aux renvois
references/syntax.md et references/workflow.md de ces instructions.
Lis syntax.md avant de préparer une formule de recherche.
Sans accès à une session Factiva contrôlable, donne une formule à copier-coller.
Signale tout document que tu ne peux pas lire. Ne présente pas de recherche comme exécutée.
```

6. Dans **Connaissances → Ajouter des fichiers**, joignez `syntax.md` et `workflow.md` depuis
   le dossier `references`. `openai.yaml` n'est pas nécessaire pour cette adaptation.
7. Cliquez sur **Enregistrer**, puis choisissez ce Gem pour discuter et faire le test ci-dessus.

La création d'un Gem et l'ajout de fichiers sont décrits dans
[l'aide officielle](https://support.google.com/gemini/answer/15146780?hl=fr).
Pour la légistique, appliquez la même logique avec ses instructions et les fiches utiles à l'exercice.
Si vous ne pouvez pas joindre toutes les références, l'adaptation reste partielle.

## Limites et dépannage

| Situation | Ce qu'elle signifie / quoi faire |
|:---|:---|
| Compétences absent sur un compte scolaire | L'aide actuelle ne l'y propose pas encore ; vérifier les Gems et les règles de l'école. |
| Seul SKILL.md a été importé | Les références manquent ; réimporter le dossier complet. |
| Import refusé | Vérifier le nom exact `SKILL.md`, les fichiers acceptés et la taille ; garder les sous-dossiers. |
| Vous cherchez l'import sur téléphone | Utiliser le site Web sur ordinateur ou l'application Mac. |
| Vous voulez employer la skill dans Deep Research ou Canvas | Ces fonctions ne sont pas encore compatibles selon l'aide de transition. |

Google annonce la transition des Gems à partir de novembre 2026 pour les comptes personnels,
de mars 2027 pour certaines offres Workspace et de juin 2027 pour Education. Ce sont les dates
annoncées, pas une garantie d'accès immédiat pour chaque compte.
[Source et limites de compatibilité](https://support.google.com/gemini/answer/18560919?hl=fr).

Installer Factiva Research ne donne pas d'accès Factiva et ne fournit pas de contrôle du navigateur.
Le mode « formule à copier-coller » est le premier essai à privilégier.
