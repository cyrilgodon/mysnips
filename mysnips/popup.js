'use strict';

// ── Helpers ───────────────────────────────────────────────────────────────────

function truncate(str, len) {
  return str.length > len ? str.slice(0, len) + '…' : str;
}

function isHexColor(str) {
  return /^#[0-9A-Fa-f]{3}([0-9A-Fa-f]{3})?$/.test((str || '').trim());
}

function colorSwatch(hex) {
  const s = document.createElement('span');
  s.style.cssText =
    `display:inline-block;width:12px;height:12px;border-radius:2px;` +
    `background:${hex};border:1px solid rgba(0,0,0,0.2);` +
    `flex-shrink:0;margin-right:5px;vertical-align:middle;`;
  return s;
}

function hasMatch(node, term) {
  if (node.type === 'snippet') {
    return node.name.toLowerCase().includes(term) ||
           (node.value || '').toLowerCase().includes(term);
  }
  return (node.children || []).some(c => hasMatch(c, term));
}

// ── Focus ─────────────────────────────────────────────────────────────────────

// Map node.id → DOM element header/row
const elMap = new Map();

function setFocus(el) {
  const prev = document.querySelector('#tree .nav-item.focused');
  if (prev) prev.classList.remove('focused');
  if (!el) return;
  el.classList.add('focused');
  el.scrollIntoView({ block: 'nearest' });
}

function getFocusedEl() {
  return document.querySelector('#tree .nav-item.focused');
}

// ── Navigation ────────────────────────────────────────────────────────────────

// Each nav-item gets ._navData = { node, siblings, index, parentEl }
// parentEl = the folder header DOM element of the parent, or null if root

function navDown() {
  const el = getFocusedEl();
  if (!el) {
    const first = document.querySelector('#tree .nav-item');
    if (first) setFocus(first);
    return;
  }

  const { node, siblings, index, parentEl } = el._navData;

  // Dossier déplié → descendre dans le premier enfant
  if (node.type === 'folder') {
    const body = el.nextElementSibling;
    const isOpen = body && body.style.display !== 'none';
    if (isOpen && node.children?.length) {
      const firstChild = elMap.get(node.children[0].id);
      if (firstChild) { setFocus(firstChild); return; }
    }
  }

  // Sinon → frère suivant au même niveau
  for (let i = index + 1; i < siblings.length; i++) {
    const next = elMap.get(siblings[i].id);
    if (next) { setFocus(next); return; }
  }

  // Dernier du niveau → remonter et chercher le frère suivant du parent
  let ancestor = parentEl;
  while (ancestor) {
    const { siblings: ps, index: pi } = ancestor._navData;
    for (let i = pi + 1; i < ps.length; i++) {
      const next = elMap.get(ps[i].id);
      if (next) { setFocus(next); return; }
    }
    ancestor = ancestor._navData.parentEl;
  }
}

function navUp() {
  const el = getFocusedEl();
  if (!el) return;

  const { siblings, index, parentEl } = el._navData;

  // Frère précédent au même niveau
  for (let i = index - 1; i >= 0; i--) {
    const prev = elMap.get(siblings[i].id);
    if (prev) { setFocus(prev); return; }
  }

  // Premier du niveau → remonter au parent
  if (parentEl) setFocus(parentEl);
}

function navRight() {
  const el = getFocusedEl();
  if (!el || el._navData.node.type !== 'folder') return;
  const body = el.nextElementSibling;
  if (!body) return;
  const isCollapsed = body.style.display === 'none';
  if (isCollapsed) {
    // Expand
    el.click();
  } else {
    // Already open → move to first child
    const firstChild = (el._navData.node.children || [])[0];
    if (firstChild) {
      const childEl = elMap.get(firstChild.id);
      if (childEl) setFocus(childEl);
    }
  }
}

function navLeft() {
  const el = getFocusedEl();
  if (!el) return;
  if (el._navData.node.type === 'folder') {
    const body = el.nextElementSibling;
    if (body && body.style.display !== 'none') {
      // Collapse
      el.click();
      return;
    }
  }
  // Go to parent
  const parentEl = el._navData.parentEl;
  if (parentEl) setFocus(parentEl);
}

// ── Render ────────────────────────────────────────────────────────────────────

function renderNodes(nodes, container, term, depth, parentEl) {
  for (let i = 0; i < nodes.length; i++) {
    const node = nodes[i];
    if (term && !hasMatch(node, term)) continue;

    if (node.type === 'folder') {
      const div = document.createElement('div');

      const header = document.createElement('div');
      header.className = 'folder-header nav-item';
      header.tabIndex = -1;
      header.style.paddingLeft = (8 + depth * 16) + 'px';
      header._navData = { node, siblings: nodes, index: i, parentEl };
      elMap.set(node.id, header);

      const arrow = document.createElement('span');
      arrow.className = 'arrow';
      arrow.textContent = term ? '▼' : '▶';

      const nameSpan = document.createElement('span');
      nameSpan.textContent = '📁 ' + node.name;

      header.appendChild(arrow);
      header.appendChild(nameSpan);

      const childrenDiv = document.createElement('div');
      childrenDiv.className = 'folder-body';
      if (!term) childrenDiv.style.display = 'none';

      header.addEventListener('click', () => {
        const hidden = childrenDiv.style.display === 'none';
        childrenDiv.style.display = hidden ? '' : 'none';
        arrow.textContent = hidden ? '▼' : '▶';
      });

      header.addEventListener('mouseenter', () => setFocus(header));

      div.appendChild(header);
      div.appendChild(childrenDiv);
      container.appendChild(div);

      if (node.children?.length) {
        renderNodes(node.children, childrenDiv, term, depth + 1, header);
      }
    } else {
      const div = document.createElement('div');
      div.className = 'snippet nav-item';
      div.tabIndex = -1;
      div.style.paddingLeft = (24 + depth * 16) + 'px';
      div._navData = { node, siblings: nodes, index: i, parentEl };
      elMap.set(node.id, div);

      const nameEl = document.createElement('span');
      nameEl.className = 'snippet-name';
      nameEl.textContent = node.name;

      const valRow = document.createElement('span');
      valRow.className = 'snippet-value';
      valRow.style.display = 'flex';
      valRow.style.alignItems = 'center';

      const val = node.value || '';
      if (isHexColor(val)) valRow.appendChild(colorSwatch(val.trim()));

      const valText = document.createElement('span');
      valText.textContent = truncate(val, 60);
      valRow.appendChild(valText);

      div.appendChild(nameEl);
      div.appendChild(valRow);

      div.addEventListener('click', () => {
        const value = node.value || '';
        // Toujours copier dans le presse-papier
        navigator.clipboard.writeText(value);
        // Et tenter l'insertion directe dans le dernier champ actif
        chrome.tabs.query({ active: true, currentWindow: true }, tabs => {
          if (!tabs[0]) { showToast('Copié !'); return; }
          chrome.tabs.sendMessage(tabs[0].id, { type: 'INSERT_SNIPPET', value }, res => {
            if (chrome.runtime.lastError || !res?.ok) {
              showToast('Copié !');
            } else {
              window.close();
            }
          });
        });
      });

      div.addEventListener('mouseenter', () => setFocus(div));

      container.appendChild(div);
    }
  }
}

function render(tree, term) {
  elMap.clear();
  const container = document.getElementById('tree');
  container.innerHTML = '';

  if (!tree.length) {
    container.innerHTML =
      `<p class="empty">${t('noSnippets')}<br><a id="open-options" href="#">${t('openEditor')}</a></p>`;
    document.getElementById('open-options').addEventListener('click', e => {
      e.preventDefault();
      chrome.runtime.openOptionsPage();
    });
    return;
  }

  const filtered = term ? tree.filter(n => hasMatch(n, term)) : tree;
  if (term && !filtered.length) {
    container.innerHTML = `<p class="empty">${t('noResults')}</p>`;
    return;
  }

  renderNodes(tree, container, term, 0, null);
}

// ── Toast ─────────────────────────────────────────────────────────────────────

function showToast(msg = 'Copié !') {
  const toast = document.getElementById('toast');
  toast.textContent = msg;
  toast.classList.remove('hidden');
  clearTimeout(toast._timer);
  toast._timer = setTimeout(() => toast.classList.add('hidden'), 1400);
}

// ── Init ──────────────────────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
  chrome.storage.local.get('snips', data => {
    const tree = (data.snips || { tree: [] }).tree;

    render(tree, '');

    const search = document.getElementById('search');

    search.addEventListener('input', () => {
      render(tree, search.value.trim().toLowerCase());
    });

    document.addEventListener('keydown', e => {
      // Taper une lettre → focus recherche
      if (e.key.length === 1 && !e.ctrlKey && !e.metaKey && !e.altKey) {
        if (document.activeElement !== search) {
          search.focus();
          return;
        }
      }

      switch (e.key) {
        case 'ArrowDown':  e.preventDefault(); navDown();  break;
        case 'ArrowUp':    e.preventDefault(); navUp();    break;
        case 'ArrowRight': e.preventDefault(); navRight(); break;
        case 'ArrowLeft':  e.preventDefault(); navLeft();  break;
        case 'Enter':
          e.preventDefault();
          getFocusedEl()?.click();
          break;
        case 'Escape':
          search.value = '';
          render(tree, '');
          search.focus();
          break;
      }
    });

    // i18n
    document.getElementById('search').placeholder = t('searchPlaceholder');
    document.getElementById('btn-options').title = t('openOptions');

    document.getElementById('btn-options').addEventListener('click', () => {
      chrome.runtime.openOptionsPage();
    });
  });
});
