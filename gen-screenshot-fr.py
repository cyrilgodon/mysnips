#!/usr/bin/env python3
"""Génère le screenshot Store en français — 1280×800."""

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

HTML_FILE = Path(__file__).parent / "screenshot-combined.html"
OUT_FILE  = Path(__file__).parent / "screenshot-store-fr.png"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1280, "height": 800})

        url = HTML_FILE.resolve().as_uri()
        await page.goto(url, wait_until="networkidle")

        await page.evaluate("""(data) => {
            const el = (id) => document.getElementById(id);
            const set = (id, html) => { const e = el(id); if (e) e.innerHTML = html; };
            const setText = (id, txt) => { const e = el(id); if (e) e.textContent = txt; };

            // ── Titres étapes ──
            set('step1-text', data.step1);
            set('step2-text', data.step2);

            // ── Options card ──
            setText('editor-title',    data.editorTitle);
            setText('import-btn',      data.importBtn);
            setText('export-btn',      data.exportBtn);
            setText('shortcut-label',  data.shortcutLabel);
            setText('configure-link',  data.configureLink);
            setText('tab-tree',        data.tabTree);
            setText('tab-json',        data.tabJson);
            setText('hint-text',       data.hint);

            // Options tree
            const treeMap = data.treeMap;
            document.querySelectorAll('.options-card .item-name').forEach(node => {
                const t = node.textContent.trim();
                if (treeMap[t]) node.textContent = treeMap[t];
            });

            // ── Callouts colonne 1 ──
            setText('col1-bubble1-text', data.col1b1);
            setText('col1-bubble2-text', data.col1b2);
            setText('col1-bubble3-text', data.col1b3);

            // ── Formulaire ──
            setText('form-title',    data.formTitle);
            setText('label-company', data.labelCompany);
            setText('label-vat',     data.labelVat);
            setText('label-msg',     data.labelMsg);
            el('input-company').value = data.companyValue;
            el('textarea-msg').value  = data.textareaValue;

            // ── Bulles colonne 2 gauche ──
            set('bubble1', data.bubble1);
            setText('bubble2', data.bubble2);

            // ── Bulle colonne 2 droite ──

            // ── Panel ──
            el('panel-search-input').placeholder = data.searchPlaceholder;
            setText('folder-company',  data.panelFolderCompany);
            setText('snippet-vat',     data.panelSnipVat);
            setText('snippet-id',      data.panelSnipId);
            setText('snippet-addr',    data.panelSnipAddr);
            setText('folder-booking',  data.panelFolderBooking);
            setText('folder-colors',   data.panelFolderColors);
        }""", {
            # Étapes
            "step1": "Configurez vos snippets r\u00e9currents<br>directement dans l\u2019extension",
            "step2": (
                "Ins\u00e9rez instantan\u00e9ment vos snippets les plus courants "
                "dans n\u2019importe quel champ texte \u2014 appuyez sur "
                "<span style=\"background:rgba(255,255,255,0.25);border-radius:4px;"
                "padding:1px 7px;font-family:monospace;\">Alt+S</span>"
            ),
            # Options card
            "editorTitle":   "\u2702\ufe0f MySnips \u2014 \u00c9diteur",
            "importBtn":     "\u2b06 Importer",
            "exportBtn":     "\u2b07 Exporter",
            "shortcutLabel": "Raccourci clavier\u00a0:",
            "configureLink": "\u00b7 Configurer",
            "tabTree":       "Arbre",
            "tabJson":       "JSON brut",
            "hint":          "Double-cliquez sur un nom ou une valeur pour l\u2019\u00e9diter.",
            "treeMap": {
                "Company":          "Soci\u00e9t\u00e9",
                "VAT number":       "Num\u00e9ro de TVA",
                "Company ID":       "N\u00b0 SIREN",
                "Address":          "Adresse",
                "Booking links":    "Liens visio",
                "Calendly":         "Calendly",
                "Zoom":             "Zoom",
                "Brand colors":     "Couleurs marque",
                "Primary (mauve)":  "Primaire (mauve)",
                "Secondary (blue)": "Secondaire (bleu)",
                "Emails":           "Emails",
            },
            # Callouts col 1  (1=Alt+S, 2=Folders, 3=Edit inline)
            "col1b1": "Personnalisez votre raccourci Alt+S",
            "col1b2": "Organisez en dossiers th\u00e9matiques",
            "col1b3": "\u00c9ditez en ligne \u2014 double-cliquez sur la valeur",
            # Formulaire
            "formTitle":      "Inscription fournisseur",
            "labelCompany":   "Nom de la soci\u00e9t\u00e9",
            "labelVat":       "Num\u00e9ro de TVA",
            "labelMsg":       "Message",
            "companyValue":   "Acme France SAS",
            "textareaValue":  "Bonjour,\nSi vous pr\u00e9f\u00e9rez, je peux vous retrouver sur Zoom.\n\u00c0 bient\u00f4t, Alex",
            # Bulles col 2 gauche
            "bubble1": (
                "<kbd style=\"background:rgba(255,255,255,0.3);border-radius:3px;"
                "padding:1px 5px;font-family:monospace;\">Alt+S</kbd> "
                "pour ouvrir les snippets"
            ),
            "bubble2": "Naviguez, s\u00e9lectionnez, ins\u00e9rez",
            # Bulle col 2 droite — supprimée
            # Panel
            "searchPlaceholder":  "Recherche\u2026",
            "panelFolderCompany": "Soci\u00e9t\u00e9",
            "panelSnipVat":       "Num\u00e9ro de TVA",
            "panelSnipId":        "N\u00b0 SIREN",
            "panelSnipAddr":      "Adresse",
            "panelFolderBooking": "Liens visio",
            "panelFolderColors":  "Couleurs marque",
        })

        await page.screenshot(path=str(OUT_FILE), full_page=False)
        await browser.close()

    print(f"Screenshot saved: {OUT_FILE}")
    print(f"Size: {OUT_FILE.stat().st_size // 1024} KB")

if __name__ == "__main__":
    asyncio.run(main())
