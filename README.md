# ✂️ MySnips

**MySnips** is a private, local-first Chrome extension to organize and instantly paste your text snippets.

No account. No cloud. No tracking. Your data never leaves your browser.

---

## Features

- **Tree organization** — unlimited nested folders, drag-free reordering
- **Floating panel** — opens right below the active field (Alt+S)
- **Keyboard navigation** — ↓↑ move between siblings, → expands a folder, ← collapses / goes to parent, Enter inserts
- **Direct insertion** — pastes directly into the focused field, no Ctrl+V needed
- **Color swatches** — hex color values (`#3286A7`) are shown with a color preview
- **Full JSON editor** — edit your snippets as raw JSON, import/export in one click
- **Context menu** — right-click any editable field → MySnips → pick a snippet
- **Zero permissions abuse** — `<all_urls>` and `scripting` are used solely to inject the panel and insert text into the active field

---

## Install

### From the Chrome Web Store
*(coming soon)*

### Manual (developer mode)
1. Download or clone this repo
2. Go to `chrome://extensions/`
3. Enable **Developer mode**
4. Click **Load unpacked** → select the `mysnips/` folder

---

## Keyboard shortcut

Default: **Alt+S**

If the shortcut conflicts with another extension, configure it at `chrome://extensions/shortcuts`.

---

## Data format

Your snippets are stored locally in `chrome.storage.local` as a simple JSON tree:

```json
{
  "tree": [
    {
      "id": "folder-elevatio",
      "type": "folder",
      "name": "Elevatio",
      "children": [
        { "id": "elevatio-siret", "type": "snippet", "name": "SIRET", "value": "12345678900000" }
      ]
    }
  ]
}
```

You can export, edit, and re-import this file at any time from the options page.

---

## Privacy

MySnips collects **no data**. See the [Privacy Policy](https://cyrilgodon.github.io/mysnips/).

---

## License

MIT
