# Gabarits de réponse

Sommaire : 0. Le bloc « Dans la situation » (tous les modes) — 1. Analyse complète — 2. Chrono — 3. Oral — 4. Correction de copie — 5. Entraînement — 6. Fiche de révision — 7. Vérification — 8. Pièces opérationnelles — 9. Kit / trame de réponse — 10. Règles communes

## 0. Le bloc « Dans la situation » (obligatoire dans tous les gabarits qui répondent à un énoncé)

Chaque partie ou chaque question commence par ce bloc, avant toute règle :

```markdown
**Dans la situation :** [fait de l'énoncé, avec ses éléments concrets : qui, quoi, quand, combien]
→ [qualification : de quoi ce fait relève en droit] → [enjeu : ce que cela change pour la décision ou pour l'action]
```

Exemple : « **Dans la situation :** Mme D. enchaîne depuis mars des arrêts de deux jours, transmis avec retard → arrêts de courte durée répétés, soumis au jour de carence et désormais au contrôle administratif → levier de contrôle et d'entretien avant toute idée de discipline. »

Une règle qui ne s'applique à aucun fait ainsi posé sort de la réponse. Contrôle : `verifier_reponse.py --enonce enonce.md`.

## 1. Analyse complète (mode par défaut)

Structure imposée (c'est celle que l'évaluation attend ; le script de contrôle la vérifie). Longueur indicative : 1 500 à 2 500 mots, davantage seulement si le cas comporte plusieurs situations.

```markdown
# [Titre du cas en une ligne]

> Sources : cours INSP (chapitres …) ; Légifrance, versions en vigueur au JJ/MM/AAAA ; [DGAFP le cas échéant].
> [S'il y a lieu : « Écart cours / droit en vigueur signalé au point II.x » ou « Droit non vérifié sur Légifrance »]

**En bref :** [deux ou trois phrases : la décision et sa raison principale]

## I. Diagnostic de la situation
**Dans la situation :** … → … → …
- Faits essentiels (établis / rapportés ou allégués / à vérifier)
- Problèmes posés : juridiques, RH, humains, organisationnels, managériaux
- Enjeux et risques, hiérarchisés (du plus urgent au moins urgent)
- Informations manquantes qui pourraient modifier la décision

## II. Cadre juridique et réglementaire
Par question de droit : le fait en cause (« Dans la situation »), la règle, son application aux faits, puis les sources.
- Droits et obligations de l'agent ; droits et obligations de l'administration
- Marges de manœuvre du manager (ce qu'il décide seul, propose, ne peut pas faire) : pour chaque action, **qui décide, qui propose** (`methode.md`, section 2 bis)
- [Écart éventuel entre le cours et le droit en vigueur : les deux formulations, celle qui s'applique]

## III. Analyse des solutions possibles
Par option : contenu, avantages, limites et risques, statut (obligatoire / autorisé / interdit), autorité qui décide et acteurs à associer.

## IV. Plan d'action opérationnel
- **Immédiatement :** …
- **À court terme :** …
- **À moyen terme :** …
Pour chaque mesure : qui agit, dans quel ordre, avec quelle précaution.

## V. Recommandation finale
Ce que je décide en tant que [fonction], justifié sur les plans juridique, humain et managérial.

**Synthèse :** [les décisions essentielles, en quatre à six lignes]

| Question ou enjeu | Réponse ou action recommandée | Sources (INSP : chapitre et page ; Légifrance : article et lien) |
|---|---|---|
| … | … | … |
```

Forme des références, à placer au plus près de l'affirmation qu'elles fondent :

> **Source prioritaire :** INSP, chapitre 3, « Droit et sanctions », p. 9 du PDF (article L530-1 du CGFP).

> **Complément juridique :** Légifrance, code général de la fonction publique, article L530-1, version en vigueur au JJ/MM/AAAA, https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI…

> **Analyse :** [déduction ou proposition managériale], fondée sur INSP, chapitre …, p. … [et/ou référence Légifrance].

Dans le tableau final, une ligne par question de l'énoncé et par décision importante ; la colonne des sources reprend les mêmes références, en abrégé.

## 2. Chrono (500 à 800 mots)

Pour une évaluation en temps limité, ou sur demande de synthèse. Même plan, resserré ; les décisions, leurs justifications et les références restent. Les liens ne comptent pas dans la longueur.

```markdown
# [Titre]
**Décision :** [une ou deux phrases]
## I. Diagnostic            (≈ 100 mots, ouvert par « Dans la situation » : faits décisifs, problème central, risque principal, ce qui manque)
## II. Cadre juridique      (≈ 180 mots : les trois ou quatre règles qui décident, chacune avec sa source)
## III. Options             (≈ 120 mots : deux ou trois options, une ligne de pour et de contre)
## IV. Plan d'action        (≈ 150 mots : immédiat / court terme / moyen terme, qui fait quoi)
## V. Recommandation        (≈ 100 mots : la décision et ses trois justifications)
| Enjeu | Action | Sources |   (trois à cinq lignes)
```

Couper d'abord les rappels généraux, les options non retenues peu plausibles et les redites entre parties ; ne jamais couper une source ni la décision. Contrôler avec `--mode chrono`.

## 3. Oral

```markdown
# [Titre] — exposé de N minutes
**Accroche (30 s) :** la situation en deux phrases et l'annonce de la décision.
**Plan annoncé :** deux ou trois temps.
## 1. [Temps 1] (x min)   idées, règle clé avec sa source, phrase à dire telle quelle
## 2. [Temps 2] (x min)
## 3. [Temps 3] (x min)
**Conclusion (30 s) :** la décision, sa justification, le point de vigilance.
## Questions probables du jury
- Question → éléments de réponse (avec source) → piège à éviter
## À avoir en tête   (chiffres, délais, articles : chacun avec sa source)
```

Privilégier les questions qui déplacent le cas : « et si l'agent était contractuel ? », « et si les faits dataient de quatre ans ? », « votre directeur refuse, que faites-vous ? », « le syndicat médiatise ? ». Les sources restent écrites dans le support même si elles ne se disent pas toutes à l'oral.

## 4. Correction de copie

L'utilisateur fournit sa copie (et idéalement l'énoncé). Traiter d'abord le cas soi-même (cours, puis Légifrance), puis comparer. Barème : `grille-evaluation.md`.

```markdown
# Correction — [titre du cas]
**Appréciation générale :** [trois lignes : le niveau, la principale qualité, le principal manque]
**Note indicative : X / 20** (détail par critère ci-dessous)
| Critère | Points | Commentaire |
## Erreurs de droit ou de source   (citation de la copie → ce qui est inexact → la règle exacte, avec source)
## Oublis importants               (ce qu'un correcteur attendait, avec la page du cours)
## Ce qui est réussi               (à conserver)
## Trois priorités pour progresser
## Passages réécrits               (les deux ou trois passages les plus faibles, réécrits)
```

Être exact avant d'être bienveillant : une erreur de droit se nomme, source à l'appui. Ne pas reprocher l'absence d'un point que ni l'énoncé ni le cours n'appelaient. Vérifier les pages et les articles cités par la copie (`verifier_reponse.py` sur la copie les contrôle).

## 5. Entraînement

1. Demander ou déduire le thème, le chapitre et le niveau de difficulté ; à défaut, choisir un thème et croiser deux chapitres.
2. Rédiger un **énoncé original** dans l'esprit du cours : 120 à 250 mots, jusqu'à 350 pour un cas difficile ou croisant deux chapitres (`cours.py enonces -c 3` donne les énoncés d'un chapitre comme modèles de ton et de longueur) : une fonction précise, une situation concrète avec deux ou trois difficultés imbriquées, un élément humain, une ou deux questions ouvertes. Ne pas recopier un cas du cours ; faire varier le statut de l'agent, la fonction du décideur, le calendrier, un élément perturbateur (tract, plainte, arrêt de travail, pression hiérarchique). Tout ce qui est nécessaire pour répondre doit se trouver dans le cours ou être vérifiable sur Légifrance.
3. **Prouver que le cas est traitable** avant de l'envoyer : pour chaque difficulté, noter la page du cours qui la couvre (`cours.py chercher`), ou, si le cours est muet, le texte qui la règle, ouvert sur Légifrance. Une difficulté que ni le cours ni un texte vérifié ne permettent de trancher se retire ou se reformule. Garder ces notes (difficultés, pages, textes, pièges voulus) dans `reponses/<sujet>-corrige.md` : c'est la trame de la correction au tour suivant, à ne pas montrer avant que la copie soit rendue.
4. Indiquer le temps conseillé et le format attendu, **sans donner de piste**. Attendre la copie.
5. À réception : corriger (gabarit 4) en repartant de la trame, puis proposer le corrigé complet (gabarit 1).

Si l'utilisateur demande le corrigé d'emblée, le donner. S'il demande une série, varier les thèmes pour couvrir les quatre chapitres.

## 6. Fiche de révision

Une page par thème, faite pour être relue la veille :

```markdown
# [Thème]
**L'essentiel en trois lignes**
## Règles à connaître          (chacune avec sa source ; chiffres et délais vérifiés sur Légifrance, date de version)
## Procédure, pas à pas        (qui, quoi, quand)
## Réflexes managériaux du cours   (avec pages)
## Pièges et confusions fréquentes
## Cas du cours à relire       (chapitre, cas, pages)
## Écarts cours / droit en vigueur constatés   (s'il y en a)
## Trois questions pour s'auto-tester
```

## 7. Vérification

Pour « que dit le CGFP sur… », « cet article est-il à jour ? », « le cours est-il encore exact sur… ? » : réponse courte.

```markdown
**Règle en vigueur au JJ/MM/AAAA :** [énoncé]
**Source :** Légifrance, [texte, article], version en vigueur depuis le …, [lien direct]
**Ce que dit le cours :** INSP, chapitre …, « … », p. … : [formulation du cours]
**Concordance :** conforme / écart : [lequel, depuis quand, conséquence pratique]
```

Si l'article ou le texte cité par l'utilisateur n'existe pas (numéro faux, article non codifié, texte abrogé), l'annoncer en première ligne, puis donner la bonne référence :

```markdown
**La référence est à corriger : [l'article … n'existe pas / est abrogé depuis le …].** [La règle de fond est exacte / inexacte.]
**Pourquoi :** [constat, avec ce que montre le sommaire du code ou la page du texte]
**Règle en vigueur au JJ/MM/AAAA :** [énoncé] — **Source :** [texte, article, version, lien direct]
**Ce que dit le cours :** [page, ou « le cours ne donne pas ce point »]
**Formulation proposée pour la copie :** « … »
**Limites :** [ce qui n'a pas été relu, versant concerné]
```

## 8. Pièces opérationnelles

Sur demande, ou proposées en une ligne après une analyse : note à la hiérarchie, courrier à l'agent (convocation, rappel des obligations, information sur l'ouverture d'une procédure), trame d'entretien, compte rendu d'entretien, calendrier de procédure daté, éléments de langage pour la réunion d'équipe ou les représentants du personnel, fiche de saisine d'un référent ou d'une instance.

- Chaque pièce découle de l'analyse : mêmes faits, même décision, mêmes sources.
- Mettre entre crochets tout ce que l'utilisateur doit compléter : [nom], [date], [service].
- Un courrier à un agent ne contient que des faits établis, les mentions que les textes imposent (vérifiées sur Légifrance : droits de la défense, voies et délais de recours) et aucun jugement de valeur.
- Rappeler en une ligne que la pièce est un projet à faire valider par la DRH ou le service juridique : c'est ce que ferait le cadre lui-même.

## 9. Kit / trame de réponse

Quand l'utilisateur veut **les règles, les références et des options, sans que la réponse tranche**, parce qu'il rédige lui-même sa copie (évaluation à domicile, devoir à rendre, entraînement guidé). Déclencheurs : « kit », « trame », « matériau », « donne-moi les éléments », « je rédigerai moi-même », « ne tranche pas », un support Word à remplir joint à la demande. C'est le seul mode qui ne recommande pas : la décision appartient à l'utilisateur. Si celui-ci demande malgré tout un avis, le donner à part, étiqueté « Analyse ».

Avant d'écrire, relever dans la consigne : la **longueur par question** (« 10 à 15 lignes »), le **support imposé** (fichier `.docx` fourni par l'école), et toute **règle d'usage de l'IA** (charte de l'établissement, déclaration d'usage à joindre).

### Gabarit, par question

```markdown
# Kit de réponse — [intitulé de l'évaluation]

> Sources : cours INSP (chapitres …) ; Légifrance, versions en vigueur au JJ/MM/AAAA. Kit de travail : règles et options, sans recommandation ; la rédaction et les choix appartiennent à l'auteur de la copie.

## Question 1 — [reformulation courte de la question]

**Dans la situation :** [faits de l'énoncé qualifiés : fait → qualification → enjeu ; un ou deux par question]

**Qui décide, qui propose :** [l'autorité compétente pour chaque action envisageable ; ce que la personne placée dans l'énoncé peut faire seule]

**Règles**
- [Règle 1, appliquée au fait] — Légifrance, [texte, article], version en vigueur au JJ/MM/AAAA, [lien direct]
- [Règle 2] — INSP, chapitre …, « … », p. …
- [Écart cours / droit en vigueur, s'il y en a]

**Options à trancher**
- **Option A — [intitulé]** : [contenu] ; pour : … ; contre ou risque : … ; [obligatoire / permis / interdit]
- **Option B — [intitulé]** : …
- [Option C, si elle est réelle]

**Points de vigilance :** [piège, délai, procédure à ne pas oublier ; vocabulaire de l'énoncé à actualiser]  (facultatif quand la longueur est imposée)

## Question 2 — …

## Références
| Texte ou source | Article | Version consultée | Lien |
|---|---|---|---|

## Charte IA   (seulement si la consigne le demande)
[Rappel de la règle d'usage de l'IA de l'établissement, à vérifier dans la consigne ou le règlement, et proposition de mention d'usage à adapter par l'auteur]
```

Règles du mode :

- **Deux ou trois options**, réelles et distinctes, présentées à égalité, sans ordre de préférence ni formule qui tranche (« la meilleure option », « je recommande », « il faut retenir »). Le statut juridique (obligatoire, permis, interdit) reste dit : ce n'est pas trancher, c'est le droit.
- **Respecter la longueur par question** : c'est le texte placé sous chaque question du support qui est mesuré (le vérificateur mesure le kit lui-même, et c'est lui qui remplit le support). Une ligne Word fait environ 95 caractères (police 11, A4). Le gabarit complet ci-dessus tient en 20 à 25 lignes : au-delà de 12 lignes environ de plafond, passer au **gabarit compact** ci-dessous. Contrôle : `--lignes-par-section 10-15`, puis compter dans le document final (constat de l'évaluation du 17/10/2026 : premier jet à 23 / 20 / 19 lignes pour 15 demandées).
- **Gabarit compact** (longueur imposée courte) : « Dans la situation » en deux lignes au plus ; « Qui décide, qui propose » en deux lignes ; étiquette en tête de ligne, suivie du premier élément (« **Règles :** carence : … ») puis des autres en puces ; trois règles d'une ligne, référence courte en lien (`[L711-2](…)`, `[86-442, art. 25](…)`), la date de version étant donnée une fois dans le chapeau et dans « Références » ; deux ou trois options d'une ligne ; pas de « Points de vigilance » (les reporter dans une règle ou une option s'ils sont décisifs).
- Les étiquettes Cours / Légifrance / Analyse restent visibles : elles permettent au rédacteur de distinguer la règle de la proposition.
- Charte IA : si la consigne encadre l'usage de l'IA (charte de l'INSP ou de l'établissement), le rappeler en tête du kit et proposer la mention d'usage à joindre ; ne pas décrire la charte de mémoire : citer la consigne ou le document fourni, ou écrire que la règle est à vérifier.

### Remplir le support Word fourni

Quand l'école fournit un `.docx` à remplir :

1. Analyser le support sans le modifier : `uv run --with python-docx python scripts/remplir_docx.py support.docx --analyser` (questions repérées, style des puces, styles disponibles). Si les questions ne sont pas repérées, adapter `--motif` (expression dont le premier groupe est le numéro de la question).
2. Rédiger le kit en Markdown avec un titre `## Question N …` par question, dans la numérotation du support. Le chapeau (sources, date de version, « sans recommandation ») est reporté dans le Word juste avant la première question.
3. Contrôler : `python3 scripts/verifier_reponse.py kit.md --mode kit --enonce enonce.md --lignes-par-section 10-15`.
4. Remplir : `uv run --with python-docx python scripts/remplir_docx.py support.docx kit.md support-rempli.docx --sans-liens --supprimer "^Exemple"`. Chaque bloc est inséré sous sa question, avec les puces du gabarit ; les sections « Références » et « Charte IA » vont en fin de document. Le support d'origine n'est pas modifié. **`--sans-liens` est indispensable dès qu'une longueur est imposée** : sans lui, chaque lien devient « texte (adresse) » et une adresse Légifrance occupe une ligne Word à elle seule (évaluation du 17/10/2026 : 15 lignes estimées, 18 à 22 lignes réelles) ; avec lui, les adresses restent dans la table « Références ». `--supprimer` retire les paragraphes d'exemple du gabarit (adapter le motif au support ; `--analyser` les montre).
5. Contrôler la mise en page du fichier produit : le convertir en PDF (`soffice --headless --convert-to pdf support-rempli.docx` ; sur Mac, si `soffice` n'est pas dans le PATH : `/Applications/LibreOffice.app/Contents/MacOS/soffice …`) et compter les lignes de chaque question, ou, sans LibreOffice, le relire avec la compétence `docx`. Vérifier aussi les puces et les consignes du support restées en place.

Si `uv` ou python-docx ne sont pas disponibles, utiliser la compétence `docx` pour insérer le contenu sous chaque question, en reprenant le style de puces du gabarit.

## 10. Règles communes

- Écrire en français, au présent, à la première personne pour la décision (« je décide », « je saisis ») ; en mode kit, à l'impersonnel (« option A : … »), sans décision.
- Ouvrir chaque partie ou question par le bloc « Dans la situation » (section 0).
- La décision d'abord, la justification ensuite, dans chaque partie.
- Une affirmation, une source, au même endroit. Regrouper les sources en fin de document ne suffit pas.
- Les trois étiquettes de provenance (cours, Légifrance, analyse) restent visibles dans tous les modes.
- Pas de remplissage : ni introduction générale sur la fonction publique, ni conclusion sur « la complexité du management ».
- Enregistrer la réponse dans un fichier et la contrôler avant de la remettre ; donner ensuite la réponse dans la conversation avec le chemin du fichier.
