# 🟠 Installer une skill dans Claude

[← Tous les tutoriels](README.md) · [Préparer les fichiers](preparer-les-fichiers.md)

**Vérifié dans la documentation officielle le 8 octobre 2026.** Méthode pour
[Claude sur le Web](https://claude.ai), sans installer Claude Code.

## 1. Vérifier les conditions

L'aide actuelle annonce les skills sur Free, Pro, Max, Team et Enterprise. Elles nécessitent
l'activation de **l'exécution de code et de la création de fichiers**. Une organisation peut
restreindre cette fonction. [Source : utiliser les skills dans Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

## 2. Préparer le ZIP complet

Téléchargez la skill depuis le catalogue. Le ZIP à importer doit contenir **un dossier de skill**,
avec `SKILL.md` et toutes ses références à l'intérieur.

- **Factiva v3 :** l'archive fournie a déjà cette structure.
- **Légistique v0.5.1 :** décompressez l'archive, puis recompressez uniquement le dossier
  `legistique-fr`. Le `README.md` d'installation situé à côté doit rester hors du nouveau ZIP.

Le [guide de préparation](preparer-les-fichiers.md#5-si-vous-devez-refaire-un-zip) détaille les clics
sur Mac et Windows. Cette organisation de l'archive est demandée par
[la documentation Claude](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills).

## 3. Importer et activer

1. Dans Claude, ouvrez **Paramètres → Capacités / Settings → Capabilities**.
2. Activez **Exécution de code et création de fichiers / Code execution and file creation**.
3. Ouvrez **Personnaliser → Skills / Customize → Skills**.
4. Cliquez sur **+**, puis **Créer une skill / + Create skill**.
5. Choisissez **Importer une skill / Upload a skill** et sélectionnez le ZIP préparé.
6. Attendez son apparition dans la liste, puis mettez son interrupteur sur **activé**.

Dans un compte Team ou Enterprise, si ces réglages sont indisponibles, un responsable doit vérifier
la politique dans **Organization settings → Plugins & skills**. Les libellés traduits peuvent varier ;
le chemin anglais est celui de [l'aide officielle](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

## 4. Faire un essai qui utilise un fichier de référence

Ouvrez une nouvelle conversation et écrivez :

> Utilise la skill factiva-research installée. Lis references/syntax.md et indique son titre.
> Puis prépare une formule de recherche en français sur la rénovation énergétique des bâtiments
> publics, du 1er au 30 septembre 2026. Je veux la formule à copier-coller dans Factiva.

Vérifiez que la skill est activée dans la liste et que la réponse s'appuie sur le fichier fourni.
Le titre à retrouver est **Factiva Advanced Search Syntax**. Comparez aussi la langue et la période
avec votre demande. Ce test ne demande pas d'accès à votre abonnement Factiva.

Pour tester la légistique, utilisez un court projet fictif et demandez des corrections avec les
fiches du Guide citées. Comparez ces renvois aux documents fournis avec la skill.

## 5. Si l'installation échoue

| Problème | Solution |
|:---|:---|
| Skills absent | Vérifier les capacités et, dans une organisation, la politique de l'administrateur. |
| « SKILL.md introuvable » ou archive mal formée | Refaire le ZIP à partir du dossier entier, sans couche de dossier supplémentaire. |
| Skill visible mais pas utilisée | L'activer, démarrer une nouvelle conversation et la demander par son nom. |
| Fichier de référence absent | Refaire l'archive avec tous les sous-dossiers ; ne charger pas uniquement `SKILL.md`. |
| Le message refuse la longueur de `description` | Appliquer la correction facultative ci-dessous à une copie locale. |

<details>
<summary>Si le message indique explicitement « description trop longue »</summary>

La documentation Web de création mentionne une description de 200 caractères maximum, tandis
que celle de la plateforme Agent Skills indique 1 024 caractères. Les descriptions des archives
contrôlées dépassent 200 caractères. **Ne les modifiez que si votre import signale ce problème.**
[Aide Web](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills) ·
[Format Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview).

Faites une copie du dossier. Dans son `SKILL.md`, remplacez uniquement le champ `description`
situé entre les deux lignes `---` par une des lignes suivantes. Si l'ancien champ occupe plusieurs
lignes indentées, remplacez-les toutes. Conservez les autres champs et toutes les instructions.

Pour la légistique :

```yaml
description: Rédige, corrige et analyse les textes normatifs français selon le Guide de légistique.
```

Pour Factiva :

```yaml
description: Prépare et affine les recherches avancées dans Factiva ; fournit une requête à copier-coller quand le navigateur ne peut pas être contrôlé.
```

Enregistrez en texte brut sous le nom exact `SKILL.md`, puis refaites le ZIP du dossier. Cette
adaptation du descriptif peut modifier le déclenchement automatique : demandez la skill par son nom.

</details>

## Les limites à connaître

L'import dans Claude n'installe pas la skill dans tous les autres logiciels. Les fichiers locaux
de votre ordinateur et votre connexion Factiva ne sont pas automatiquement accessibles à Claude
sur le Web. Pour Factiva, commencez donc par le mode « formule à copier-coller ».

L'activation d'une skill et de l'exécution de code ne constitue pas, à elle seule, une autorisation
ou un outil pour contrôler votre navigateur personnel.
