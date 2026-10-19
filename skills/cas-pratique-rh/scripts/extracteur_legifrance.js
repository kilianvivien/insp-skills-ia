// Extracteur Légifrance : à exécuter dans la page ouverte par le navigateur
// (outil javascript_tool / javascript_exec), après le délai d'attente anti-robot.
// Renvoie, pour chaque article affiché : numéro, identifiant LEGIARTI, mention de version,
// texte créateur ou modificateur, et texte intégral (tronqué à MAX caractères).
// Fonctionne sur les sections de code (/codes/section_lc/…), les articles seuls
// (/codes/article_lc/…, /loda/article_lc/…) et les textes consolidés (/loda/id/…).
// Relevé et testé le 17/10/2026.
// FILTRE : laisser null, ou une expression testée sur « numéro + texte » de chaque article, par ex.
//   /^Article (25|36-1)\b/  (décret long)   ou   /ANNEXE 5|chef de service/  (accord, annexes : voir plus bas).
(() => {
  const MAX = 3000;
  const FILTRE = null;
  const net = s => s.replace(/[ \t]+/g, ' ').replace(/\n{3,}/g, '\n\n')
    .replace(/\n(Voir les versions|Comparer les versions|Textes liés|Informations pratiques)[\s\S]*$/, '').trim();
  const origineDe = el => [...el.querySelectorAll('a')].map(x => x.innerText.trim())
    .filter(x => /^(Création|Modifié par|Abrogé par)/.test(x)).join(' ; ');
  const versionDe = t => (t.match(/version en vigueur[^\n]*|abrogé[^\n]*/i) || [''])[0];
  // 1. Structure de la page : un <article> par article, titre <h2 id="LEGIARTI…">
  const blocs = [...document.querySelectorAll('article')]
    .filter(a => a.querySelector('h2[id^="LEGIARTI"], h2 a[href*="LEGIARTI"]'));
  let res = blocs.map(a => {
    const h = a.querySelector('h2');
    const id = ((h.id || '') + ' ' + (h.querySelector('a')?.href || '')).match(/LEGIARTI\d{12}/)?.[0] || '';
    const txt = net(a.innerText);
    // Accords, annexes : le titre affiche seulement « Article » ; on le complète par la première ligne utile
    // du corps (« ANNEXE 5 LISTE… ») et par le suffixe de l'identifiant de la page (…-5-1).
    let titre = net(h.innerText);
    if (/^Article$/i.test(titre)) {
      const ligne = txt.split('\n').map(x => x.trim()).find(x => x && !/^Article$|^version en vigueur|^(Création|Modifié par)/i.test(x)) || '';
      const suffixe = (h.id || '').replace(/^LEGIARTI\d{12}-?/, '');
      titre = 'Article sans numéro' + (suffixe ? ' [' + suffixe + ']' : '') + ' — ' + ligne.slice(0, 70);
    }
    return { article: titre, id, version: versionDe(txt), origine: origineDe(a), texte: txt.slice(0, MAX) };
  });
  // 2. Secours si la structure change : découper le texte sur "\nArticle " et
  //    rattacher chaque article au lien LEGIARTI qui porte son numéro.
  if (!res.length) {
    const ids = {};
    document.querySelectorAll('a[href*="LEGIARTI"]').forEach(x => {
      const k = x.innerText.trim(); if (/^Article /.test(k) && !ids[k]) ids[k] = x.href.match(/LEGIARTI\d{12}/)[0];
    });
    res = document.body.innerText.split('\nArticle ').slice(1).map(b => {
      const num = b.split(/[\s\n]/)[0];
      const txt = net('Article ' + b);
      return { article: 'Article ' + num, id: ids['Article ' + num] || '', version: versionDe(txt), origine: '', texte: txt.slice(0, MAX) };
    });
  }
  if (FILTRE) res = res.filter(a => FILTRE.test(a.article + '\n' + a.texte));
  // Lien « Création / Modifié par Décret n° … » : mène au texte créateur (utile pour un décret codificateur).
  const textesLies = [...document.querySelectorAll('a')]
    .filter(x => /^(Création|Modifié par|Abrogé par)/.test(x.innerText.trim()))
    .map(x => ({ libelle: x.innerText.trim(), href: x.href })).filter((v, i, t) => t.findIndex(w => w.href === v.href) === i);
  return {
    page: document.title,
    adresse: location.href,
    date_page: location.pathname.match(/\d{4}-\d{2}-\d{2}/)?.[0] || 'version du jour',
    anti_robot: /Un instant|Just a moment|Vérification/i.test(document.title),
    articles: res,
    textes_lies: textesLies.slice(0, 15),
  };
})()
