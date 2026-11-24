# Dual Wield Keyboard

Public site for **Dual Wield Keyboard**, the two-handed keyboard for iPad and iPhone Duo by
Tengaira. Served via GitHub Pages.

| Page | URL |
|---|---|
| Top (EN) | https://TengaiRashinban.github.io/DualWieldKeyboard/ |
| トップ (JA) | https://TengaiRashinban.github.io/DualWieldKeyboard/index.ja.html |
| Support (EN) | https://TengaiRashinban.github.io/DualWieldKeyboard/support.html |
| サポート (JA) | https://TengaiRashinban.github.io/DualWieldKeyboard/support.ja.html |
| Privacy Policy (EN) | https://TengaiRashinban.github.io/DualWieldKeyboard/privacy.html |
| プライバシーポリシー (JA) | https://TengaiRashinban.github.io/DualWieldKeyboard/privacy.ja.html |

The privacy and support URLs are the ones to register in App Store Connect — do not
move or rename these files.

Contact: contact@tengaira.com

## How the pages are made

The six pages are generated — don't edit them by hand. Edit `tools/shell.ja.html`
(the shared look and the Japanese top page) or `tools/build.py` (the English top page and the
support / privacy text in both languages), then rebuild from the repository root and commit:

```bash
/Applications/Xcode.app/Contents/Developer/usr/bin/python3 -I tools/build.py
```

The mock-ups that led to this design are kept in the app repository
(`DuoKeyboard/docs/mock/`, with a README describing the order).
