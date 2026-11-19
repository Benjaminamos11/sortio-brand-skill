window.REEL = {
  "width": 1080,
  "height": 1920,
  "fps": 30,
  "duration": 18.0,
  "music": "audio/soundtrack.m4a",
  "logo": "../../assets/logo/sortio-mark-origami.png",
  "hook": {
    "duration": 2.9,
    "eyebrow": "Bisher",
    "lines": ["Briefe stapeln sich", "auf dem Tisch."],
    "strike": true,
    "letter": { "screen": "../../assets/screens/review-result.webp", "crop": [36, 248, 682, 1173] }
  },
  "beats": [
    {
      "duration": 3.7,
      "eyebrow": "01 — Scannen",
      "lines": ["Sortio liest,", "was wichtig ist."],
      "before": "../../assets/screens/scanner-page.webp",
      "tap": [360, 1422],
      "screen": "../../assets/screens/review-result.webp",
      "callouts": [
        { "icon": "building", "label": "Absender", "value": "Helsana Versicherungen AG" },
        { "icon": "banknote", "label": "Betrag", "value": "CHF 412.30", "mono": true },
        { "icon": "calendar", "label": "Fälligkeit", "value": "31.10.2026", "mono": true }
      ]
    },
    {
      "duration": 3.5,
      "eyebrow": "02 — Ablegen",
      "lines": ["Automatisch", "im richtigen Ordner."],
      "screen": "../../assets/screens/folders.webp",
      "highlight": [372, 771, 683, 1068],
      "collect": true,
      "callouts": []
    },
    {
      "duration": 3.6,
      "eyebrow": "03 — Erinnern",
      "lines": ["Keine Frist", "rutscht durch."],
      "screen": "../../assets/screens/tasks.webp",
      "highlight": [36, 357, 684, 524],
      "callouts": [
        { "icon": "bell", "label": "Erinnerung", "value": "1 Tag vor Frist erinnern", "y": 1150 }
      ]
    }
  ],
  "end": {
    "duration": 4.3,
    "wordmark": "Sortio",
    "eyebrow": "Verwaltungs-Assistent · Aus der Schweiz",
    "lines": ["Weniger Papierkram.", "Mehr Kopf für das,", "was zählt."],
    "cta": "Im App Store laden",
    "url": "sortio.ch",
    "urlNote": "Kostenlos starten"
  }
};
