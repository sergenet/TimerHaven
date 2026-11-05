"""Rebuild benefits-of-taking-breaks-el.html with a clean Greek body.

The page is double-encoded: ~3,700 of its 8,390 visible characters are mojibake
lead bytes, so it is unreadable while still being linked from all 8 language
mirrors and listed in the sitemap. The corruption is lossy (an earlier pass
replaced some non-ASCII bytes) and predates the only commit that touches the
file, so it cannot be decoded back and no clean copy exists locally, on the
server or in git.

This keeps the page's own <head> (Greek canonical, hreflang cluster, consent and
analytics wiring) and every <script> from its <body>, and replaces the visible
content with a Greek article whose structure, internal links and two AdSense
units match the English source.

Run: python scripts/fix_greek_article.py [--dry]
"""
import re
import sys

DRY = "--dry" in sys.argv
PATH = "benefits-of-taking-breaks-el.html"

TITLE = "Διαλείμματα στην εργασία: η επιστήμη της ανάκαμψης"
DESC = ("Πλήρης οδηγός για την επιστήμη της ανάκαμψης στην εργασία: υπερημερήσιοι "
        "ρυθμοί, κορτιζόλη και πρακτικοί τρόποι για αποδοτικά διαλείμματα.")

AD_IN = ('<div class="th-ad-slot" data-ad-placement="in-article" '
         'style="margin:24px auto;max-width:728px;min-height:90px;text-align:center;overflow:hidden">\n'
         '<span class="th-ad-label" style="display:block;font-size:10px;letter-spacing:.1em;'
         'text-transform:uppercase;opacity:.55;margin-bottom:4px">Διαφήμιση</span>\n'
         '<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-0467059729557007" '
         'data-ad-slot="2835722251" data-ad-format="auto" data-full-width-responsive="true"></ins>\n'
         '</div>')

AD_OUT = ('<div class="th-ad-slot" data-ad-placement="footer" '
          'style="margin:24px auto;max-width:728px;min-height:90px;text-align:center;overflow:hidden">\n'
          '<span class="th-ad-label" style="display:block;font-size:10px;letter-spacing:.1em;'
          'text-transform:uppercase;opacity:.55;margin-bottom:4px">Διαφήμιση</span>\n'
          '<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-0467059729557007" '
          'data-ad-slot="1522640584" data-ad-format="auto" data-full-width-responsive="true"></ins>\n'
          '</div>')

BODY = f"""<body>
  <div class="article-container">
    <div class="author">
      <img src="/assets/images/authors/serge-shammas-200.jpg"
           srcset="/assets/images/authors/serge-shammas-400.jpg 2x"
           width="56" height="56"
           alt="Serge Shammas — αρθρογράφος παραγωγικότητας και ερευνητής UX" loading="lazy">
      <div class="byline"><strong>Από τον Serge Shammas</strong> — αρθρογράφος παραγωγικότητας
        και ερευνητής UX</div>
    </div>
    <div class="meta">Δημοσιεύτηκε: 20 Ιαν 2026 · Ενημερώθηκε: 29 Ιαν 2026 · Χρόνος ανάγνωσης: 10 λεπτά</div>

    <h1>Η επιστήμη της ανάκαμψης στην εργασία</h1>

    <p>Για δεκαετίες, η κουλτούρα της υπερεργασίας υποστήριζε ότι η επιτυχία έρχεται μόνο με
      περισσότερες ώρες και λιγότερη ανάπαυση. Οι σύγχρονες νευροεπιστήμες λένε κάτι διαφορετικό:
      <strong>η σκόπιμη ανάκαμψη είναι το κλειδί για σταθερή, βιώσιμη απόδοση.</strong></p>

    {AD_IN}

    <h2>1. Κατανοώντας τον υπερημερήσιο ρυθμό</h2>
    <p>Η ανθρώπινη προσοχή δεν είναι γραμμικός πόρος. Ο εγκέφαλος λειτουργεί σε κύκλους έντονης
      δραστηριότητας που ακολουθούνται από περιόδους ανάπαυσης — τους <strong>υπερημερήσιους
      ρυθμούς</strong>. Αυτοί οι κύκλοι διαρκούν συνήθως περίπου 90 λεπτά.</p>
    <p>Όταν περνάς το όριο των 90 λεπτών χωρίς διάλειμμα, η απόδοση μειώνεται. Εκεί ξεκινούν τα
      λάθη, κολλάει η δημιουργικότητα και κοιτάς την ίδια παράγραφο για δεκαπέντε λεπτά. Ένα
      διάλειμμα 15 λεπτών κάθε 90 λεπτά (ή 5 λεπτά κάθε 25, όπως στην
      <a href="/pomodoro.html">τεχνική Pomodoro</a>) επαναφέρει το γνωστικό σου ρολόι για την
      επόμενη συνεδρία.</p>

    <h2>2. Κορτιζόλη και διαχείριση του ψηφιακού στρες</h2>
    <p>Η παρατεταμένη συγκέντρωση ενεργοποιεί την αντίδραση στρες του σώματος και ανεβάζει την
      κορτιζόλη. Σε μικρές δόσεις είναι χρήσιμη, αλλά η χρόνια αύξηση οδηγεί σε θολή σκέψη και
      συναισθηματική εξάντληση.</p>

    <div class="expert-box">
      <p><strong>Γνώμη εμπειρογνώμονα:</strong> «Ένα διάλειμμα δεν είναι απλώς μια φυσική
        επανεκκίνηση. Η κίνηση του σώματος ή η εξάσκηση της ενσυνειδητότητας βοηθά στον καθαρισμό
        της κορτιζόλης από το σύστημα, αποτρέποντας την εξάντληση στους περισσότερους υπαλλήλους
        γραφείου.»</p>
      <span class="scientific-cite">— S. Shammas, Επικεφαλής Έρευνας UX</span>
    </div>

    <h2>3. Το πλαίσιο της «ενεργητικής ανάκαμψης»</h2>
    <p>Δεν είναι όλα τα διαλείμματα ίδια. Για το μεγαλύτερο όφελος, προτίμησε την ενεργητική
      ανάκαμψη αντί για τα «ψεύτικα διαλείμματα» — όπως το σκρολάρισμα στα social media, που
      συνεχίζει να καταναλώνει γνωστική ενέργεια.</p>

    <h3>Σωματική κίνηση</h3>
    <p>Ακόμη και 2 λεπτά περπάτημα ή διατάσεις βελτιώνουν την κυκλοφορία στον προμετωπιαίο φλοιό,
      την περιοχή που είναι υπεύθυνη για τις εκτελεστικές λειτουργίες. Χρησιμοποίησε το
      <a href="/timer-el.html">Task Timer</a> για να μην ξεχνάς αυτές τις μικρές αλλά ζωτικές
      κινήσεις.</p>

    <h3>Οπτική ανάπαυση (ο κανόνας 20-20-20)</h3>
    <p>Για να μειώσεις την κόπωση των ματιών και τους πονοκεφάλους, ακολούθησε τον κανόνα: κάθε
      20 λεπτά, κοίτα κάτι σε απόσταση 6 μέτρων για τουλάχιστον 20 δευτερόλεπτα. Έτσι χαλαρώνουν
      οι μύες των ματιών και μειώνεται η γνωστική κόπωση.</p>

    <h3>Κοινωνική επαφή (η ώθηση της ωκυτοκίνης)</h3>
    <p>Μια σύντομη, θετική συζήτηση με έναν συνάδελφο ή ένα αγαπημένο πρόσωπο απελευθερώνει
      ωκυτοκίνη, που λειτουργεί ως φυσική ασπίδα απέναντι στο εργασιακό στρες. Γι' αυτό τα
      κοινωνικά διαλείμματα βοηθούν ιδιαίτερα σε δουλειές με υψηλή συναισθηματική απαίτηση.</p>

    <h2>4. Πώς να οργανώσεις την ημέρα ανάκαμψής σου</h2>
    <p>Για μέγιστη παραγωγικότητα, προτείνουμε διαλείμματα σε επίπεδα:</p>
    <ul>
      <li><strong>Μικρο-διαλείμματα (κάθε 25-30 λεπτά):</strong> 2 έως 5 λεπτά για να σηκωθείς,
        να τεντωθείς και να επανεκκινήσεις. Ιδανικά με το
        <a href="/pomodoro.html">Pomodoro Timer</a>.</li>
      <li><strong>Γνωστική επαναφορά (κάθε 90 λεπτά):</strong> 15 έως 20 λεπτά μακριά από όλες
        τις οθόνες. Ιδανική στιγμή για ένα υγιεινό σνακ ή βαθιές αναπνοές.</li>
      <li><strong>Βαθιά επαναφορά (μέσα στη μέρα):</strong> Ένα διάλειμμα 45 έως 60 λεπτών, όπως
        ένας περίπατος, για πλήρη αποσύνδεση από τις εργασίες.</li>
    </ul>

    <div class="internal-link-box">
      <strong>Σχετικοί πόροι στο TimerHaven:</strong>
      <ul>
        <li><a href="/timer-el.html">Εκτίμηση χρόνου εργασιών με το Task Timer</a></li>
        <li><a href="/el/notes/notes-index.html">Σημειώσεις που δουλεύουν υπό πίεση</a></li>
        <li><a href="/pomodoro.html">Δοκίμασε το Pomodoro Timer για αυτόματα διαλείμματα</a></li>
      </ul>
    </div>

    <h2>Σύνοψη</h2>
    <p>Τα διαλείμματα δεν είναι μια «πολυτέλεια» για όταν υπάρχει χρόνος. Είναι δομικό στοιχείο
      της επαγγελματικής εργασίας. Σεβόμενοι τα βιολογικά όρια του εγκεφάλου και αξιοποιώντας
      εργαλεία όπως το TimerHaven για να διαχειρίζεστε τις συνεδρίες σας, μπορείτε να πετύχετε
      περισσότερα σε 6 ώρες από ό,τι ένας εξαντλημένος εργαζόμενος σε 10.</p>

    {AD_OUT}

    <div class="mt-4 text-center">
      <a href="/index-el.html" class="btn btn-primary btn-lg">Εξερευνήστε περισσότερα εργαλεία παραγωγικότητας</a>
    </div>

    <footer>
      &copy; 2025 TimerHaven. Όλα τα εργαλεία είναι δωρεάν και σέβονται την ιδιωτικότητα.<br>
      <a href="/privacy.html">Πολιτική Απορρήτου</a> ·
      <a href="/terms.html">Όροι Χρήσης</a> ·
      <a href="/contact.html">Επικοινωνία</a>
    </footer>
  </div>
"""


def main():
    html = open(PATH, encoding="utf-8", errors="surrogateescape").read()
    original = html

    body_start = html.find("<body")
    body_end = html.rfind("</body>")
    if body_start == -1 or body_end == -1:
        sys.exit("no body — refusing to touch this file")

    head = html[:body_start]
    old_body = html[body_start:body_end]

    # Keep every script from the old body: consent gating and the ad loader
    # live there, and they are plain ASCII, so they survived the corruption.
    scripts = re.findall(r"<script\b.*?</script>", old_body, re.S)

    head = re.sub(r"(<html[^>]*\blang=[\"'])en([\"'])", r"\1el\2", head, count=1)
    head = re.sub(r"(<title[^>]*>).*?(</title>)",
                  lambda m: m.group(1) + TITLE + m.group(2), head, count=1, flags=re.S)
    for attr, text in (
        ('name="description"', DESC), ("name='description'", DESC),
        ('property="og:title"', TITLE), ("property='og:title'", TITLE),
        ('property="og:description"', DESC), ("property='og:description'", DESC),
        ('name="twitter:title"', TITLE), ("name='twitter:title'", TITLE),
        ('name="twitter:description"', DESC), ("name='twitter:description'", DESC),
    ):
        pattern = re.compile(r"(<meta\s+" + re.escape(attr) + r"[^>]*content=[\"']).*?([\"'])",
                             re.S | re.I)
        head = pattern.sub(lambda m: m.group(1) + text + m.group(2), head, count=1)

    new_html = head + BODY + "\n" + ("\n".join(scripts) + "\n" if scripts else "") + "</body>\n</html>\n"

    print("scripts preserved:", len(scripts))
    print("mojibake lead bytes remaining:", sum(new_html.count(c) for c in "ÎÏÃÂ"))
    print("title len:", len(TITLE), "| desc len:", len(DESC))
    print("hrefs:", re.findall(r'<a\b[^>]*href="([^"]+)"', new_html))

    if DRY:
        print("DRY RUN — nothing written")
        return
    with open(PATH, "w", encoding="utf-8", newline="") as fh:
        fh.write(new_html)
    print("written; bytes", len(original), "->", len(new_html))


if __name__ == "__main__":
    main()
