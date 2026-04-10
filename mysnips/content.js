// Guard contre la double-injection (SPA, iframes)
if (typeof window.__mysnipsLoaded === 'undefined') {
window.__mysnipsLoaded = true;
'use strict';

// i18n helper
function t(key) { return chrome.i18n.getMessage(key) || key; }

// ── Focus tracking ────────────────────────────────────────────────────────────

let lastFocused = null;

document.addEventListener('focusin', e => {
  const el = e.target;
  if (
    el.tagName === 'INPUT' ||
    el.tagName === 'TEXTAREA' ||
    el.isContentEditable ||
    el.getAttribute('contenteditable') === 'true'
  ) {
    lastFocused = el;
  }
}, true);

// ── Insert text ───────────────────────────────────────────────────────────────

function insertText(value) {
  const el = lastFocused;
  if (!el) { navigator.clipboard.writeText(value); return; }
  el.focus();
  const ok = document.execCommand('insertText', false, value);
  if (!ok) navigator.clipboard.writeText(value);
}

// ── Helpers ───────────────────────────────────────────────────────────────────

function truncate(str, len) {
  return str.length > len ? str.slice(0, len) + '…' : str;
}

function isHexColor(str) {
  return /^#[0-9A-Fa-f]{3}([0-9A-Fa-f]{3})?$/.test((str || '').trim());
}

// ── Panel ─────────────────────────────────────────────────────────────────────

let panelHost = null;
const elMap = new Map();

let _panelKeydown = null;

function closePanel() {
  if (panelHost) { panelHost.remove(); panelHost = null; }
  if (_panelKeydown) { document.removeEventListener('keydown', _panelKeydown, true); _panelKeydown = null; }
}

function getPosition() {
  const panelW = 360;
  const panelH = 420;

  // Utilise activeElement en priorité (plus fiable que lastFocused sur Gmail etc.)
  const anchor = document.activeElement !== document.body ? document.activeElement : lastFocused;

  if (anchor) {
    const r = anchor.getBoundingClientRect();
    const spaceBelow = window.innerHeight - r.bottom;
    const spaceAbove = r.top;

    // Préférence : en dessous si la place suffit, sinon au-dessus.
    let top;
    if (spaceBelow >= panelH || spaceBelow >= spaceAbove) {
      top = r.bottom + 4;
    } else {
      top = r.top - panelH - 4;
    }
    // Garder dans le viewport
    if (top + panelH > window.innerHeight - 4) top = window.innerHeight - panelH - 4;
    if (top < 4) top = 4;

    let left = r.left;
    if (left + panelW > window.innerWidth - 8) left = window.innerWidth - panelW - 8;
    if (left < 4) left = 4;

    return { top, left };
  }

  // Fallback centre écran
  return {
    top: Math.max(20, (window.innerHeight - panelH) / 2),
    left: Math.max(8, (window.innerWidth - panelW) / 2),
  };
}

const PANEL_CSS = `
* { box-sizing: border-box; margin: 0; padding: 0; }

:host {
  all: initial;
  position: fixed;
  z-index: 2147483647;
  font-family: system-ui, -apple-system, sans-serif;
  font-size: 13px;
}

#panel {
  width: 360px;
  max-height: 420px;
  background: #fff;
  border: 1px solid #d0d0d0;
  border-radius: 10px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.18), 0 2px 8px rgba(0,0,0,0.10);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.header {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 10px;
  border-bottom: 1px solid #e5e5e5;
  background: #f8f8f8;
  border-radius: 10px 10px 0 0;
}

#search {
  flex: 1;
  padding: 5px 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 13px;
  outline: none;
  background: #fff;
  font-family: inherit;
}
#search:focus { border-color: #4a90e2; }

.icon-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 15px;
  padding: 3px 6px;
  border-radius: 5px;
  color: #666;
  line-height: 1;
}
.icon-btn:hover { background: #e8e8e8; color: #333; }

#tree {
  flex: 1;
  overflow-y: auto;
  padding: 4px 0 6px;
}

.empty {
  padding: 20px;
  text-align: center;
  color: #888;
  line-height: 1.7;
}

.folder-header {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 5px 10px;
  cursor: pointer;
  user-select: none;
  font-weight: 600;
  color: #333;
  border-radius: 6px;
  margin: 1px 4px;
}
.folder-header:hover, .folder-header.focused { background: #dce8fb; }

.arrow {
  font-size: 10px;
  color: #999;
  width: 10px;
  display: inline-block;
  flex-shrink: 0;
}

.snippet {
  display: flex;
  flex-direction: column;
  padding: 5px 10px;
  cursor: pointer;
  gap: 1px;
  border-radius: 6px;
  margin: 1px 4px;
}
.snippet:hover, .snippet.focused { background: #dce8fb; }
.snippet:active { background: #c8d8f8; }

.snippet-name {
  font-weight: 500;
  color: #1a1a1a;
}

.snippet-value {
  color: #777;
  font-size: 11px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
  display: flex;
  align-items: center;
}

.swatch {
  display: inline-block;
  width: 11px;
  height: 11px;
  border-radius: 2px;
  border: 1px solid rgba(0,0,0,0.2);
  flex-shrink: 0;
  margin-right: 5px;
}

.toast {
  position: absolute;
  bottom: 10px;
  left: 50%;
  transform: translateX(-50%);
  background: #2d2d2d;
  color: #fff;
  padding: 5px 14px;
  border-radius: 20px;
  font-size: 12px;
  pointer-events: none;
  opacity: 1;
  transition: opacity 0.2s;
  white-space: nowrap;
}
.toast.hidden { opacity: 0; }
`;

function showToast(root, msg = 'Copié !') {
  const toast = root.getElementById('toast');
  toast.textContent = msg;
  toast.classList.remove('hidden');
  clearTimeout(toast._t);
  toast._t = setTimeout(() => toast.classList.add('hidden'), 1400);
}

// ── Navigation ────────────────────────────────────────────────────────────────

function getFocused(root) { return root.querySelector('.nav-item.focused'); }
function setFocus(root, el) {
  const prev = getFocused(root);
  if (prev) prev.classList.remove('focused');
  if (!el) return;
  el.classList.add('focused');
  el.scrollIntoView({ block: 'nearest' });
}

function navDown(root) {
  const el = getFocused(root);
  if (!el) { setFocus(root, root.querySelector('.nav-item')); return; }
  const { node, siblings, index, parentEl } = el._nav;
  if (node.type === 'folder') {
    const body = el.nextElementSibling;
    if (body && body.style.display !== 'none' && node.children?.length) {
      const c = elMap.get(node.children[0].id);
      if (c) { setFocus(root, c); return; }
    }
  }
  for (let i = index + 1; i < siblings.length; i++) {
    const n = elMap.get(siblings[i].id);
    if (n) { setFocus(root, n); return; }
  }
  let anc = parentEl;
  while (anc) {
    const { siblings: ps, index: pi } = anc._nav;
    for (let i = pi + 1; i < ps.length; i++) {
      const n = elMap.get(ps[i].id);
      if (n) { setFocus(root, n); return; }
    }
    anc = anc._nav.parentEl;
  }
}

function navUp(root) {
  const el = getFocused(root);
  if (!el) return;
  const { siblings, index, parentEl } = el._nav;
  for (let i = index - 1; i >= 0; i--) {
    const n = elMap.get(siblings[i].id);
    if (n) { setFocus(root, n); return; }
  }
  if (parentEl) setFocus(root, parentEl);
}

function navRight(root) {
  const el = getFocused(root);
  if (!el || el._nav.node.type !== 'folder') return;
  const body = el.nextElementSibling;
  if (!body) return;
  if (body.style.display === 'none') {
    el.click();
  } else {
    const first = el._nav.node.children?.[0];
    if (first) { const c = elMap.get(first.id); if (c) setFocus(root, c); }
  }
}

function navLeft(root) {
  const el = getFocused(root);
  if (!el) return;
  if (el._nav.node.type === 'folder') {
    const body = el.nextElementSibling;
    if (body && body.style.display !== 'none') { el.click(); return; }
  }
  if (el._nav.parentEl) setFocus(root, el._nav.parentEl);
}

// ── Render tree ───────────────────────────────────────────────────────────────

function renderNodes(nodes, container, term, depth, parentEl, root) {
  for (let i = 0; i < nodes.length; i++) {
    const node = nodes[i];
    if (term && !matchNode(node, term)) continue;

    if (node.type === 'folder') {
      const wrap = document.createElement('div');
      const header = document.createElement('div');
      header.className = 'folder-header nav-item';
      header.style.paddingLeft = (8 + depth * 16) + 'px';
      header._nav = { node, siblings: nodes, index: i, parentEl };
      elMap.set(node.id, header);

      const arrow = document.createElement('span');
      arrow.className = 'arrow';
      arrow.textContent = term ? '▼' : '▶';

      const nameSpan = document.createElement('span');
      nameSpan.textContent = '📁 ' + node.name;
      header.appendChild(arrow);
      header.appendChild(nameSpan);
      header.addEventListener('mouseenter', () => setFocus(root, header));

      const body = document.createElement('div');
      body.className = 'folder-body';
      if (!term) body.style.display = 'none';

      header.addEventListener('click', () => {
        const hidden = body.style.display === 'none';
        body.style.display = hidden ? '' : 'none';
        arrow.textContent = hidden ? '▼' : '▶';
      });

      wrap.appendChild(header);
      wrap.appendChild(body);
      container.appendChild(wrap);
      if (node.children?.length) renderNodes(node.children, body, term, depth + 1, header, root);

    } else {
      const div = document.createElement('div');
      div.className = 'snippet nav-item';
      div.style.paddingLeft = (24 + depth * 16) + 'px';
      div._nav = { node, siblings: nodes, index: i, parentEl };
      elMap.set(node.id, div);

      const nameEl = document.createElement('span');
      nameEl.className = 'snippet-name';
      nameEl.textContent = node.name;

      const valRow = document.createElement('span');
      valRow.className = 'snippet-value';

      const val = node.value || '';
      if (isHexColor(val)) {
        const sw = document.createElement('span');
        sw.className = 'swatch';
        sw.style.background = val.trim();
        valRow.appendChild(sw);
      }
      const valText = document.createElement('span');
      valText.textContent = truncate(val, 55);
      valRow.appendChild(valText);

      div.appendChild(nameEl);
      div.appendChild(valRow);
      div.addEventListener('mouseenter', () => setFocus(root, div));
      div.addEventListener('click', () => {
        insertText(val);
        closePanel();
      });

      container.appendChild(div);
    }
  }
}

function matchNode(node, term) {
  if (node.type === 'snippet')
    return node.name.toLowerCase().includes(term) || (node.value || '').toLowerCase().includes(term);
  return (node.children || []).some(c => matchNode(c, term));
}

function renderTree(root, tree, term) {
  elMap.clear();
  const container = root.getElementById('tree');
  container.innerHTML = '';
  if (!tree.length) { container.innerHTML = `<p class="empty">${t('noSnippets')}</p>`; return; }
  const filtered = term ? tree.filter(n => matchNode(n, term)) : tree;
  if (term && !filtered.length) { container.innerHTML = `<p class="empty">${t('noResults')}</p>`; return; }
  renderNodes(tree, container, term, 0, null, root);
}

// ── Open panel ────────────────────────────────────────────────────────────────

function openPanel(tree) {
  if (panelHost) return; // déjà ouvert, on ignore

  panelHost = document.createElement('div');
  panelHost.style.cssText = 'position:fixed;z-index:2147483647;';
  document.documentElement.appendChild(panelHost);

  const shadow = panelHost.attachShadow({ mode: 'closed' });

  const style = document.createElement('style');
  style.textContent = PANEL_CSS;
  shadow.appendChild(style);

  // Structure
  const panel = document.createElement('div');
  panel.id = 'panel';

  const header = document.createElement('div');
  header.className = 'header';

  const search = document.createElement('input');
  search.type = 'search';
  search.id = 'search';
  search.placeholder = t('searchPlaceholder');
  search.autocomplete = 'off';

  const closeBtn = document.createElement('button');
  closeBtn.className = 'icon-btn';
  closeBtn.textContent = '✕';
  closeBtn.title = t('closePanel');
  closeBtn.addEventListener('click', closePanel);

  header.appendChild(search);
  header.appendChild(closeBtn);

  const treeDiv = document.createElement('div');
  treeDiv.id = 'tree';

  const toast = document.createElement('div');
  toast.id = 'toast';
  toast.className = 'toast hidden';

  panel.appendChild(header);
  panel.appendChild(treeDiv);
  panel.appendChild(toast);
  shadow.appendChild(panel);

  // Helper getElementById sur shadow root
  shadow.getElementById = (id) => shadow.querySelector('#' + id);

  // Position
  const pos = getPosition();
  panelHost.style.top = pos.top + 'px';
  panelHost.style.left = pos.left + 'px';

  renderTree(shadow, tree, '');
  // Ne pas voler le focus — le curseur reste dans le champ texte original

  // Recherche : frappe de caractères filtre la liste sans quitter le champ
  function handleKeydown(e) {
    if (!panelHost) { document.removeEventListener('keydown', handleKeydown, true); return; }

    // Caractère imprimable → ajouter au filtre de recherche
    if (e.key.length === 1 && !e.ctrlKey && !e.metaKey && !e.altKey) {
      search.value += e.key;
      renderTree(shadow, tree, search.value.trim().toLowerCase());
      e.preventDefault();
      return;
    }
    // Backspace → effacer dernier caractère du filtre
    if (e.key === 'Backspace' && search.value) {
      search.value = search.value.slice(0, -1);
      renderTree(shadow, tree, search.value.trim().toLowerCase());
      e.preventDefault();
      return;
    }

    switch (e.key) {
      case 'ArrowDown':  e.preventDefault(); navDown(shadow);  break;
      case 'ArrowUp':    e.preventDefault(); navUp(shadow);    break;
      case 'ArrowRight': e.preventDefault(); navRight(shadow); break;
      case 'ArrowLeft':  e.preventDefault(); navLeft(shadow);  break;
      case 'Enter':
        e.preventDefault();
        getFocused(shadow)?.click();
        break;
      case 'Escape':
        e.preventDefault();
        if (search.value) { search.value = ''; renderTree(shadow, tree, ''); }
        else closePanel();
        break;
    }
  }

  _panelKeydown = handleKeydown;
  document.addEventListener('keydown', handleKeydown, true);

  // Clic en dehors → fermer
  setTimeout(() => {
    document.addEventListener('mousedown', outsideClick);
  }, 100);

  function outsideClick(e) {
    if (!panelHost?.contains(e.target)) {
      closePanel();
      document.removeEventListener('mousedown', outsideClick);
    }
  }
}

// ── Messages ──────────────────────────────────────────────────────────────────

chrome.runtime.onMessage.addListener((msg) => {
  if (msg.type === 'OPEN_PANEL') {
    // N'ouvrir que dans le frame qui a le focus (gère les iframes Jotform, Gmail, etc.)
    const active = document.activeElement;
    const hasFocus = document.hasFocus() && active && active.tagName !== 'IFRAME';
    if (!hasFocus) return;
    chrome.storage.local.get('snips', data => {
      openPanel((data.snips || { tree: [] }).tree);
    });
  }
  if (msg.type === 'INSERT_SNIPPET') {
    insertText(msg.value);
  }
});

} // end guard __mysnipsLoaded
