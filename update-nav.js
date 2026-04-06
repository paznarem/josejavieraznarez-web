#!/usr/bin/env node
/**
 * update-nav.js — Actualiza automáticamente los enlaces anterior/siguiente
 * de todos los artículos del blog según el orden definido en blog/index.html.
 *
 * Uso: node update-nav.js
 */

const fs = require('fs');
const path = require('path');

const BLOG_DIR = path.join(__dirname, 'blog');
const INDEX_PATH = path.join(BLOG_DIR, 'index.html');

function stripTags(html) {
  return html.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
}

function getH1(html) {
  const m = html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/);
  return m ? stripTags(m[1]) : '';
}

function getArticleCategory(html) {
  const m = html.match(/<span class="article-category">([\s\S]*?)<\/span>/);
  return m ? stripTags(m[1]) : '';
}

// Lee el orden de artículos desde blog/index.html (sigue el orden de las tarjetas)
function parseArticleOrder() {
  const html = fs.readFileSync(INDEX_PATH, 'utf8');
  const hrefs = [];
  const re = /href="([a-z0-9\-]+\.html)" class="blog-card"/g;
  let m;
  while ((m = re.exec(html)) !== null) {
    if (!hrefs.includes(m[1])) hrefs.push(m[1]);
  }
  return hrefs;
}

function updateNavigation() {
  const order = parseArticleOrder();

  // Precarga título y categoría de cada artículo
  const meta = {};
  for (const href of order) {
    const filePath = path.join(BLOG_DIR, href);
    if (!fs.existsSync(filePath)) continue;
    const html = fs.readFileSync(filePath, 'utf8');
    meta[href] = { title: getH1(html), category: getArticleCategory(html) };
  }

  let updated = 0;

  for (let i = 0; i < order.length; i++) {
    const href = order[i];
    const filePath = path.join(BLOG_DIR, href);
    if (!fs.existsSync(filePath)) {
      console.warn(`  [omitido] no encontrado: ${href}`);
      continue;
    }

    let html = fs.readFileSync(filePath, 'utf8');
    const currentCat = meta[href]?.category || '';

    const prevHref = i > 0 ? order[i - 1] : null;
    const nextHref = i < order.length - 1 ? order[i + 1] : null;

    let navInner = '';

    if (prevHref && meta[prevHref]) {
      const crossCat = meta[prevHref].category !== currentCat;
      const label = crossCat ? `← ${meta[prevHref].category}` : '← Anterior';
      navInner += `
            <a href="${prevHref}" class="article-nav-prev">
                <span class="article-nav-label">${label}</span>
                <span class="article-nav-title">${meta[prevHref].title}</span>
            </a>`;
    }

    if (nextHref && meta[nextHref]) {
      const crossCat = meta[nextHref].category !== currentCat;
      const label = crossCat ? `Siguiente → ${meta[nextHref].category}` : 'Siguiente →';
      navInner += `
            <a href="${nextHref}" class="article-nav-next">
                <span class="article-nav-label">${label}</span>
                <span class="article-nav-title">${meta[nextHref].title}</span>
            </a>`;
    }

    const newBlock = `<div class="article-nav-inner">${navInner}
        </div>`;

    const newHtml = html.replace(
      /<div class="article-nav-inner">[\s\S]*?<\/div>/,
      newBlock
    );

    if (newHtml !== html) {
      fs.writeFileSync(filePath, newHtml, 'utf8');
      console.log(`  ✓ ${href}`);
      updated++;
    }
  }

  console.log(`\nNavegación actualizada en ${updated} artículo(s).`);
}

updateNavigation();
