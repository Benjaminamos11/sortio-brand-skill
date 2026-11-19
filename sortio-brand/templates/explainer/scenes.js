window.SCENES = [
  {
    "id": "s1", "type": "title",
    "eyebrow": "Sortio erklärt",
    "lines": ["Jeden Monat", "derselbe Stapel."]
  },
  {
    "id": "s2", "type": "phone",
    "eyebrow": "01 — Scannen",
    "lines": ["Foto machen.", "Sortio liest."],
    "screens": [
      { "src": "../../assets/screens/scanner-page.webp" },
      { "src": "../../assets/screens/review-result.webp", "cue": [3, "Sortio"] }
    ],
    "callouts": [
      { "icon": "building", "label": "Absender", "value": "Helsana Versicherungen AG", "cue": [3, "Absender"] },
      { "icon": "banknote", "label": "Betrag", "value": "CHF 412.30", "mono": true, "cue": [3, "Betrag"] },
      { "icon": "calendar", "label": "Fälligkeit", "value": "31.10.2026", "mono": true, "cue": [3, "Fälligkeit"] }
    ]
  },
  {
    "id": "s3", "type": "phone",
    "eyebrow": "02 — Ablegen",
    "lines": ["Automatisch", "im richtigen Ordner."],
    "screens": [ { "src": "../../assets/screens/folders.webp" } ],
    "highlight": { "box": [372, 771, 683, 1068], "cue": [6, "Versicherungen"] }
  },
  {
    "id": "s4", "type": "phone",
    "eyebrow": "03 — Erinnern",
    "lines": ["Keine Frist", "rutscht durch."],
    "screens": [ { "src": "../../assets/screens/tasks.webp" } ],
    "highlight": { "box": [36, 357, 684, 524], "cue": [7, "Aufgaben"] },
    "callouts": [
      { "icon": "bell", "label": "Erinnerung", "value": "1 Tag vor Frist erinnern", "cue": [8, "Vortag"] }
    ]
  },
  {
    "id": "s5", "type": "phone",
    "eyebrow": "04 — Fragen",
    "lines": ["Frag deine", "Unterlagen."],
    "screens": [ { "src": "../../assets/screens/chat-open-bills.webp" } ],
    "callouts": [
      { "icon": "sparkle", "label": "Sortio AI", "value": "Total: CHF 3’168.25", "cue": [10, "Antwort"] }
    ]
  },
  {
    "id": "s6", "type": "points",
    "eyebrow": "Sicherheit",
    "lines": ["In der Schweiz", "gespeichert."],
    "points": [
      { "icon": "shield", "text": "Daten in der Schweiz", "cue": [11, "Schweiz"] },
      { "icon": "lock", "text": "AES-256 verschlüsselt", "cue": [11, "AES-256"] },
      { "icon": "globe", "text": "Deutsch · Französisch · Englisch", "cue": [12, "Deutsch"] }
    ]
  },
  {
    "id": "s7", "type": "end", "captions": false,
    "wordmark": "Sortio",
    "lines": ["Weniger Papierkram.", "Mehr Kopf für das, was zählt."],
    "cta": "Im App Store laden",
    "url": "sortio.ch", "urlNote": "Kostenlos starten"
  }
];
