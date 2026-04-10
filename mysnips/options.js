'use strict';

// ── Color helpers ─────────────────────────────────────────────────────────────

function isHexColor(str) {
  return /^#[0-9A-Fa-f]{3}([0-9A-Fa-f]{3})?$/.test((str || '').trim());
}

function colorSwatch(hex) {
  const s = document.createElement('span');
  s.style.cssText =
    `display:inline-block;width:14px;height:14px;border-radius:3px;` +
    `background:${hex};border:1px solid rgba(0,0,0,0.2);` +
    `flex-shrink:0;margin-right:6px;vertical-align:middle;cursor:default;`;
  s.title = hex;
  return s;
}

// ── State ─────────────────────────────────────────────────────────────────────

let tree = [];

// ── Storage ───────────────────────────────────────────────────────────────────

function loadTree() {
  chrome.storage.local.get('snips', data => {
    tree = (data.snips || { tree: [] }).tree;
    render();
  });
}

function saveTree() {
  chrome.storage.local.set({ snips: { tree } }, () => showStatus(t('savedStatus')));
}

// ── Utils ─────────────────────────────────────────────────────────────────────

function uid() { return crypto.randomUUID(); }

function truncate(str, len) {
  return str.length > len ? str.slice(0, len) + '…' : str;
}

function showStatus(msg) {
  const el = document.getElementById('status');
  el.textContent = msg;
  clearTimeout(el._t);
  el._t = setTimeout(() => (el.textContent = ''), 2500);
}

// ── Render ────────────────────────────────────────────────────────────────────

function getOpenFolders() {
  const open = new Set();
  document.querySelectorAll('.folder-body:not(.collapsed)').forEach(body => {
    const id = body.dataset.folderId;
    if (id) open.add(id);
  });
  return open;
}

function render(openFolders) {
  const container = document.getElementById('editor');
  container.innerHTML = '';
  renderList(tree, container, 0, openFolders);
}

function renderWithState() {
  const open = getOpenFolders();
  render(open);
}

function renderList(nodes, container, depth, openFolders) {
  for (let i = 0; i < nodes.length; i++) {
    container.appendChild(renderItem(nodes[i], nodes, i, depth, openFolders));
  }
  container.appendChild(createAddButtons(nodes, depth));
}

function renderItem(node, siblings, index, depth, openFolders) {
  const wrap = document.createElement('div');

  if (node.type === 'folder') {
    const row = document.createElement('div');
    row.className = 'item-row folder-row';
    row.style.paddingLeft = (8 + depth * 20) + 'px';

    const toggle = document.createElement('span');
    toggle.className = 'toggle';
    toggle.textContent = '▶';
    toggle.title = 'Ouvrir / Fermer';

    const icon = document.createElement('span');
    icon.className = 'icon';
    icon.textContent = '📁';

    const name = document.createElement('span');
    name.className = 'item-name';
    name.textContent = node.name;
    name.title = 'Double-clic pour renommer';
    name.addEventListener('dblclick', () => startEditName(name, node));

    const actions = createActions(node, siblings, index);

    row.appendChild(toggle);
    row.appendChild(icon);
    row.appendChild(name);
    row.appendChild(actions);
    wrap.appendChild(row);

    const body = document.createElement('div');
    body.className = 'folder-body collapsed';
    body.dataset.folderId = node.id;

    // Restaurer l'état ouvert si nécessaire
    if (openFolders?.has(node.id)) {
      body.classList.remove('collapsed');
      toggle.textContent = '▼';
    }

    renderList(node.children || [], body, depth + 1, openFolders);

    toggle.addEventListener('click', () => {
      const collapsed = body.classList.toggle('collapsed');
      toggle.textContent = collapsed ? '▶' : '▼';
    });

    wrap.appendChild(body);
  } else {
    // snippet
    const row = document.createElement('div');
    row.className = 'item-row snippet-row';
    row.style.paddingLeft = (28 + depth * 20) + 'px';

    const icon = document.createElement('span');
    icon.className = 'icon';
    icon.textContent = '≡';

    const fields = document.createElement('div');
    fields.className = 'snippet-fields';

    const name = document.createElement('span');
    name.className = 'item-name';
    name.textContent = node.name;
    name.title = 'Double-clic pour renommer';
    name.addEventListener('dblclick', () => startEditName(name, node));

    const sep = document.createElement('span');
    sep.className = 'sep';
    sep.textContent = '→';

    const valueWrap = document.createElement('span');
    valueWrap.className = 'item-value item-value-wrap';
    valueWrap.style.display = 'flex';
    valueWrap.style.alignItems = 'center';
    valueWrap.title = 'Double-clic pour éditer la valeur\n\n' + (node.value || '');
    valueWrap.addEventListener('dblclick', () => startEditValue(valueWrap, node));

    const val = node.value || '';
    if (isHexColor(val)) valueWrap.appendChild(colorSwatch(val.trim()));

    const valueText = document.createElement('span');
    valueText.textContent = truncate(val, 80);
    valueWrap.appendChild(valueText);

    fields.appendChild(name);
    fields.appendChild(sep);
    fields.appendChild(valueWrap);

    const actions = createActions(node, siblings, index);

    row.appendChild(icon);
    row.appendChild(fields);
    row.appendChild(actions);
    wrap.appendChild(row);
  }

  return wrap;
}

// ── Actions ───────────────────────────────────────────────────────────────────

function createActions(node, siblings, index) {
  const div = document.createElement('div');
  div.className = 'item-actions';

  div.appendChild(mkBtn('⬆', t('moveUp'), () => {
    if (index > 0) {
      [siblings[index - 1], siblings[index]] = [siblings[index], siblings[index - 1]];
      saveTree(); renderWithState();
    }
  }));

  div.appendChild(mkBtn('⬇', t('moveDown'), () => {
    if (index < siblings.length - 1) {
      [siblings[index], siblings[index + 1]] = [siblings[index + 1], siblings[index]];
      saveTree(); renderWithState();
    }
  }));

  const del = mkBtn('🗑', t('delete'), () => {
    const label = node.type === 'folder'
      ? t('deleteFolder').replace('%s', node.name)
      : t('deleteSnippet').replace('%s', node.name);
    if (confirm(label)) {
      siblings.splice(index, 1);
      saveTree(); renderWithState();
    }
  });
  del.classList.add('btn-del');
  div.appendChild(del);

  return div;
}

function mkBtn(text, title, onClick) {
  const b = document.createElement('button');
  b.className = 'action-btn';
  b.textContent = text;
  b.title = title;
  b.addEventListener('click', onClick);
  return b;
}

// ── Add buttons ───────────────────────────────────────────────────────────────

function createAddButtons(siblings, depth) {
  const div = document.createElement('div');
  div.className = 'add-row';
  div.style.paddingLeft = (28 + depth * 20) + 'px';

  const addFolder = document.createElement('button');
  addFolder.className = 'btn-add';
  addFolder.textContent = t('addFolder');
  addFolder.addEventListener('click', () => {
    const node = { id: uid(), type: 'folder', name: '', children: [] };
    siblings.push(node);
    saveTree();
    const open = getOpenFolders();
    render(open);
    // Trouver la ligne du nouveau dossier et démarrer l'édition inline
    const rows = document.querySelectorAll('.folder-row .item-name');
    const nameEl = [...rows].find(el => el.textContent === '');
    if (nameEl) startEditName(nameEl, node);
  });

  const addSnippet = document.createElement('button');
  addSnippet.className = 'btn-add';
  addSnippet.textContent = t('addSnippet');
  addSnippet.addEventListener('click', () => {
    const node = { id: uid(), type: 'snippet', name: '', value: '' };
    siblings.push(node);
    saveTree();
    const open = getOpenFolders();
    render(open);
    // Trouver la ligne du nouveau snippet et démarrer l'édition inline du nom
    const rows = document.querySelectorAll('.snippet-row .item-name');
    const nameEl = [...rows].find(el => el.textContent === '');
    if (nameEl) startEditNameThenValue(nameEl, node, siblings);
  });

  div.appendChild(addFolder);
  div.appendChild(addSnippet);
  return div;
}

// Édition en chaîne : nom → valeur pour les nouveaux snippets
function startEditNameThenValue(el, node, siblings) {
  const input = document.createElement('input');
  input.type = 'text';
  input.value = node.name;
  input.className = 'inline-input';
  input.placeholder = 'Name…';

  let committed = false;

  const commitName = () => {
    if (committed) return;
    committed = true;
    const v = input.value.trim();
    if (v) {
      node.name = v;
      saveTree();
      // Passer à l'édition de la valeur
      const open = getOpenFolders();
      render(open);
      const valueEls = document.querySelectorAll('.snippet-row .snippet-fields');
      for (const fields of valueEls) {
        const nameSpan = fields.querySelector('.item-name');
        if (nameSpan?.textContent === v) {
          const valueWrap = fields.querySelector('.item-value-wrap');
          if (valueWrap) { startEditValue(valueWrap, node); break; }
        }
      }
    } else {
      // Nom vide → supprimer le node
      if (siblings) {
        const idx = siblings.indexOf(node);
        if (idx !== -1) siblings.splice(idx, 1);
      }
      saveTree(); renderWithState();
    }
  };

  input.addEventListener('keydown', e => {
    if (e.key === 'Enter') { e.preventDefault(); commitName(); }
    if (e.key === 'Escape') {
      committed = true;
      if (siblings) {
        const idx = siblings.indexOf(node);
        if (idx !== -1) siblings.splice(idx, 1);
      }
      saveTree(); renderWithState();
    }
  });
  input.addEventListener('blur', commitName);

  el.replaceWith(input);
  input.focus();
}

// ── Inline editing ────────────────────────────────────────────────────────────

function startEditName(el, node) {
  const input = document.createElement('input');
  input.type = 'text';
  input.value = node.name;
  input.className = 'inline-input';

  let committed = false;

  const commit = () => {
    if (committed) return;
    committed = true;
    const v = input.value.trim();
    if (v) { node.name = v; saveTree(); }
    renderWithState();
  };

  input.addEventListener('keydown', e => {
    if (e.key === 'Enter') { e.preventDefault(); commit(); }
    if (e.key === 'Escape') { committed = true; renderWithState(); }
  });
  input.addEventListener('blur', commit);

  el.replaceWith(input);
  input.focus();
  input.select();
}

function startEditValue(el, node) {
  const ta = document.createElement('textarea');
  ta.value = node.value || '';
  ta.className = 'inline-textarea';
  ta.rows = Math.min(8, Math.max(3, (node.value || '').split('\n').length + 1));
  ta.title = 'Ctrl+Entrée pour valider, Échap pour annuler';

  const commit = () => {
    node.value = ta.value;
    saveTree(); renderWithState();
  };

  let committed = false;
  const commitOnce = () => { if (!committed) { committed = true; commit(); } };

  ta.addEventListener('keydown', e => {
    if (e.key === 'Escape') { committed = true; e.preventDefault(); renderWithState(); }
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); commitOnce(); }
    // Shift+Entrée → saut de ligne (comportement natif, pas besoin de handler)
  });
  ta.addEventListener('blur', commitOnce);

  el.replaceWith(ta);
  ta.focus();
}

// ── Import / Export ───────────────────────────────────────────────────────────

function exportJSON() {
  const json = JSON.stringify({ tree }, null, 2);
  const blob = new Blob([json], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'mysnips-export.json';
  a.click();
  URL.revokeObjectURL(url);
}

function importJSON(file) {
  const reader = new FileReader();
  reader.onload = e => {
    try {
      const data = JSON.parse(e.target.result);
      if (!Array.isArray(data.tree)) throw new Error('Champ "tree" manquant ou invalide.');
      const replace = confirm(t('importReplace'));
      tree = replace ? data.tree : [...tree, ...data.tree];
      saveTree(); renderWithState();
    } catch (err) {
      alert(t('importError') + err.message);
    }
  };
  reader.readAsText(file);
}

// ── JSON editor ───────────────────────────────────────────────────────────────

function syncJsonEditor() {
  const ta = document.getElementById('json-editor');
  ta.value = JSON.stringify({ tree }, null, 2);
  document.getElementById('json-error').textContent = '';
}

function applyJsonEditor() {
  const ta = document.getElementById('json-editor');
  const errEl = document.getElementById('json-error');
  try {
    const data = JSON.parse(ta.value);
    if (!Array.isArray(data.tree)) throw new Error('Champ "tree" manquant ou invalide.');
    tree = data.tree;
    saveTree();
    render();
    errEl.textContent = '';
  } catch (err) {
    errEl.textContent = '⚠ ' + err.message;
  }
}

// ── Tabs ──────────────────────────────────────────────────────────────────────

function initTabs() {
  const tabs = document.querySelectorAll('.tab');
  const panes = {
    visual: document.getElementById('pane-visual'),
    json:   document.getElementById('pane-json'),
  };

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');

      const name = tab.dataset.tab;
      Object.entries(panes).forEach(([k, p]) => {
        p.classList.toggle('hidden', k !== name);
      });

      if (name === 'json') syncJsonEditor();
    });
  });
}

// ── Shortcut display ──────────────────────────────────────────────────────────

function initShortcut() {
  chrome.commands.getAll(commands => {
    const cmd = commands.find(c => c.name === 'open-panel');
    const valueEl = document.getElementById('shortcut-value');
    const linkEl  = document.getElementById('shortcut-link');

    if (cmd?.shortcut) {
      const kbd = document.createElement('kbd');
      kbd.className = 'shortcut-key';
      kbd.textContent = cmd.shortcut;
      valueEl.appendChild(kbd);
    } else {
      const span = document.createElement('span');
      span.className = 'shortcut-none';
      span.textContent = t('shortcutNone');
      valueEl.appendChild(span);
      linkEl.textContent = t('shortcutConfigure');
      linkEl.classList.remove('hidden');
    }
  });
}

// ── Init ──────────────────────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
  // i18n static labels
  document.title = t('optionsTitle');
  document.getElementById('btn-import').textContent = t('importBtn');
  document.getElementById('btn-export').textContent = t('exportBtn');
  document.getElementById('btn-json-apply').textContent = t('jsonApply');
  document.getElementById('btn-json-reset').textContent = t('jsonReset');
  document.querySelector('#pane-visual .hint').textContent = t('visualHint');
  document.querySelector('#pane-json .hint').textContent = t('jsonHint');
  document.querySelector('.tab[data-tab="visual"]').textContent = t('tabVisual');
  document.querySelector('.tab[data-tab="json"]').textContent = t('tabJson');
  document.querySelector('#shortcut-bar .shortcut-label').textContent = t('shortcutLabel');

  loadTree();
  initTabs();
  initShortcut();

  // Import/export fichier
  document.getElementById('btn-export').addEventListener('click', exportJSON);
  const fileInput = document.getElementById('file-input');
  document.getElementById('btn-import').addEventListener('click', () => fileInput.click());
  fileInput.addEventListener('change', e => {
    if (e.target.files[0]) {
      importJSON(e.target.files[0]);
      e.target.value = '';
    }
  });

  // JSON editor
  document.getElementById('btn-json-apply').addEventListener('click', applyJsonEditor);
  document.getElementById('btn-json-reset').addEventListener('click', syncJsonEditor);
  document.getElementById('json-editor').addEventListener('keydown', e => {
    if (e.key === 's' && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      applyJsonEditor();
    }
  });
});
