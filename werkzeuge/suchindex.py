"""Erzeugt suchindex.json für die Blog-Suche auf blog.html.

Aufruf (im Ordner website):  python werkzeuge/suchindex.py
Nach jedem neuen oder geänderten Beitrag einmal ausführen und suchindex.json mit hochladen.

Welche Beiträge drin sind, bestimmt blog.html (die Blog-Karten, in deren Reihenfolge).
Pro Beitrag werden Titel, Kurzbeschreibung und alle Abschnitte (h1/h2/h3 + Text bis zur
nächsten Überschrift) sowie jede FAQ-Frage mit Antwort als eigener Abschnitt gespeichert.
"""
import json, re, html, datetime, pathlib
from html.parser import HTMLParser

SITE = pathlib.Path(__file__).resolve().parent.parent
MAX_TEXT = 2200
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}
SKIP_TAGS = {'script', 'style', 'nav', 'figure', 'svg', 'button', 'noscript', 'template'}
SKIP_CLASSES = {'blog-breadcrumb', 'blog-byline', 'blog-author-card', 'article-kicker', 'blog-actions',
                'calc', 'related', 'blog-toc', 'chapter-list', 'blog-disclaimer', 'video-box', 'blog-video-link',
                'cta-band', 'sim', 'planbox-sektion'}
SKIP_IDS = {'weiterlesen'}  # Linklisten zu anderen Beiträgen
BLOCK = {'p', 'li', 'div', 'td', 'th', 'tr', 'h1', 'h2', 'h3', 'h4', 'section', 'details', 'summary', 'ul', 'ol', 'table', 'blockquote', 'dd', 'dt'}


def clean(s):
    return re.sub(r'\s+', ' ', s).strip()


class Post(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []          # [tag, skip, section_id]
        self.in_main = False
        self.chunks = []
        self.cur = None
        self.head_tag = None     # h1/h2/h3/summary während die Überschrift gelesen wird
        self.head_id = None
        self.desc = ''

    def skipping(self):
        return any(s[1] for s in self.stack)

    def section_id(self):
        for s in reversed(self.stack):
            if s[2]:
                return s[2]
        return ''

    def new_chunk(self, kind, anchor):
        self.cur = {'a': anchor, 'h': '', 'k': kind, 'x': ''}
        self.chunks.append(self.cur)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'meta' and a.get('name') == 'description':
            self.desc = a.get('content', '')
        if tag == 'main':
            self.in_main = True
        if tag in VOID:
            if tag == 'br' and self.cur is not None:
                self.cur['x'] += ' '
            return
        cls = set((a.get('class') or '').split())
        skip = tag in SKIP_TAGS or bool(cls & SKIP_CLASSES) or a.get('id') in SKIP_IDS
        sid = a.get('id') if tag == 'section' else None
        self.stack.append([tag, skip, sid])
        if not self.in_main or self.skipping():
            return
        if tag in ('h1', 'h2', 'h3', 'summary'):
            kind = {'h1': 'intro', 'summary': 'faq'}.get(tag, tag)
            anchor = a.get('id') or ('' if tag == 'h1' else self.section_id())
            self.new_chunk(kind, anchor)
            self.head_tag = tag
        elif tag in BLOCK and self.cur is not None:
            self.cur['x'] += ' '

    def handle_endtag(self, tag):
        if tag == 'main':
            self.in_main = False
        if tag in VOID:
            return
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break
        if tag == self.head_tag:
            self.head_tag = None
        if tag in BLOCK and self.cur is not None:
            self.cur['x'] += ' '

    def handle_data(self, data):
        if not self.in_main or self.skipping() or self.cur is None:
            return
        if self.head_tag:
            self.cur['h'] += data
        else:
            self.cur['x'] += data


def blog_cards():
    s = (SITE / 'blog.html').read_text(encoding='utf-8')
    cards = []
    for m in re.finditer(r'<article class="blog-card">(.*?)</article>', s, re.S):
        c = m.group(1)
        t = re.search(r'class="blog-card-title" href="([^"]+)">(.*?)</a>', c, re.S)
        p = re.search(r'</h3>\s*<p>(.*?)</p>', c, re.S)
        tags = re.findall(r'<span>([^<]+)</span>', re.search(r'<div class="blog-meta">(.*?)</div>', c, re.S).group(1)) if 'blog-meta' in c else []
        cards.append({'u': t.group(1), 't': clean(html.unescape(re.sub('<[^>]+>', '', t.group(2)))),
                      'd': clean(html.unescape(re.sub('<[^>]+>', '', p.group(1)))) if p else '',
                      'tags': [html.unescape(x) for x in tags]})
    return cards


def main():
    posts = []
    for card in blog_cards():
        f = SITE / card['u']
        if not f.exists():
            print('fehlt:', card['u'])
            continue
        p = Post()
        p.feed(f.read_text(encoding='utf-8'))
        chunks = []
        for c in p.chunks:
            h, x = clean(c['h']), clean(c['x'])
            if not h and not x:
                continue
            if len(x) > MAX_TEXT:
                x = x[:MAX_TEXT].rsplit(' ', 1)[0] + ' …'
            chunks.append({'a': c['a'], 'h': h, 'k': c['k'], 'x': x})
        posts.append({**card, 'm': clean(p.desc), 'c': chunks})
        print(f"{card['u']}: {len(chunks)} Abschnitte")
    out = {'stand': datetime.date.today().isoformat(), 'posts': posts}
    (SITE / 'suchindex.json').write_text(json.dumps(out, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    print('suchindex.json:', round((SITE / 'suchindex.json').stat().st_size / 1024), 'KB,', len(posts), 'Beiträge')


if __name__ == '__main__':
    main()
