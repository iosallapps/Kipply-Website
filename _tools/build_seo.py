#!/usr/bin/env python3
"""SEO build for kipplyapp.com.  python3 _tools/build_seo.py <legal fragments dir>

The English pages in the site root are the source. This script
  1. rewrites each page's <head> (title, description, canonical, hreflang, Open Graph,
     Twitter, preloads, JSON-LD) and adds the EN/RO switch + the Visto Apps footer link,
  2. generates the real Romanian pages in ro/ (index, support, privacy, terms) from the
     English body (text nodes through RO_TEXT), _tools/ro_support_body.html and the
     Romanian legal fragments (visto-apps/tools/legal/adapters/fragments.py),
  3. rewrites sitemap.xml and robots.txt.
Re-run after every edit of an English page.
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FRAG = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else None
BASE = "https://kipplyapp.com"
ASSET_V = "20261116s"
LASTMOD = "2026-11-15"
APP_ID = "6756061280"
STORE = f"https://apps.apple.com/app/id{APP_ID}"
SCREENS = ["home", "swipe", "smart", "deleted", "discover"]
# the one contact address already published on the site
MAIL = re.search(r'mailto:([^"]+)"', (ROOT / "support.html").read_text()).group(1)

PAGES = {
    "index": {
        "path": {"en": "/", "ro": "/ro/"},
        "title": {"en": "Kipply: Phone Cleaner, Delete Duplicate Photos", "ro": "Kipply: Curățare Poze Telefon, Șterge Duplicate"},
        "desc": {
            "en": "Free phone cleaner for iPhone. Swipe to delete duplicate and similar photos, screenshots and videos and free up storage. Photos never leave your device.",
            "ro": "Curățare gratuită a pozelor pe iPhone. Glisezi ca să ștergi duplicate, poze similare, capturi de ecran și clipuri video și faci spațiu. Pozele rămân pe telefon.",
        },
        "og_desc": {
            "en": "Swipe left to delete, right to keep. Smart Clean finds duplicates, similar shots and screenshots on your device. Your photos never leave your iPhone.",
            "ro": "Glisezi la stânga ca să ștergi, la dreapta ca să păstrezi. Curățarea inteligentă găsește duplicate, poze similare și capturi de ecran. Pozele nu părăsesc iPhone-ul.",
        },
    },
    "support": {
        "path": {"en": "/support.html", "ro": "/ro/support.html"},
        "title": {"en": "Kipply Help Center: Phone Cleaner Support and FAQ", "ro": "Asistență Kipply: ajutor pentru curățarea pozelor"},
        "desc": {
            "en": "Help for the Kipply phone cleaner: delete duplicate photos and videos, Kipply Pro, free trial, restore purchases, privacy choices and troubleshooting.",
            "ro": "Ajutor pentru Kipply: șterge poze duplicate și clipuri video, Kipply Pro, perioada de probă, restaurarea achizițiilor și rezolvarea problemelor.",
        },
        "crumb": {"en": "Support", "ro": "Asistență"},
    },
    "privacy": {
        "path": {"en": "/privacy.html", "ro": "/ro/privacy.html"},
        "title": {"en": "Privacy Policy: Kipply Phone Cleaner", "ro": "Politica de confidențialitate: Kipply"},
        "desc": {
            "en": "Kipply privacy policy: your photos stay on your device, there is no account, and ads and analytics wait for your consent where the law requires it.",
            "ro": "Politica de confidențialitate Kipply: pozele rămân pe dispozitiv, nu există cont, iar reclamele și statisticile așteaptă consimțământul tău, unde legea o cere.",
        },
        "crumb": {"en": "Privacy Policy", "ro": "Politica de confidențialitate"},
    },
    "terms": {
        "path": {"en": "/terms.html", "ro": "/ro/terms.html"},
        "title": {"en": "Terms of Use: Kipply Phone Cleaner", "ro": "Termeni de utilizare: Kipply"},
        "desc": {
            "en": "Kipply terms of use: what the photo cleaner does, the free version, Kipply Pro subscriptions, ads, and your responsibility when deleting photos.",
            "ro": "Termenii de utilizare Kipply: ce face aplicația, versiunea gratuită, abonamentul Kipply Pro, reclamele și responsabilitatea ta când ștergi poze.",
        },
        "crumb": {"en": "Terms of Use", "ro": "Termeni de utilizare"},
    },
}
LOCALE = {"en": "en_US", "ro": "ro_RO"}

OG_ALT = {
    "en": "The Kipply phone cleaner Home tab on an iPhone, beside the words Swipe your camera roll clean.",
    "ro": "Ecranul principal Kipply pe un iPhone, lângă textul Curăță-ți galeria prin glisare.",
}
APP_DESC = {
    "en": "Free phone cleaner for iPhone and iPad. Swipe left to delete, right to keep. Smart Clean finds duplicate photos, similar shots, screenshots and videos on your device.",
    "ro": "Aplicație gratuită de curățare a pozelor pentru iPhone și iPad. Glisezi la stânga ca să ștergi, la dreapta ca să păstrezi. Curățarea inteligentă găsește duplicate, poze similare, capturi de ecran și clipuri video pe dispozitiv.",
}

RO_TEXT = {
    "Skip to content": "Sari la conținut",
    "Features": "Funcții",
    "Privacy": "Confidențialitate",
    "FAQ": "Întrebări",
    "Support": "Asistență",
    "Download": "Descarcă",
    "Phone cleaner for photos and videos on iPhone and iPad": "Curățare poze și video pe iPhone și iPad",
    "Swipe your camera roll": "Curăță-ți galeria",
    "clean.": "prin glisare.",
    "Kipply helps you delete the photos and videos you no longer need. Swipe left to delete, right to keep, up to skip. Your photos never leave your device.": "Kipply te ajută să ștergi pozele și clipurile video de care nu mai ai nevoie. Glisezi la stânga ca să ștergi, la dreapta ca să păstrezi, în sus ca să sari peste. Pozele tale nu părăsesc telefonul.",
    "Download on the App Store": "Descarcă din App Store",
    "See how it works": "Vezi cum funcționează",
    "Photos stay on your device": "Pozele rămân pe telefon",
    "Scanning runs on your iPhone": "Scanarea rulează pe iPhone",
    "No account": "Fără cont",
    "Nothing to sign up for": "Nu te înregistrezi nicăieri",
    "Free to use": "Gratuită",
    "25 swipes a day, with ads": "25 de glisări pe zi, cu reclame",
    "Duplicates": "Duplicate",
    "Videos": "Clipuri video",
    "Screenshots": "Capturi de ecran",
    "Similar": "Similare",
    "How Kipply works": "Cum funcționează Kipply",
    "Five tabs.": "Cinci file.",
    "One lighter library.": "O galerie mai ușoară.",
    "Home, Swipe, Smart, Deleted and Discover: the same screens you will find in the app, each doing one job.": "Acasă, Glisare, Smart, Șterse și Descoperă: aceleași ecrane din aplicație, fiecare cu o singură treabă.",
    "Swipe": "Glisare",
    "One photo": "O poză",
    "at a time.": "pe rând.",
    "Go through your library one photo at a time. Swipe left to delete, right to keep, or up to skip, and sort the pile newest, oldest or largest first.": "Treci prin galerie poză cu poză. Glisezi la stânga ca să ștergi, la dreapta ca să păstrezi sau în sus ca să sari peste, iar grămada o sortezi după cele mai noi, cele mai vechi sau cele mai mari.",
    "Undo takes back your last swipe": "Anulează ultima glisare",
    "Changed your mind? One tap.": "Te-ai răzgândit? O atingere.",
    "Newest, oldest or largest first": "Cele mai noi, vechi sau mari întâi",
    "Start where the space is.": "Începe de unde e spațiul.",
    "Videos too": "Și clipuri video",
    "Kipply works on photos and videos.": "Kipply lucrează cu poze și clipuri video.",
    "Smart Clean": "Curățare inteligentă",
    "Smart Clean finds": "Curățarea inteligentă găsește",
    "the clutter.": "dezordinea.",
    "Smart Clean scans your whole library on your device and gathers what you can clear. In each group of duplicates or similar shots, Kipply marks one to keep, and you can choose a different one with a tap.": "Curățarea inteligentă scanează toată galeria pe telefon și strânge ce poți șterge. În fiecare grup de duplicate sau poze similare, Kipply marchează una de păstrat, iar tu poți alege alta cu o atingere.",
    "Duplicates and similar photos": "Duplicate și poze similare",
    "Exact copies, and shots that look alike.": "Copii exacte și poze care seamănă între ele.",
    "Similar videos, and all your videos in one place": "Clipuri video similare și toate clipurile într-un singur loc",
    "Similar screenshots, and all your screenshots in one place": "Capturi de ecran similare și toate capturile într-un singur loc",
    "Deleted tab": "Fila Șterse",
    "You decide": "Tu decizi",
    "what goes.": "ce pleacă.",
    "Swiped photos wait in the Deleted tab until you decide to restore them or delete them for good. Once you confirm, they move to Recently Deleted in the Photos app, where iOS keeps them for 30 days.": "Pozele glisate la ștergere așteaptă în fila Șterse până decizi să le restaurezi sau să le ștergi definitiv. După ce confirmi, ajung în Șterse recent din aplicația Fotografii, unde iOS le păstrează 30 de zile.",
    "Restore with one tap": "Restaurezi dintr-o atingere",
    "Or swipe right on an item to bring it back.": "Sau glisezi la dreapta pe un element ca să-l readuci.",
    "Delete all, or just a selection": "Ștergi tot sau doar o selecție",
    "Nothing goes until you confirm": "Nimic nu pleacă până nu confirmi",
    "iOS asks before anything is removed.": "iOS cere acordul înainte să elimine ceva.",
    "Discover": "Descoperă",
    "Memories": "Amintiri",
    "worth keeping.": "care merită păstrate.",
    "Every day, Memory of the Day on Home brings back an older photo. Discover shows the photos you took on this date in past years and lets you browse your library month by month.": "În fiecare zi, Amintirea zilei de pe ecranul principal readuce o poză mai veche. Descoperă îți arată pozele făcute în această zi în anii trecuți și te lasă să răsfoiești galeria lună de lună.",
    "On This Date": "În această zi",
    "Photos from this day in past years.": "Poze din această zi, din anii trecuți.",
    "Month by month": "Lună de lună",
    "Browse your library and clear what you no longer need.": "Răsfoiești galeria și ștergi ce nu mai ai nevoie.",
    "Memory of the Day": "Amintirea zilei",
    "One older photo, every day, on Home.": "O poză mai veche în fiecare zi, pe ecranul principal.",
    "Statistics and streak": "Statistici și serie",
    "Cleaning that feels": "O curățenie care se simte",
    "like a game.": "ca un joc.",
    "Earn XP for every photo you review, level up, keep your daily streak going and complete daily and weekly challenges.": "Primești XP pentru fiecare poză verificată, urci în niveluri, îți ții seria zilnică și finalizezi provocări zilnice și săptămânale.",
    "Daily streak": "Serie zilnică",
    "Keep it going one session at a time.": "Ține-o vie, o sesiune pe rând.",
    "This week, this month, all time": "Săptămâna aceasta, luna aceasta, de la început",
    "What you have freed, reviewed, kept and deleted.": "Ce ai eliberat, verificat, păstrat și șters.",
    "Daily and weekly challenges": "Provocări zilnice și săptămânale",
    "Earn XP and level up.": "Câștigi XP și urci în niveluri.",
    "Two cards from the Home tab: your streak and level, and how much of your library you have reviewed.": "Două carduri din fila Acasă: seria și nivelul tău, și cât din galerie ai verificat.",
    "And on Home": "Și pe ecranul principal",
    "Everything": "Totul",
    "at a glance.": "dintr-o privire.",
    "Your space, in numbers": "Spațiul tău, în cifre",
    "Home shows how much space you can recover, how much you have saved so far and how much of your library you have reviewed.": "Ecranul principal arată cât spațiu poți recupera, cât ai economisit până acum și cât din galerie ai verificat.",
    "Library Insights": "Analiza bibliotecii",
    "Counts your blurry photos, screenshots, Live Photos and photos without people, and takes you straight into a swipe session for any of them.": "Numără pozele neclare, capturile de ecran, Live Photos și pozele fără persoane, și te duce direct într-o sesiune de glisare pentru oricare dintre ele.",
    "Siri and Control Center": "Siri și Centrul de control",
    "Ask Siri to clean your photos or scan your library, or add the Free Up Space control to Control Center.": "Roagă Siri să-ți curețe pozele sau să scaneze galeria, ori adaugă controlul Eliberează spațiu în Centrul de control.",
    "iPhone and iPad": "iPhone și iPad",
    "Kipply requires iOS 17 or later and works on iPhone and iPad.": "Kipply necesită iOS 17 sau mai nou și merge pe iPhone și pe iPad.",
    "Private by design": "Confidențială prin construcție",
    "Your photos never": "Pozele tale nu",
    "leave your device.": "părăsesc telefonul.",
    "Kipply analyzes your photos on your device. Your photos and videos never leave it, and there is no account to create. Where the law requires consent, ads and analytics wait for your answer.": "Kipply îți analizează pozele pe dispozitiv. Pozele și clipurile tale nu îl părăsesc, iar nu trebuie să creezi niciun cont. Unde legea cere consimțământ, reclamele și statisticile așteaptă răspunsul tău.",
    "Read the Privacy Policy": "Citește Politica de confidențialitate",
    "On-device scanning": "Scanare pe dispozitiv",
    "Duplicates, similar shots and screenshots are found on your iPhone.": "Duplicatele, pozele similare și capturile de ecran sunt găsite pe iPhone.",
    "No account, no sign-in": "Fără cont, fără autentificare",
    "We never ask for your name or email address.": "Nu îți cerem niciodată numele sau adresa de email.",
    "Consent first": "Mai întâi consimțământul",
    "Where the law requires it, ads and analytics wait for your answer.": "Unde legea o cere, reclamele și statisticile așteaptă răspunsul tău.",
    "Questions,": "Întrebări,",
    "answered.": "cu răspunsuri.",
    "Is Kipply free?": "Este Kipply gratuită?",
    "Kipply is free to use, with 25 swipes a day, a limit on how many items you can delete at once, and ads. Kipply Pro is an auto-renewing subscription that removes both limits and the ads.": "Kipply se poate folosi gratuit, cu 25 de glisări pe zi, o limită pentru câte elemente ștergi odată și reclame. Kipply Pro este un abonament cu reînnoire automată care elimină ambele limite și reclamele.",
    "It is offered weekly or monthly at the price shown in the app for your region. If your Apple Account is eligible for a free trial, currently 3 days, its length is shown before you subscribe.": "Se oferă săptămânal sau lunar, la prețul afișat în aplicație pentru regiunea ta. Dacă Apple Account-ul tău este eligibil pentru o perioadă de probă gratuită, în prezent de 3 zile, durata ei apare înainte să te abonezi.",
    "Do my photos leave my device?": "Pozele mele părăsesc telefonul?",
    "No. Scanning, comparing and deleting all happen on your iPhone or iPad. Kipply has no account, and we have no access to your photos or videos.": "Nu. Scanarea, compararea și ștergerea se fac pe iPhone sau iPad. Kipply nu are cont, iar noi nu avem acces la pozele sau clipurile tale.",
    "What happens when I delete something?": "Ce se întâmplă când șterg ceva?",
    "Items you swipe left wait in the Deleted tab, still in your Photos library, until you confirm. When you confirm, iOS asks for your permission and moves them to the Recently Deleted album in the Photos app, where Apple keeps them for 30 days.": "Elementele glisate la stânga așteaptă în fila Șterse, încă în biblioteca Fotografii, până confirmi. Când confirmi, iOS îți cere acordul și le mută în albumul Șterse recent din aplicația Fotografii, unde Apple le păstrează 30 de zile.",
    "After that they are gone for good, so back up anything you want to keep first.": "După aceea dispar definitiv, așa că salvează mai întâi ce vrei să păstrezi.",
    "Does Kipply clean caches, app data or system storage?": "Curăță Kipply memoria cache, datele aplicațiilor sau spațiul de sistem?",
    "No. Kipply works only on the photos and videos in your Photos library.": "Nu. Kipply lucrează doar cu pozele și clipurile video din biblioteca ta Fotografii.",
    "Which devices does Kipply support?": "Ce dispozitive suportă Kipply?",
    "Does Kipply work offline?": "Merge Kipply fără internet?",
    "Yes, for photos and videos stored on your device. Swiping, scanning and deleting work without an internet connection. You need a connection to load photos stored only in iCloud, to buy or restore Kipply Pro, and for ads to load.": "Da, pentru pozele și clipurile stocate pe dispozitiv. Glisarea, scanarea și ștergerea merg fără conexiune la internet. Ai nevoie de conexiune ca să încarci pozele stocate doar în iCloud, ca să cumperi sau să restaurezi Kipply Pro și ca să se încarce reclamele.",
    "How do I cancel Kipply Pro?": "Cum anulez Kipply Pro?",
    "Subscriptions are managed by Apple. Open the Settings app, tap your name, then Subscriptions, then Kipply. If you cancel, Kipply Pro stays active until the end of the period you have already paid for. Deleting the app does not cancel a subscription.": "Abonamentele sunt gestionate de Apple. Deschide aplicația Setări, atinge numele tău, apoi Abonamente, apoi Kipply. Dacă anulezi, Kipply Pro rămâne activ până la sfârșitul perioadei deja plătite. Ștergerea aplicației nu anulează abonamentul.",
    "More answers in the Help Center": "Mai multe răspunsuri în Centrul de ajutor",
    "Free to download": "Descărcare gratuită",
    "Get your": "Recapătă-ți",
    "space back.": "spațiul.",
    "Start with today's 25 swipes. Your photos stay on your device the whole time.": "Începe cu cele 25 de glisări de azi. Pozele tale rămân tot timpul pe telefon.",
    "Requires iOS 17 or later. iPhone and iPad.": "Necesită iOS 17 sau mai nou. iPhone și iPad.",
    "Photo and video cleaner for iPhone and iPad. Swipe to delete, on your device.": "Curățare poze și video pentru iPhone și iPad. Glisezi ca să ștergi, direct pe dispozitiv.",
    "App Store": "App Store",
    "Legal": "Informații juridice",
    "Privacy Policy": "Politica de confidențialitate",
    "Terms of Service": "Termeni de utilizare",
    "Help Center": "Centrul de ajutor",
    "More apps by Visto Apps": "Mai multe aplicații Visto Apps",
    "&copy; 2026 Visto Apps, the brand of Darius Cirjan": "&copy; 2026 Visto Apps, brandul lui Darius Cirjan",
    "Made by": "Creat de",
    "Kipply home": "Kipply, pagina principală",
    "Primary": "Principal",
    "Open menu": "Deschide meniul",
    "Kipply": "Kipply",
    "Visto Apps": "Visto Apps",
    "Contents": "Cuprins",
    "The Kipply phone cleaner Home tab on an iPhone: a day streak and level card, how much storage you can recover, Quick Actions for duplicates, videos, screenshots and similar photos, and a Memory of the Day.": "Fila Acasă din Kipply pe un iPhone: cardul cu seria zilnică și nivelul, cât spațiu poți recupera, Acțiuni rapide pentru duplicate, clipuri video, capturi de ecran și poze similare, și Amintirea zilei.",
    "The Swipe tab in Kipply: a photo card being dragged to the left with a Delete label, and Delete, Skip and Keep buttons below it.": "Fila Glisare din Kipply: o poză trasă spre stânga cu eticheta Șterge, și butoanele Șterge, Omite și Păstrează dedesubt.",
    "Smart Clean in Kipply showing groups of similar photos, with one photo in each group marked Best and the others selected for deletion.": "Curățarea inteligentă din Kipply cu grupuri de poze similare: o poză din fiecare grup e marcată Recomandat, iar celelalte sunt selectate pentru ștergere.",
    "The Deleted tab in Kipply with three items selected and Restore 3 and Delete 3 buttons at the bottom.": "Fila Șterse din Kipply cu trei elemente selectate și butoanele Restaurează 3 și Șterge 3 în partea de jos.",
    "The Discover tab in Kipply with an On This Date card and photos grouped by month.": "Fila Descoperă din Kipply cu un card În această zi și poze grupate pe luni.",
    "Kipply's streak card: a 1 day streak, Level 2 with 160 XP, and a progress bar reading 40 XP to Level 3.": "Cardul cu seria din Kipply: o serie de 1 zi, nivelul 2 cu 160 XP și o bară de progres cu 40 XP până la nivelul 3.",
    "Kipply's progress card: Library Organized at 40 percent with Keep going, and 0 MB saved so far.": "Cardul de progres din Kipply: biblioteca organizată în proporție de 40 la sută, cu mesajul Continuă!, și 0 MB economisiți până acum.",
}


def esc(s):
    return html.escape(s, quote=True)


def lang_url(page, lang):
    return BASE + PAGES[page]["path"][lang]


def faq_from_html(doc):
    """FAQPage built only from the visible <details> FAQ of the page."""
    items = []
    for m in re.finditer(r'<details class="glass faq">\s*<summary>(.*?)</summary>\s*<div class="faq-body">(.*?)</div>\s*</details>', doc, re.S):
        q = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip()
        a = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(2)))).strip()
        items.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})
    return {"@type": "FAQPage", "mainEntity": items}


def head_for(page, lang, body_html):
    p = PAGES[page]
    other = "ro" if lang == "en" else "en"
    url = lang_url(page, lang)
    title = p["title"][lang]
    desc = p["desc"][lang]
    og_desc = p.get("og_desc", p["desc"])[lang]
    assert len(title) <= 60, (page, lang, title, len(title))
    assert 120 <= len(desc) <= 160, (page, lang, len(desc))
    pre = []
    if page == "index":
        pre.append('<link rel="preload" as="image" href="/img/screens/home-720.webp" imagesrcset="/img/screens/home-360.webp 360w, /img/screens/home-540.webp 540w, /img/screens/home-720.webp 720w" imagesizes="(min-width: 900px) 340px, 70vw" fetchpriority="high">')
    pre.append('<link rel="preload" href="/assets/fonts/instrument-serif.woff2" as="font" type="font/woff2" crossorigin>')
    pre.append('<link rel="preload" href="/assets/fonts/inter.woff2" as="font" type="font/woff2" crossorigin>')

    org = {"@type": "Organization", "@id": "https://vistoapps.com/#org", "name": "Visto Apps", "url": "https://vistoapps.com",
           "email": MAIL, "founder": {"@type": "Person", "name": "Darius Cirjan"}}
    site = {"@type": "WebSite", "@id": BASE + "/#site", "url": BASE + "/", "name": "Kipply",
            "publisher": {"@id": "https://vistoapps.com/#org"}, "inLanguage": ["en", "ro"]}
    graph = []
    if page == "index":
        # No aggregateRating: the App Store lookup returns a single rating, not representative.
        graph.append({
            "@type": "MobileApplication", "@id": BASE + "/#app", "name": "Kipply",
            "alternateName": "Kipply: Phone Cleaner",
            "description": APP_DESC[lang], "operatingSystem": "iOS 17.0 or later",
            "applicationCategory": "UtilitiesApplication", "url": url,
            "image": BASE + "/img/icon.webp",
            "screenshot": [f"{BASE}/img/screens/{s}-720.webp" for s in SCREENS],
            "installUrl": STORE, "downloadUrl": STORE,
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
            "inLanguage": lang,
            "author": {"@id": "https://vistoapps.com/#org"}, "publisher": {"@id": "https://vistoapps.com/#org"},
        })
        graph += [org, site, faq_from_html(body_html)]
    else:
        home = BASE + PAGES["index"]["path"][lang]
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Kipply", "item": home},
            {"@type": "ListItem", "position": 2, "name": p["crumb"][lang], "item": url}]})
        graph.append({"@type": "WebPage", "@id": url + "#page", "url": url, "name": title, "inLanguage": lang,
                      "isPartOf": {"@id": BASE + "/#site"}, "publisher": {"@id": "https://vistoapps.com/#org"}})
        graph += [org, site]
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1).replace("</", "<\\/")
    pre_html = "\n    ".join(pre)

    return f"""<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <meta name="apple-itunes-app" content="app-id={APP_ID}">
    <title>{esc(title)}</title>
    <meta name="description" content="{esc(desc)}">
    <meta name="color-scheme" content="dark">
    <meta name="theme-color" content="#153464" data-scrolled="#050b1c">
    <link rel="canonical" href="{url}">
    <link rel="alternate" hreflang="en" href="{lang_url(page, 'en')}">
    <link rel="alternate" hreflang="ro" href="{lang_url(page, 'ro')}">
    <link rel="alternate" hreflang="x-default" href="{lang_url(page, 'en')}">

    <!-- Social -->
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="Kipply">
    <meta property="og:url" content="{url}">
    <meta property="og:title" content="{esc(title)}">
    <meta property="og:description" content="{esc(og_desc)}">
    <meta property="og:image" content="{BASE}/og-image.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:image:alt" content="{esc(OG_ALT[lang])}">
    <meta property="og:locale" content="{LOCALE[lang]}">
    <meta property="og:locale:alternate" content="{LOCALE[other]}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{esc(title)}">
    <meta name="twitter:description" content="{esc(og_desc)}">
    <meta name="twitter:image" content="{BASE}/og-image.png">

    <!-- Icons -->
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png">
    <link rel="apple-touch-icon" href="/apple-touch-icon.png">

    <!-- Same-origin only: self-hosted fonts, no third-party scripts. -->
    {pre_html}
    <link rel="stylesheet" href="/styles.css?v={ASSET_V}">
    <script>document.documentElement.classList.add('js');</script>

    <script type="application/ld+json">
{ld}
    </script>
</head>"""


def switch_link(page, lang):
    other = "ro" if lang == "en" else "en"
    label = {"ro": ("RO", "Română (RO)"), "en": ("EN", "English (EN)")}[other]
    return (f'<a class="lang-switch" href="{PAGES[page]["path"][other]}" hreflang="{other}" lang="{other}" '
            f'aria-label="{label[1]}">{label[0]}</a>')


def patch_en_body(doc, page):
    """Idempotent English body edits: switch link, toggle labels, footer link, keyword copy."""
    if 'class="lang-switch"' not in doc:
        doc = doc.replace('<div class="nav-actions">', '<div class="nav-actions">\n                    ' + switch_link(page, "en"), 1)
    if "data-label-open" not in doc:
        doc = doc.replace('aria-controls="navmenu">', 'aria-controls="navmenu" data-label-open="Open menu" data-label-close="Close menu">', 1)
    if "vistoapps.com/apps.html" not in doc:
        anchor = f'<li><a href="mailto:{MAIL}">{MAIL}</a></li>'
        doc = doc.replace(anchor, anchor + '\n                        <li><a href="https://vistoapps.com/apps.html">More apps by Visto Apps</a></li>', 1)
    doc = doc.replace("Photo and video cleaner for iPhone and iPad\n                    </p>", "Phone cleaner for photos and videos on iPhone and iPad\n                    </p>")
    doc = doc.replace('alt="The Kipply Home tab on an iPhone:', 'alt="The Kipply phone cleaner Home tab on an iPhone:')
    return doc


def translate_body(doc):
    """Translate text nodes and alt/aria-label values with RO_TEXT; report leftovers."""
    missing = []

    def tr_text(m):
        raw = m.group(1)
        s = raw.strip()
        if not s or not re.search(r"[A-Za-z]", s) or "@" in s or s in ("RO", "EN"):
            return m.group(0)
        if s in RO_TEXT:
            return ">" + raw.replace(s, RO_TEXT[s]) + "<"
        missing.append(s)
        return m.group(0)

    def tr_attr(m):
        name, val = m.group(1), m.group(2)
        if val in RO_TEXT:
            return f'{name}="{RO_TEXT[val]}"'
        if name == "alt" and re.search(r"[A-Za-z]{3}", val):
            missing.append(val)
        return m.group(0)

    b0 = doc.index("<body>")
    body = re.sub(r">([^<>]+)<", tr_text, doc[b0:])
    body = re.sub(r'\b(alt|aria-label)="([^"]*)"', tr_attr, body)
    return doc[:b0] + body, missing


def ro_paths(doc):
    """RO pages live in /ro/: make asset URLs root-absolute, use RO toggle labels."""
    def fix(m):
        attr, val = m.group(1), m.group(2)
        val = re.sub(r"(^|(?<=, ))img/", "/img/", val)
        if re.match(r"(styles\.css|script\.js|favicon|apple-touch)", val):
            val = "/" + val
        return f'{attr}="{val}"'
    doc = re.sub(r'\b(src|srcset|imagesrcset|href)="([^"]*)"', fix, doc)
    return doc.replace('data-label-open="Open menu" data-label-close="Close menu"', 'data-label-open="Deschide meniul" data-label-close="Închide meniul"')


def build_page(page):
    src_path = ROOT / f"{page}.html"
    en = patch_en_body(src_path.read_text(), page)
    m = re.search(r"<head>.*?</head>", en, re.S)
    en = en[:m.start()] + head_for(page, "en", en[m.end():]) + en[m.end():]
    en = re.sub(r'(<script src=")/?script\.js[^"]*"', rf'\1/script.js?v={ASSET_V}"', en)
    src_path.write_text(en)

    ro = en.replace('<html lang="en">', '<html lang="ro">')
    region = None
    if page == "support":
        a = ro.index("<h1>Support &amp; Help Center</h1>")
        b = ro.index("        </div>\n        </div>\n    </main>")
        region = (a, b, (ROOT / "_tools" / "ro_support_body.html").read_text().replace("@@MAIL@@", MAIL))
    elif page in ("privacy", "terms"):
        a = ro.index("<!--legal:start-->")
        b = ro.index("<!--legal:end-->") + len("<!--legal:end-->")
        region = (a, b, (FRAG / f"{page}.ro.html").read_text().strip())
    if region:
        ro = ro[:region[0]] + "@@REGION@@" + ro[region[1]:]
    ro, missing = translate_body(ro)
    if region:
        ro = ro.replace("@@REGION@@", region[2])
    ro = re.sub(r'<a class="lang-switch"[^>]*>[^<]*</a>', switch_link(page, "ro"), ro, 1)
    ro = ro_paths(ro)
    m = re.search(r"<head>.*?</head>", ro, re.S)
    ro = ro[:m.start()] + head_for(page, "ro", ro[m.end():]) + ro[m.end():]
    ro = ro.replace('<a class="skip-link" href="#main">Skip to content</a>', '<a class="skip-link" href="#main">Sari la conținut</a>')
    (ROOT / "ro").mkdir(exist_ok=True)
    (ROOT / "ro" / ("index.html" if page == "index" else f"{page}.html")).write_text(ro)
    return missing


def write_sitemap():
    rows = ['<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for page in PAGES:
        for lang in ("en", "ro"):
            rows += ["  <url>", f"    <loc>{lang_url(page, lang)}</loc>", f"    <lastmod>{LASTMOD}</lastmod>",
                     f'    <xhtml:link rel="alternate" hreflang="en" href="{lang_url(page, "en")}"/>',
                     f'    <xhtml:link rel="alternate" hreflang="ro" href="{lang_url(page, "ro")}"/>',
                     f'    <xhtml:link rel="alternate" hreflang="x-default" href="{lang_url(page, "en")}"/>', "  </url>"]
    rows.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(rows) + "\n")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")


def main():
    if FRAG is None:
        sys.exit("usage: build_seo.py <fragments dir>")
    for page in PAGES:
        missing = build_page(page)
        if missing:
            print("UNTRANSLATED in", page)
            for s in sorted(set(missing)):
                print("   ", repr(s[:100]))
    write_sitemap()
    print("done")


if __name__ == "__main__":
    main()
