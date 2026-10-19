# Texte du cours INSP — à générer vous-même

Ce dossier doit contenir `chapitre-1.md` à `chapitre-4.md`, le texte du cours INSP page par page.
Ce texte appartient à l'INSP : il **n'est pas fourni** dans le catalogue public. Chaque élève le
génère à partir de ses propres PDF du cours, pour un usage personnel de révision.

## Générer les fichiers

1. Placez les quatre PDF du cours dans un dossier (par exemple `Cours/`). Leur nom doit commencer
   par « Chapitre 1 », « Chapitre 2 », etc.
2. Depuis le dossier de la compétence, lancez :

   ```bash
   uv run --with pymupdf python scripts/construire_cours.py /chemin/vers/Cours
   ```

   Le script crée les quatre fichiers ici et met à jour `data/plan_cours.json` et
   `references/plan-cours.md`.
3. Vérifiez : `python3 scripts/cours.py citation 1 9` doit renvoyer une citation du chapitre 1.

## Sans les fichiers

La compétence fonctionne quand même, avec Légifrance et le portail de la fonction publique. Elle
vous signale alors que le cours manque et ne cite aucune page. Vous pouvez aussi joindre les PDF
à la conversation.

Ne publiez pas les fichiers générés et ne les partagez pas.
