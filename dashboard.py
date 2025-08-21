# app.py
from flask import Flask, request, render_template_string, url_for
import re
from datetime import datetime

app = Flask(__name__)

# ----- Data proyek (ditambah dari GitHub kamu) -----
PROJECTS = [
    # Ganti 's' -> DigitalConvert
    {
        "title": "DigitalConvert",
        "subtitle": "Konversi pulsa/paylater/voucher + Admin panel",
        "description": "Web app untuk konversi pulsa, paylater, dan voucher dengan modul kategori, produk, dan chart KPI.",
        "tech": ["Node.js", "Express", "EJS", "MySQL"],
        "tags": ["web", "fintech", "dashboard"],
        "links": {"repo": "https://github.com/davasangkara/s", "demo": ""},
        "status": "Active",
        "emoji": "💳",
        "last_updated": "",
    },
    {
        "title": "Object Tracking",
        "subtitle": "Pelacakan objek (vision)",
        "description": "Eksperimen pelacakan objek untuk video/stream. Fokus ke computer vision.",
        "tech": ["Python", "OpenCV"],
        "tags": ["computer-vision", "opencv", "tracking"],
        "links": {"repo": "https://github.com/davasangkara/object_tracking", "demo": ""},
        "status": "Active",
        "emoji": "🎯",
        "last_updated": "",
    },
    {
        "title": "lokasi-selecction ",
        "subtitle": "Eksperimen pemilihan lokasi / peta",
        "description": "UI/UX pemetaan dan seleksi lokasi. Cocok untuk prototipe fitur geolocation.",
        "tech": ["Python", "Flask", "Leaflet"],
        "tags": ["map", "geolocation", "flask"],
        "links": {"repo": "https://untukmuonlyu.onrender.com", "demo": ""},
        "status": "Active",
        "emoji": "📍",
        "last_updated": "",
    },
    {
        "title": "skintonee",
        "subtitle": "Deteksi skintone (vision)",
        "description": "Eksperimen deteksi skintone dengan pengolahan citra.",
        "tech": ["Python", "OpenCV"],
        "tags": ["vision", "opencv"],
        "links": {"repo": "https://github.com/davasangkara/skintonee", "demo": ""},
        "status": "Active",
        "emoji": "🎨",
        "last_updated": "",
    },
    # Ganti 'project_skripsi' -> aplikasi keuangan AI
    {
        "title": "Aplikasi Keuangan AI",
        "subtitle": "Project skripsi — analitik keuangan berbasis AI",
        "description": "Aplikasi keuangan yang memanfaatkan AI/ML untuk insight dan otomasi sederhana.",
        "tech": ["Python", "ML"],
        "tags": ["finance", "ai", "research"],
        "links": {"repo": "https://github.com/davasangkara/project_skripsi", "demo": ""},
        "status": "Active",
        "emoji": "🧠",
        "last_updated": "",
    },
    {
        "title": "Real Estate Prediction — ANN",
        "subtitle": "Prediksi harga properti dengan Artificial Neural Network",
        "description": "Eksperimen regresi untuk prediksi harga real estate menggunakan ANN.",
        "tech": ["Python", "ANN"],
        "tags": ["ml", "regression"],
        "links": {"repo": "https://github.com/davasangkara/Real-Estate-Prediction---ANN", "demo": ""},
        "status": "Active",
        "emoji": "🏠",
        "last_updated": "",
    },
    {
        "title": "klasikasi-sea",
        "subtitle": "Eksperimen klasifikasi",
        "description": "Percobaan model klasifikasi (SEA).",
        "tech": ["Python", "ML"],
        "tags": ["classification"],
        "links": {"repo": "https://github.com/davasangkara/klasikasi-sea", "demo": ""},
        "status": "Active",
        "emoji": "🌊",
        "last_updated": "",
    },
    {
        "title": "Classification Fruits",
        "subtitle": "Klasifikasi buah",
        "description": "Eksperimen klasifikasi gambar buah untuk pembelajaran mesin.",
        "tech": ["Python", "ML"],
        "tags": ["ml", "image"],
        "links": {"repo": "https://github.com/davasangkara/Classification_Fruits", "demo": ""},
        "status": "Active",
        "emoji": "🍎",
        "last_updated": "",
    },
    {
        "title": "Association Market Analyst (MBA)",
        "subtitle": "Analisis market basket (association rules)",
        "description": "Eksperimen association rule mining untuk analisis keranjang belanja.",
        "tech": ["Python"],
        "tags": ["association-rules", "market-basket"],
        "links": {"repo": "https://github.com/davasangkara/Association_Market_Analyst_MBA", "demo": ""},
        "status": "Active",
        "emoji": "🛒",
        "last_updated": "",
    },
]

SITE_TITLE = "Project Dashboard"
AUTHOR = "M Daffa Alfikri"  # opsional ganti namamu

GITHUB_PROFILE = "https://github.com/davasangkara"


def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"[\s-]+", "-", s).strip("-")
    return s


def parse_date(s: str):
    try:
        return datetime.fromisoformat(s) if s else None
    except Exception:
        return None


# Derive fields (slug, parsed date) & collect tags
for p in PROJECTS:
    p["slug"] = slugify(p["title"])
    p["last_updated_dt"] = parse_date(p.get("last_updated"))
ALL_TAGS = sorted({t for p in PROJECTS for t in p.get("tags", [])})


def matches_query(p, q):
    if not q:
        return True
    q = q.lower()
    hay = " ".join([
        p.get("title", ""), p.get("subtitle", ""), p.get("description", ""),
        " ".join(p.get("tech", [])), " ".join(p.get("tags", [])),
    ]).lower()
    return q in hay


def matches_tag(p, tag):
    if not tag:
        return True
    return tag.lower() in [t.lower() for t in p.get("tags", [])]


# ---------- Templates (inline, aesthetic) ----------
BASE_HEAD = """
<!doctype html>
<html lang="id" class="h-full">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ SITE_TITLE }}</title>
  <meta name="theme-color" content="#0b1220">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;800&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = { darkMode: 'class', theme: { extend: {
      fontFamily: { inter: ['Inter','ui-sans-serif','system-ui'] },
      boxShadow: { glow: '0 10px 30px rgba(14,165,233,.25), inset 0 0 0 1px rgba(14,165,233,.35)' },
      keyframes: {
        floaty: { '0%,100%': { transform: 'translateY(0px)' }, '50%': { transform: 'translateY(-10px)' } },
        fadeup: { '0%': { opacity: 0, transform: 'translateY(12px)' }, '100%': { opacity: 1, transform: 'translateY(0)' } },
        shine: { '0%': { backgroundPosition: '0% 50%' }, '100%': { backgroundPosition: '100% 50%' } }
      },
      animation: { floaty: 'floaty 6s ease-in-out infinite', fadeup: 'fadeup .5s ease forwards', shine: 'shine 6s linear infinite' }
    }}};
    (function(){
      const s = localStorage.getItem('theme');
      if (s==='light') document.documentElement.classList.remove('dark');
      else document.documentElement.classList.add('dark');
    })();
  </script>
  <style>
    html,body{font-family:Inter,ui-sans-serif,system-ui}
    *{-webkit-tap-highlight-color:transparent}
    .glass{backdrop-filter:blur(10px);background:rgba(11,18,32,.55)}
    .chip{display:inline-flex;align-items:center;padding:.4rem .75rem;border-radius:9999px;border:1px solid rgb(51 65 85);font-size:.75rem}
    .clamp-2{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
    .gradient-border{position:relative}
    .gradient-border::before{
      content:"";position:absolute;inset:0;border-radius:1rem;padding:1px;
      background:linear-gradient(135deg, rgba(34,211,238,.7), rgba(168,85,247,.7), rgba(249,115,22,.7));
      -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
      -webkit-mask-composite: xor; mask-composite: exclude;
      pointer-events:none;
    }
    .reveal{opacity:0;transform:translateY(12px)}
    .reveal.show{opacity:1;transform:none;transition:all .5s ease}
  </style>
</head>
<body class="min-h-full bg-slate-950 text-slate-100">
  <!-- Background blobs -->
  <div class="pointer-events-none fixed inset-0 -z-10 overflow-hidden">
    <div class="absolute -top-16 -left-16 h-64 w-64 rounded-full blur-3xl opacity-25 animate-floaty"
         style="background:radial-gradient(45% 45% at 50% 50%, rgba(14,165,233,.8), transparent 60%)"></div>
    <div class="absolute -bottom-24 -right-10 h-72 w-72 rounded-full blur-3xl opacity-25 animate-floaty"
         style="animation-delay:1.2s;background:radial-gradient(45% 45% at 50% 50%, rgba(168,85,247,.8), transparent 60%)"></div>
    <div class="absolute top-1/3 -right-24 h-80 w-80 rounded-full blur-3xl opacity-20 animate-floaty"
         style="animation-delay:2.1s;background:radial-gradient(45% 45% at 50% 50%, rgba(249,115,22,.8), transparent 60%)"></div>
  </div>

  <header class="sticky top-0 z-30 border-b border-slate-800/70 glass">
    <div class="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between gap-3">
      <a href="{{ url_for('home') }}" class="flex items-center gap-2">
        <span class="inline-flex h-8 w-8 rounded-xl items-center justify-center font-extrabold shadow-glow"
              style="background:linear-gradient(135deg,#22d3ee,#a855f7,#f97316);background-size:200% 200%"></span>
        <div class="leading-tight">
          <div class="font-semibold tracking-tight">{{ SITE_TITLE }}</div>
          <div class="text-[11px] text-slate-400">by {{ AUTHOR }}</div>
        </div>
      </a>
      <div class="flex items-center gap-2">
        <a href="{{ github }}" target="_blank" class="px-3 py-1.5 rounded-lg border border-slate-700 text-xs hover:border-cyan-600">Profil GitHub</a>
        <button id="themeBtn" class="px-3 py-1.5 rounded-lg border border-slate-700 text-xs hover:border-cyan-600">Toggle Theme</button>
      </div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto px-4 py-8">
"""

BASE_FOOT = """
  </main>
  <footer class="max-w-7xl mx-auto px-4 py-10 text-xs text-slate-400">
    <span id="copy"></span>
  </footer>
  <script>
    // Theme toggle
    document.getElementById('themeBtn').addEventListener('click', function(){
      const isDark = document.documentElement.classList.toggle('dark');
      localStorage.setItem('theme', isDark ? 'dark' : 'light');
    });

    // "/" focuses search
    const searchEl = document.getElementById('searchInput');
    window.addEventListener('keydown', (e)=>{ if(e.key==='/'){ e.preventDefault(); searchEl?.focus(); }});

    // Live search (debounced, client-side filter + update URL)
    function debounce(fn, d){ let t; return (...a)=>{ clearTimeout(t); t=setTimeout(()=>fn(...a), d)}}
    const syncURL = debounce((val)=> {
      const u = new URL(window.location);
      if (val) u.searchParams.set('q', val); else u.searchParams.delete('q');
      history.replaceState(null,'',u);
      const cards = document.querySelectorAll('[data-card]');
      const v = val.trim().toLowerCase();
      let any=false;
      cards.forEach(c=>{
        const hay = c.dataset.hay || "";
        const hide = v && !hay.includes(v);
        c.classList.toggle('hidden', hide);
        if(!hide) any=true;
      });
      const es = document.getElementById('emptyState');
      if (es) es.classList.toggle('hidden', any);
    }, 150);
    searchEl?.addEventListener('input', e=> syncURL(e.target.value));

    // Tag chips behaviour
    document.querySelectorAll('[data-tag]').forEach(ch=>{
      ch.addEventListener('click', (e)=>{
        e.preventDefault();
        const tag = ch.dataset.tag;
        const u = new URL(window.location);
        if (u.searchParams.get('tag') === tag) u.searchParams.delete('tag');
        else u.searchParams.set('tag', tag);
        window.location = u.toString();
      });
    });

    // Reveal on scroll
    const io = new IntersectionObserver((entries)=>{
      entries.forEach(en=>{ if(en.isIntersecting){ en.target.classList.add('show'); io.unobserve(en.target);} });
    }, { threshold: .08 });
    document.querySelectorAll('.reveal').forEach(el=>io.observe(el));

    // Footer year
    document.getElementById('copy').textContent = "© " + new Date().getFullYear() + " • " + {{ AUTHOR|tojson }};
  </script>
</body>
</html>
"""


INDEX_HTML = BASE_HEAD + """
  <!-- Hero -->
  <section class="relative overflow-hidden rounded-3xl border border-slate-800 p-6 md:p-8 mb-8 gradient-border reveal">
    <div class="relative z-10">
      <h1 class="text-3xl md:text-4xl font-extrabold tracking-tight">Dashboard Project</h1>
      <p class="text-slate-400 mt-2">Kumpulan project saya. Responsif, aesthetic, tanpa login.</p>
      <div class="mt-5 flex flex-col md:flex-row gap-3 md:items-center">
        <form method="get" action="{{ url_for('home') }}" class="w-full md:w-auto flex gap-2">
          <div class="relative flex-1 md:w-96">
            <input id="searchInput" name="q" value="{{ q }}" placeholder="Cari judul, tech, atau deskripsi (tekan / untuk fokus)"
                   class="w-full pl-9 pr-3 py-2 rounded-xl bg-slate-900/70 border border-slate-700 outline-none focus:ring focus:ring-cyan-700 text-sm">
            <svg class="absolute left-3 top-2.5 h-4 w-4 text-slate-400" viewBox="0 0 24 24" fill="none"><path d="M21 21l-4.3-4.3M10.5 18a7.5 7.5 0 1 1 0-15 7.5 7.5 0 0 1 0 15Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
          </div>
          <select name="sort" class="px-3 py-2 rounded-xl bg-slate-900/70 border border-slate-700 text-sm">
            <option value="updated" {{ 'selected' if sort=='updated' else '' }}>Terbaru</option>
            <option value="title" {{ 'selected' if sort=='title' else '' }}>Judul A→Z</option>
          </select>
          <button class="px-4 py-2 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-sm shadow-glow">Cari</button>
        </form>
        <div class="text-xs text-slate-400 md:ml-3">Tekan <span class="px-1.5 py-0.5 rounded border border-slate-600">/</span> untuk fokus search</div>
      </div>
    </div>
    <div class="absolute inset-0 opacity-20 -z-0 rounded-3xl"
         style="background:linear-gradient(120deg,#22d3ee,#a855f7,#f97316);background-size:200% 200%;"></div>
  </section>

  <!-- Stats -->
  <section class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
    <div class="reveal rounded-2xl border border-slate-800 p-4 bg-slate-900/60">
      <div class="text-slate-400 text-xs">Total Project</div>
      <div class="text-2xl font-bold">{{ projects|length }}</div>
    </div>
    <div class="reveal rounded-2xl border border-slate-800 p-4 bg-slate-900/60">
      <div class="text-slate-400 text-xs">Unique Tags</div>
      <div class="text-2xl font-bold">{{ all_tags|length }}</div>
    </div>
    <div class="reveal rounded-2xl border border-slate-800 p-4 bg-slate-900/60">
      <div class="text-slate-400 text-xs">Sort</div>
      <div class="text-2xl font-bold">{{ 'Terbaru' if sort=='updated' else 'Judul' }}</div>
    </div>
  </section>

  <!-- Tag filters -->
  <section class="mb-6 reveal">
    <div class="flex items-center gap-2 overflow-x-auto pb-2">
      <a href="{{ url_for('home', q=q, sort=sort) }}" class="chip {{ 'bg-cyan-900/40 text-cyan-300 border-cyan-700' if not tag else 'bg-slate-900' }}">Semua</a>
      {% for t in all_tags %}
        <a href="#" data-tag="{{ t }}" class="chip {{ 'bg-cyan-900/40 text-cyan-300 border-cyan-700' if tag==t else 'bg-slate-900' }}">{{ t }}</a>
      {% endfor %}
    </div>
    {% if tag %}<div class="text-xs text-slate-400 mt-1">Filter tag: {{ tag }}</div>{% endif %}
  </section>

  <!-- Grid -->
  <section>
    {% if projects %}
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      {% for p in projects %}
      <article data-card data-hay="{{ (p.title ~ ' ' ~ p.subtitle ~ ' ' ~ p.description ~ ' ' ~ (p.tech|join(' ')) ~ ' ' ~ (p.tags|join(' ')))|lower }}"
               class="reveal gradient-border rounded-2xl p-[1px] hover:translate-y-[-2px] transition-transform">
        <div class="rounded-2xl bg-slate-950 p-5 border border-slate-800 group">
          <div class="flex gap-4 items-start">
            <div class="text-2xl md:text-3xl shrink-0 rounded-xl h-12 w-12 flex items-center justify-center bg-slate-800/60 border border-slate-700">{{ p.emoji or '📦' }}</div>
            <div class="min-w-0">
              <a href="{{ url_for('detail', slug=p.slug) }}" class="block font-semibold text-lg truncate group-hover:text-cyan-300">{{ p.title }}</a>
              <p class="text-slate-400 text-sm clamp-2">{{ p.subtitle }}</p>
              <div class="mt-3 flex flex-wrap gap-2">
                {% for tech in p.tech[:6] %}
                <span class="px-2.5 py-1 rounded-full bg-slate-800 border border-slate-700 text-xs">{{ tech }}</span>
                {% endfor %}
              </div>
              <div class="mt-3 flex items-center gap-2 text-xs text-slate-400">
                <span class="px-2 py-0.5 rounded bg-emerald-900/40 border border-emerald-800">{{ p.status }}</span>
                {% if p.last_updated_dt %}<span>• {{ p.last_updated_dt.strftime('%Y-%m-%d') }}</span>{% endif %}
              </div>
              <div class="mt-4 flex gap-2">
                {% if p.links.repo %}
                  <a href="{{ p.links.repo }}" target="_blank" class="px-3 py-1.5 rounded-lg bg-slate-800 border border-slate-700 text-sm hover:border-cyan-700">Repo</a>
                {% endif %}
                {% if p.links.demo %}
                  <a href="{{ p.links.demo }}" target="_blank" class="px-3 py-1.5 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-sm">Demo</a>
                {% endif %}
                <a href="{{ url_for('detail', slug=p.slug) }}" class="px-3 py-1.5 rounded-lg bg-slate-800 border border-slate-700 text-sm hover:border-cyan-700">Detail</a>
              </div>
            </div>
          </div>
        </div>
      </article>
      {% endfor %}
    </div>
    {% else %}
      <div id="emptyState" class="text-slate-400">Tidak ada project yang cocok dengan filter.</div>
    {% endif %}
  </section>
""" + BASE_FOOT

DETAIL_HTML = BASE_HEAD + """
  <nav class="mb-4 text-sm reveal">
    <a href="{{ url_for('home') }}" class="text-slate-400 hover:text-cyan-300">← Kembali</a>
  </nav>

  <header class="mb-6 reveal">
    <div class="relative overflow-hidden rounded-3xl border border-slate-800 p-6 md:p-8 gradient-border">
      <div class="flex items-start gap-4 relative z-10">
        <div class="text-4xl rounded-2xl h-16 w-16 flex items-center justify-center bg-slate-800/60 border border-slate-700">{{ p.emoji or '📦' }}</div>
        <div class="min-w-0">
          <h1 class="text-2xl md:text-3xl font-extrabold leading-tight">{{ p.title }}</h1>
          <p class="text-slate-400">{{ p.subtitle }}</p>
          <div class="mt-2 flex items-center gap-2 text-xs text-slate-400">
            <span class="px-2 py-0.5 rounded bg-emerald-900/40 border border-emerald-800">{{ p.status }}</span>
            {% if p.last_updated_dt %}<span>• Updated {{ p.last_updated_dt.strftime('%Y-%m-%d') }}</span>{% endif %}
          </div>
        </div>
        <div class="ml-auto flex gap-2">
          {% if p.links.repo %}<a class="px-3 py-1.5 rounded-lg bg-slate-800 border border-slate-700 text-sm hover:border-cyan-700" target="_blank" href="{{ p.links.repo }}">Repo</a>{% endif %}
          {% if p.links.demo %}<a class="px-3 py-1.5 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-sm" target="_blank" href="{{ p.links.demo }}">Demo</a>{% endif %}
          <button onclick="navigator.clipboard.writeText(window.location.href)" class="px-3 py-1.5 rounded-lg bg-slate-800 border border-slate-700 text-sm hover:border-cyan-700">Copy Link</button>
        </div>
      </div>
      <div class="absolute inset-0 opacity-25 -z-0" style="background:linear-gradient(120deg,#22d3ee,#a855f7,#f97316);background-size:200% 200%;animation:shine 8s linear infinite;"></div>
    </div>
  </header>

  <section class="grid md:grid-cols-3 gap-6">
    <div class="md:col-span-2 reveal">
      <div class="bg-slate-900/60 rounded-2xl border border-slate-800 p-5">
        <h2 class="font-semibold mb-2">Deskripsi</h2>
        <p class="text-slate-300 leading-relaxed whitespace-pre-line">{{ p.description }}</p>
      </div>
    </div>
    <aside class="space-y-6">
      <div class="bg-slate-900/60 rounded-2xl border border-slate-800 p-5 reveal">
        <h3 class="font-semibold mb-2">Tech Stack</h3>
        <div class="flex flex-wrap gap-2">
          {% for t in p.tech %}
          <span class="px-2.5 py-1 rounded-full bg-slate-800 border border-slate-700 text-xs">{{ t }}</span>
          {% endfor %}
        </div>
      </div>
      <div class="bg-slate-900/60 rounded-2xl border border-slate-800 p-5 reveal">
        <h3 class="font-semibold mb-2">Tags</h3>
        <div class="flex flex-wrap gap-2">
          {% for t in p.tags %}
          <a href="{{ url_for('home', tag=t) }}" class="px-2.5 py-1 rounded-full bg-slate-800 border border-slate-700 text-xs hover:border-cyan-700">{{ t }}</a>
          {% endfor %}
        </div>
      </div>
      <div class="bg-slate-900/60 rounded-2xl border border-slate-800 p-5 reveal">
        <h3 class="font-semibold mb-2">Info</h3>
        <div class="text-sm text-slate-300">Slug: <code class="text-slate-400">{{ p.slug }}</code></div>
      </div>
    </aside>
  </section>
""" + BASE_FOOT


# ---------- Routes ----------
@app.route("/")
def home():
    q = request.args.get("q", "").strip()
    tag = request.args.get("tag", "").strip()
    sort = request.args.get("sort", "updated")  # updated|title

    items = [p for p in PROJECTS if matches_query(
        p, q) and matches_tag(p, tag)]
    if sort == "title":
        items.sort(key=lambda x: x["title"].lower())
    else:
        items.sort(key=lambda x: (x.get("last_updated_dt")
                   or datetime.min), reverse=True)

    return render_template_string(
        INDEX_HTML,
        SITE_TITLE=SITE_TITLE,
        AUTHOR=AUTHOR,
        projects=items,
        q=q,
        tag=tag,
        sort=sort,
        all_tags=ALL_TAGS,
        github=GITHUB_PROFILE
    )


@app.route("/p/<slug>")
def detail(slug):
    p = next((it for it in PROJECTS if it["slug"] == slug), None)
    if not p:
        return "Not Found", 404
    return render_template_string(
        DETAIL_HTML,
        SITE_TITLE=SITE_TITLE,
        AUTHOR=AUTHOR,
        p=p,
        github=GITHUB_PROFILE
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5055, debug=True)
