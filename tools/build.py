"""公開サイトの 6 枚（日本語 .ja.html・英語は無印）を作る。

元は tools/shell.ja.html（地形・自機・ロゴ・キーボードの絵の部品と、日本語のトップの中身）。
英語のトップ・サポート・プライバシーの文は、このファイルの中にある。文を直したら、作り直してコミットする:

    /Applications/Xcode.app/Contents/Developer/usr/bin/python3 -I tools/build.py

（このリポジトリのいちばん上で走らせる。引数で元と出力先を替えられる: build.py <元の html> <出力先>）
"""
import sys, re, os
here = os.path.dirname(os.path.abspath(__file__))
mock = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, 'shell.ja.html')
dst = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(here)
shell = open(mock, encoding='utf-8').read()

# ---- 共通の直し（公開用） ----
shell = re.sub(r'<!--\n  モック。公開しない。.*?-->\n', '', shell, flags=re.S)
shell = shell.replace("drawLogo(document.getElementById('logo'), 'DUAL WIELD', 12);\n  drawLogo(document.getElementById('logo2'), 'KEYBOARD', 8);",
  "if (document.getElementById('logo')) {\n    drawLogo(document.getElementById('logo'), 'DUAL WIELD', 12);\n    drawLogo(document.getElementById('logo2'), 'KEYBOARD', 8);\n  }")
shell = shell.replace("if (e.isIntersecting) hud.textContent = 'AREA ' + e.target.dataset.area;",
  "if (e.isIntersecting) hud.textContent = e.target.dataset.hud || ('AREA ' + e.target.dataset.area);")
shell = shell.replace('    position: relative; z-index: 1; background: #000;', '    position: relative; z-index: 3; background: #000;')
shell = shell.replace('  footer a { color: #ddd; }', '  footer a { color: #ddd; }\n  footer .legal { flex-basis: 100%; font-size: 11px; color: #888; letter-spacing: .02em; }')
shell = shell.replace('<a class="tag" href="#top">', '<a class="tag" href="{HOME}#top">')
assert '{HOME}' in shell

def page(lang, title, hud, nav_prefix, main, footer, switch_href, switch_label):
    s = shell.replace('<html lang="ja">', f'<html lang="{lang}">')
    s = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', s)
    s = s.replace('<span id="hud-area">AREA 00</span>', f'<span id="hud-area">{hud}</span>')
    s = s.replace('{HOME}', nav_prefix)
    store = 'App Store で近日公開' if lang == 'ja' else 'Coming soon to the App Store'
    nav = f'''<nav>
    <a href="{nav_prefix}#feature">FEATURE</a>
    <a href="{nav_prefix}#setup">READY</a>
    <a href="{nav_prefix}#practice">PRACTICE</a>
    <a href="{nav_prefix}#faces">FACES</a>
    <a href="{nav_prefix}#game">BONUS</a>
    <a href="{nav_prefix}#price">PRICE</a>
    <a href="{switch_href}" lang="{'en' if lang == 'ja' else 'ja'}">{switch_label}</a>
    <span class="store">{store}</span>
  </nav>'''
    s = re.sub(r'<nav>.*?</nav>', nav, s, flags=re.S)
    s = re.sub(r'<main>.*?</main>', main.strip(), s, flags=re.S)
    s = re.sub(r'<footer>.*?</footer>', footer.strip(), s, flags=re.S)
    return s

EULA = 'https://www.apple.com/legal/internet-services/itunes/dev/stdeula/'
def footer(lang):
    if lang == 'ja':
        return f'''<footer>
  <span>DUAL WIELD KEYBOARD · © 2026 Tengaira (Hideto Minegishi)</span>
  <a href="support.ja.html">サポート</a>
  <a href="privacy.ja.html">プライバシーポリシー</a>
  <a href="{EULA}">利用規約（Apple 標準 EULA）</a>
  <span class="legal">iPad、iPhone は、米国およびその他の国で登録された Apple Inc. の商標です。App Store は、米国およびその他の国で登録された Apple Inc. のサービスマークです。</span>
</footer>'''
    return f'''<footer>
  <span>DUAL WIELD KEYBOARD · © 2026 Tengaira (Hideto Minegishi)</span>
  <a href="support.html">Support</a>
  <a href="privacy.html">Privacy Policy</a>
  <a href="{EULA}">Terms of Use (Apple Standard EULA)</a>
  <span class="legal">iPad and iPhone are trademarks of Apple Inc., registered in the U.S. and other countries. App Store is a service mark of Apple Inc., registered in the U.S. and other countries.</span>
</footer>'''

# ---- トップ ----
ja_main = re.search(r'<main>.*?</main>', shell, re.S).group(0)
ja_main = ja_main.replace('<span class="start">COMING SOON · App Store で近日公開</span>', '<span class="start">COMING SOON · App Store で近日公開</span>')

en_main = '''<main>
  <section id="top" data-area="00">
    <div class="title">
      <canvas id="logo" role="img" aria-label="DUAL WIELD"></canvas>
      <canvas id="logo2" role="img" aria-label="KEYBOARD"></canvas>
    </div>
    <h1>Dual Wield Keyboard</h1>
    <p class="lead">Hold tight. Type with both thumbs.<br>One thumb types. The other picks digits and words. A keyboard made for iPhone Duo and iPad.</p>
    <div class="blink">SCROLL TO START</div>
  </section>

  <section id="feature" data-area="01">
    <div class="area">AREA <b>01</b> · DUAL WIELD</div>
    <h2>Hold tight.<br>Type with both thumbs<span class="dot">.</span></h2>
    <div class="split">
      <div class="points">
        <div class="point"><h3>Keep your grip</h3><p>Typing keys and suggestions sit on the sides, by your thumbs.</p></div>
        <div class="point"><h3>Both hands at once</h3><p>One thumb keeps typing while the other picks.</p></div>
        <div class="point"><h3>Right- or left-handed</h3><p>Swap the sides with one key.</p></div>
      </div>
    </div>
    <div class="screen big">
      <div class="field">hel</div>
      <div class="board" data-face="en-qwerty" data-cands="hello,help,held" data-hl="hello" data-thumbs="1"></div>
    </div>
  </section>

  <section id="setup" data-area="02">
    <div class="area">AREA <b>02</b> · READY</div>
    <h2>Three steps to get ready<span class="dot">.</span></h2>
    <div class="row three">
      <div class="panel step"><div class="no">SETUP 1 / 3</div><h3>Turn it on in Settings</h3>
        <p>Go to Settings → General → Keyboard → Keyboards → Add New Keyboard, and choose Dual Wield Keyboard.</p>
        <div class="goal"><span>WHEN IT WORKS</span><div class="switch">Dual Wield Keyboard<i></i></div></div></div>
      <div class="panel step"><div class="no">SETUP 2 / 3</div><h3>Touch and hold 🌐, then pick it</h3>
        <p>In any text field, touch and hold the globe key, then pick Dual Wield Keyboard from the list.</p>
        <div class="goal"><span>WHEN IT WORKS</span><div class="board" data-face="en-qwerty"></div></div></div>
      <div class="panel step"><div class="no">SETUP 3 / 3</div><h3>Left-handed? Press ⇄</h3>
        <p>Each press of ⇄ in the middle swaps the sides. The keyboard remembers your choice.</p>
        <div class="goal"><span>LEFT-HANDED</span><div class="board" data-face="en-qwerty" data-mirror="1"></div></div></div>
    </div>
    <p class="note">No network access. No Full Access. Japanese conversion runs on your device, and nothing you type is learned.</p>
  </section>

  <section id="practice" data-area="03">
    <div class="area">AREA <b>03</b> · PRACTICE</div>
    <h2>Type “hel”,<br>then pick “hello”<span class="dot">.</span></h2>
    <p class="lead">Type h, e, l with one thumb. With the other, tap the suggestion “hello”.</p>
    <div class="practice"><span class="ok">h</span><span class="ok">e</span><span class="ok">l</span><b>→</b><span class="ok">hello</span><em>✓ Done</em></div>
    <div class="screen">
      <div class="field">hel</div>
      <div class="board" data-face="en-qwerty" data-cands="hello,help,held" data-hl="hello" data-thumbs="1"></div>
    </div>
  </section>

  <section id="faces" data-area="04">
    <div class="area">AREA <b>04</b> · FOUR FACES</div>
    <h2>Four layouts,<br>one key apart<span class="dot">.</span></h2>
    <div class="row two">
      <div class="face"><div class="no">Japanese · Flick</div><div class="board" data-face="ja-flick" data-cands="今日は,京は,きょうは" data-thumbs="1"></div></div>
      <div class="face"><div class="no">Japanese · Romaji</div><div class="board" data-face="ja-qwerty" data-cands="今日は,京は,きょうは" data-thumbs="1"></div></div>
      <div class="face"><div class="no">English · Flick (tap for digits)</div><div class="board" data-face="en-flick" data-cands="hello,help,held" data-thumbs="1"></div></div>
      <div class="face"><div class="no">English · QWERTY</div><div class="board" data-face="en-qwerty" data-cands="hello,help,held" data-thumbs="1"></div></div>
    </div>
    <div class="legend">
      <div><kbd>あ/A</kbd>Japanese and English</div>
      <div><kbd>⌨︎</kbd>Flick and QWERTY</div>
      <div><kbd>⇄</kbd>Right- and left-handed</div>
      <div><kbd>記</kbd>Digits sit on the picking side. 記 switches to symbols.</div>
    </div>
  </section>

  <section id="game" data-area="05">
    <div class="area">AREA <b>05</b> · BONUS STAGE</div>
    <h2>Build one sentence,<br>stage by stage<span class="dot">.</span></h2>
    <p class="lead">The first-run guide ends with a small game. Add one piece at a time until you finish the sentence, then type it in the final against your own record.</p>
    <div class="stages">
      <div class="stage on"><small>STAGE 1</small>Meet me at<em>Type letters</em></div>
      <div class="stage"><small>STAGE 2</small>+7<em>Tap a number</em></div>
      <div class="stage final"><small>FINAL</small>Timed<em>Type the whole sentence against the clock</em></div>
    </div>
    <div class="prompt">Meet me at <b>7</b> for <b>2</b> cups of tea</div>
  </section>

  <section id="price" class="coin" data-area="06">
    <div class="area">AREA <b>06</b> · INSERT COIN</div>
    <div class="credit">$3.99<small> / ¥600</small></div>
    <div class="sub">1 COIN · Buy once · No subscription<br>For iPad and iPhone Duo (OS version 27.2 or later)</div>
    <div><span class="start">COMING SOON · App Store</span></div>
  </section>
</main>'''

# ---- サポート ----
def panel(no, h, p): return f'      <div class="panel"><div class="no">{no}</div><h3>{h}</h3><p>{p}</p></div>\n'
def sub_main(sections):
    out = '<main>\n'
    for i, (hud, area, h2, lead, panels, extra) in enumerate(sections):
        pad = 'padding-top:140px;' if i == 0 else ''
        out += f'''  <section data-area="S{i+1}" data-hud="{hud}" style="min-height:auto;{pad}">
    <div class="area">{area}</div>
    <h2>{h2}<span class="dot">{'。' if hud.isascii() and False else '{DOT}'}</span></h2>
'''
        if lead: out += f'    <p class="lead">{lead}</p>\n'
        if panels: out += '    <div class="row" style="max-width:900px">\n' + ''.join(panel(*x) for x in panels) + '    </div>\n'
        out += extra + '  </section>\n'
    return out + '</main>'

MAIL = '<a href="mailto:contact@tengaira.com" style="color:inherit">contact@tengaira.com</a>'
sup_ja = sub_main([
 ('SUPPORT', 'SUPPORT · <b>CONTINUE?</b>', 'お気軽に、<br>ご連絡ください', 'ご質問、不具合のご報告、ご意見をお待ちしています。日本語でも英語でもかまいません。',
  [('CONTACT', MAIL, '不具合のときは、お使いの機種（iPad の型・iPhone Duo）、OS の版、縦か横か、どの面で起きたかを添えてください。'),
   ('提供者', 'Tengaira（Hideto Minegishi）', 'Dual Wield Keyboard は App Store で、日本では 600 円、米国では $3.99 の買い切りで提供します。')], ''),
 ('SUPPORT', 'HOW TO PLAY', 'よくある質問', '',
  [('Q1 · 入れ方', 'キーボードが出てきません。', '設定 → 一般 → キーボード → キーボード → 新しいキーボードを追加 から、Dual Wield Keyboard を選んでください。そのあと、文字を打つ欄でキーボードの地球儀を長押しし、一覧から Dual Wield Keyboard を選びます。アプリの「使い方と設定の手順を見る」でも同じ手順を見られます。'),
   ('Q2 · フルアクセス', '「フルアクセスを許可」は入れるべきですか？', '入れなくてかまいません。このキーボードはフルアクセスを求めず、なしですべての働きが使えます。'),
   ('Q3 · 左利き', '左手で打ちたい。', 'キーボードの真ん中の ⇄ を押すと、左右が入れ替わります。キーボードが覚えているので、次からもそのままです。'),
   ('Q4 · 変換', 'よく使う言葉を覚えてくれません。', 'そういう作りです。打った読みと確定した言葉を書き残さないため、変換の学習をしません。'),
   ('Q5 · 打った字', '打った字は、どこかへ送られますか？', '送られません。キーボードは通信をせず、かな漢字変換も端末の中で行います。くわしくはプライバシーポリシーをご覧ください。'),
   ('Q6 · 地球儀', 'キーボードの中に地球儀がありません。', '地球儀をキーボードの下に出す機種では、そちらの地球儀を使ってください。その機種では、キーボードの中には出しません。'),
   ('Q7 · 支払いと返金', '支払いと返金は？', '代金は App Store で払います。月額や追加の購入はありません。返金は Apple が扱うので、reportaproblem.apple.com からお申し込みください。')], ''),
 ('PRIVACY', 'PRIVACY', 'データの扱い', '', [], '    <div style="margin-top:32px"><a class="start" href="privacy.ja.html">プライバシーポリシーを読む →</a></div>\n'),
]).replace('{DOT}', '。')

sup_en = sub_main([
 ('SUPPORT', 'SUPPORT · <b>CONTINUE?</b>', 'Questions?<br>Just ask', 'Questions, bug reports, and feedback are all welcome, in English or Japanese.',
  [('CONTACT', MAIL, 'For a bug, please include your device (which iPad, or iPhone Duo), the OS version, portrait or landscape, and which layout you were using.'),
   ('PROVIDED BY', 'Tengaira (Hideto Minegishi)', 'Dual Wield Keyboard is a one-time purchase on the App Store: $3.99 in the U.S. and ¥600 in Japan.')], ''),
 ('SUPPORT', 'HOW TO PLAY', 'Frequently asked questions', '',
  [('Q1 · SETUP', 'The keyboard doesn’t show up.', 'Go to Settings → General → Keyboard → Keyboards → Add New Keyboard, and choose Dual Wield Keyboard. Then, in any text field, touch and hold the globe key and pick Dual Wield Keyboard from the list. The app’s setup guide walks through the same steps.'),
   ('Q2 · FULL ACCESS', 'Should I turn on “Allow Full Access”?', 'No need. The keyboard never asks for Full Access, and every feature works without it.'),
   ('Q3 · LEFT-HANDED', 'I want to type with my left hand.', 'Press ⇄ in the middle of the keyboard to swap the sides. The keyboard remembers your choice.'),
   ('Q4 · CONVERSION', 'It doesn’t learn the words I use often.', 'That’s by design. It never stores what you type or the words you pick, so conversion doesn’t learn.'),
   ('Q5 · WHAT YOU TYPE', 'Is what I type sent anywhere?', 'No. The keyboard never uses the network, and Japanese conversion runs on your device. See the Privacy Policy for details.'),
   ('Q6 · GLOBE KEY', 'There’s no globe key on the keyboard.', 'On devices that show a globe key below the keyboard, use that one. On those devices the keyboard doesn’t show its own.'),
   ('Q7 · PAYMENT AND REFUNDS', 'How do payment and refunds work?', 'You pay once on the App Store. There’s no subscription and nothing else to buy. Refunds are handled by Apple at reportaproblem.apple.com.')], ''),
 ('PRIVACY', 'PRIVACY', 'Your data', '', [], '    <div style="margin-top:32px"><a class="start" href="privacy.html">Read the Privacy Policy →</a></div>\n'),
]).replace('{DOT}', '.')

pri_ja = sub_main([
 ('PRIVACY', 'PRIVACY POLICY · 2026-11-24 から適用', '打った字は、<br>端末から出ない',
  'Dual Wield Keyboard（本体アプリとキーボード）が扱うデータについて書きます。提供者は Tengaira（Hideto Minegishi）です。',
  [('01 · 集めるデータ', 'ありません。', '本体アプリもキーボードも、通信をしません。打った字・読み・確定した言葉・使い方の記録を、端末の外へ送ることはありません。分析や広告のための道具も入っていません。'),
   ('02 · フルアクセス', '求めません。', 'キーボードは「フルアクセスを許可」なしで働きます。そのため、キーボードは通信できません。'),
   ('03 · 変換', '端末の中だけで。', 'かな漢字変換は、アプリに入っている Mozc と辞書で、端末の中で行います。変換の学習はしません。打った読みと確定した言葉は書き残しません。'),
   ('04 · 端末に残すもの', '設定と、ゲームの記録だけ。', 'キーボード: 左右の入れ替え、画面の広さごとに選んだ打ち方（フリックか QWERTY）、変換の設定のファイル（学習の中身は空）。本体アプリ: はじめての案内を終えたか、早打ちのゲームの自己ベスト（秒）と区切りの時刻、面をクリアしたか。どれも、あなたが打った文は含みません。'),
   ('05 · 第三者', '渡しません。', 'データを第三者に渡すことはありません。購入と支払いは App Store で行われ、Apple のプライバシーポリシーに従います。'),
   ('06 · 消し方', 'アプリを消せば、消えます。', '端末に残すものは、Dual Wield Keyboard を端末から削除すると、すべて消えます。キーボードだけを止めるには、設定 → 一般 → キーボード → キーボード から外してください。私たちは、あなたのデータを何も持っていません。そのため、消去の申し出は要りません。'),
   ('07 · 変更と連絡先', '変えるときは、ここで知らせます。', 'このポリシーを変えるときは、このページを更新し、適用の日付を改めます。ご質問は contact@tengaira.com へ。')], ''),
]).replace('{DOT}', '。')

pri_en = sub_main([
 ('PRIVACY', 'PRIVACY POLICY · EFFECTIVE NOV 24, 2026', 'What you type<br>stays on your device',
  'This policy covers the data handled by Dual Wield Keyboard (the app and its keyboard). Dual Wield Keyboard is provided by Tengaira (Hideto Minegishi).',
  [('01 · DATA WE COLLECT', 'None.', 'Neither the app nor the keyboard uses the network. Nothing you type, no readings, no words you pick, and no usage records ever leave your device. There are no analytics or advertising tools.'),
   ('02 · FULL ACCESS', 'Never requested.', 'The keyboard works without “Allow Full Access”, so it cannot use the network.'),
   ('03 · CONVERSION', 'On your device only.', 'Japanese conversion runs on your device, using Mozc and the dictionary bundled with the app. Conversion doesn’t learn, and what you type and the words you pick are never stored.'),
   ('04 · WHAT STAYS ON YOUR DEVICE', 'Settings and game records only.', 'Keyboard: the left/right swap, the typing style you chose for each screen width (flick or QWERTY), and the conversion settings files (with no learned data). App: whether you finished the first-run guide, your best time in the typing game and its split times, and which stages you cleared. None of these include anything you typed.'),
   ('05 · THIRD PARTIES', 'Nothing is shared.', 'We don’t share any data with third parties. Purchases and payments happen on the App Store under Apple’s privacy policy.'),
   ('06 · DELETING YOUR DATA', 'Delete the app, and it’s gone.', 'Everything stored on your device is removed when you delete Dual Wield Keyboard. To stop using just the keyboard, remove it in Settings → General → Keyboard → Keyboards. We don’t hold any of your data, so there’s nothing to request for deletion.'),
   ('07 · CHANGES AND CONTACT', 'Changes are posted here.', 'If this policy changes, we’ll update this page and its effective date. Questions: contact@tengaira.com.')], ''),
]).replace('{DOT}', '.')

pages = {
 'index.ja.html': page('ja', 'Dual Wield Keyboard — 握ったまま、両手の親指で打つ。', 'AREA 00', '', ja_main, footer('ja'), 'index.html', 'EN'),
 'index.html':    page('en', 'Dual Wield Keyboard — Hold tight. Type with both thumbs.', 'AREA 00', '', en_main, footer('en'), 'index.ja.html', '日本語'),
 'support.ja.html': page('ja', 'サポート — Dual Wield Keyboard', 'SUPPORT', 'index.ja.html', sup_ja, footer('ja'), 'support.html', 'EN'),
 'support.html':    page('en', 'Support — Dual Wield Keyboard', 'SUPPORT', 'index.html', sup_en, footer('en'), 'support.ja.html', '日本語'),
 'privacy.ja.html': page('ja', 'プライバシーポリシー — Dual Wield Keyboard', 'PRIVACY', 'index.ja.html', pri_ja, footer('ja'), 'privacy.html', 'EN'),
 'privacy.html':    page('en', 'Privacy Policy — Dual Wield Keyboard', 'PRIVACY', 'index.html', pri_en, footer('en'), 'privacy.ja.html', '日本語'),
}
for name, s in pages.items():
    # トップの中の目次は同じページの中へ（"#feature" のまま）
    if name.startswith('index'):
        s = s.replace('href="#feature"', 'href="#feature"')
    for bad in ['モック', 'MOCK', 'xevious', 'sales']:
        assert bad not in s, (name, bad)
    open(os.path.join(dst, name), 'w', encoding='utf-8').write(s)
    print(name, len(s))
