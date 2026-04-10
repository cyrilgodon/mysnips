'use strict';

// ── Build context menus ───────────────────────────────────────────────────────

function buildMenus(tree) {
  chrome.contextMenus.removeAll(() => {
    chrome.contextMenus.create({
      id: 'mysnips-root',
      title: '✂️ MySnips',
      contexts: ['editable'],
    });

    let count = 0;

    function addNodes(nodes, parentId) {
      for (const node of nodes) {
        if (count > 200) return;
        count++;
        if (node.type === 'folder') {
          chrome.contextMenus.create({
            id: 'folder-' + node.id,
            parentId,
            title: '📁 ' + node.name,
            contexts: ['editable'],
          });
          if (node.children?.length) addNodes(node.children, 'folder-' + node.id);
        } else {
          const preview = (node.value || '').slice(0, 40).replace(/\n/g, ' ');
          chrome.contextMenus.create({
            id: 'snip-' + node.id,
            parentId,
            title: node.name + (preview ? '  —  ' + preview : ''),
            contexts: ['editable'],
          });
        }
      }
    }

    addNodes(tree, 'mysnips-root');
  });
}

function loadAndBuild() {
  chrome.storage.local.get('snips', data => {
    buildMenus((data.snips || { tree: [] }).tree);
  });
}

// ── Send open-panel to active tab ─────────────────────────────────────────────

let lastOpenCall = 0;

function openPanel() {
  const now = Date.now();
  if (now - lastOpenCall < 800) return; // ignore key repeat + keyup
  lastOpenCall = now;
  chrome.tabs.query({ active: true, currentWindow: true }, tabs => {
    if (!tabs[0]) return;
    const tabId = tabs[0].id;

    // Essaie d'envoyer le message ; si le content script n'est pas là, l'injecte d'abord
    chrome.tabs.sendMessage(tabId, { type: 'OPEN_PANEL' }, res => {
      if (chrome.runtime.lastError) {
        // Content script absent → injection dynamique puis retry
        chrome.scripting.executeScript(
          { target: { tabId }, files: ['content.js'] },
          () => {
            if (chrome.runtime.lastError) return;
            setTimeout(() => {
              chrome.tabs.sendMessage(tabId, { type: 'OPEN_PANEL' });
            }, 100);
          }
        );
      }
    });
  });
}

// ── Snippet lookup ────────────────────────────────────────────────────────────

function findSnippet(nodes, targetId) {
  for (const node of nodes) {
    if (node.type === 'snippet' && node.id === targetId) return node.value;
    if (node.type === 'folder' && node.children) {
      const found = findSnippet(node.children, targetId);
      if (found !== null) return found;
    }
  }
  return null;
}

// ── Events ────────────────────────────────────────────────────────────────────

chrome.runtime.onInstalled.addListener(loadAndBuild);
chrome.runtime.onStartup.addListener(loadAndBuild);
chrome.storage.onChanged.addListener((changes, area) => {
  if (area === 'local' && changes.snips) loadAndBuild();
});

// Toolbar button click → open panel
chrome.action.onClicked.addListener(openPanel);

// Keyboard shortcut → open panel
chrome.commands.onCommand.addListener(cmd => {
  if (cmd === 'open-panel') openPanel();
});

// Context menu click → insert snippet
chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (!info.menuItemId.startsWith('snip-')) return;
  const snippetId = info.menuItemId.replace('snip-', '');
  chrome.storage.local.get('snips', data => {
    const value = findSnippet((data.snips || { tree: [] }).tree, snippetId);
    if (value !== null) chrome.tabs.sendMessage(tab.id, { type: 'INSERT_SNIPPET', value });
  });
});
