import base64
import os
from datetime import date
from pathlib import Path

import requests
import streamlit as st

EVENT_DATE = date(2026, 11, 8)
MAX_FILE_MB = 15
MAX_FILE_BYTES = MAX_FILE_MB * 1024 * 1024
MAX_FILES = 5
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "heic", "png", "webp", "mp4", "mov", "m4v"}

st.set_page_config(
    page_title="Umut & Melike — Anılarımız",
    page_icon="✉️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

try:
    SCRIPT_URL = st.secrets["APPS_SCRIPT_URL"]
    UPLOAD_TOKEN = st.secrets["UPLOAD_TOKEN"]
except Exception:
    SCRIPT_URL = os.getenv("APPS_SCRIPT_URL", "")
    UPLOAD_TOKEN = os.getenv("UPLOAD_TOKEN", "")

if "invitation_open" not in st.session_state:
    st.session_state.invitation_open = False

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&family=DM+Sans:wght@400;500;600&display=swap');

    :root {
      --paper:#f4efe6; --paper-light:#fbf8f1; --ink:#39352f;
      --muted:#8d8274; --gold:#b39a72; --line:#dfd4c3;
      --wine:#754e49; --shadow:rgba(63,48,37,.13);
    }
    html, body, [class*="css"] {font-family:'DM Sans',sans-serif;}
    .stApp {
      background:
        radial-gradient(ellipse at 50% 13%, rgba(255,255,255,.82), transparent 48%),
        linear-gradient(145deg,#eee7dc 0%,#f8f4ec 48%,#eee7dc 100%);
      color:var(--ink);
    }
    [data-testid="stHeader"] {background:transparent;}
    #MainMenu,footer {visibility:hidden;}
    .block-container {width:100%;max-width:760px;margin-left:auto;margin-right:auto;padding:2.1rem 1.1rem 3.5rem;}
    .top-label {
      text-align:center;color:#978875;text-transform:uppercase;
      letter-spacing:.28em;font-size:.61rem;font-weight:600;margin:.25rem 0 1.4rem;
    }
    .stage {
      min-height:570px;display:flex;align-items:center;justify-content:center;
      position:relative;padding:2.2rem 1rem;
      background:rgba(251,248,241,.47);border:1px solid rgba(196,179,153,.35);
      box-shadow:0 24px 75px rgba(72,57,43,.045);
      overflow:hidden;
    }
    .stage:before,.stage:after {
      content:"";position:absolute;width:190px;height:190px;border:1px solid rgba(179,154,114,.18);
      border-radius:50%;pointer-events:none;
    }
    .stage:before{top:-135px;left:-105px;}
    .stage:after{bottom:-140px;right:-100px;}
    .envelope-wrap {width:min(100%,510px);text-align:center;position:relative;z-index:1;}
    .overline {font-size:.62rem;letter-spacing:.3em;text-transform:uppercase;color:#988a77;margin-bottom:1.2rem;}
    .envelope {
      position:relative;width:min(100%,440px);height:280px;margin:0 auto 1.9rem;
      filter:drop-shadow(0 24px 24px rgba(73,55,38,.15));
      perspective:1000px;
    }
    .env-back {
      position:absolute;inset:0;background:#d9c9b2;border-radius:5px;
      box-shadow:inset 0 0 0 1px rgba(120,94,64,.12);
    }
    .letter-peek {
      position:absolute;left:7%;right:7%;top:8%;height:78%;
      background:#fffdf7;border:1px solid #e7ddce;
      display:flex;flex-direction:column;align-items:center;justify-content:center;
      transition:transform 1s cubic-bezier(.2,.75,.2,1),top 1s;
    }
    .letter-peek .tiny {font-size:9px;letter-spacing:3px;color:#a38e70;text-transform:uppercase;}
    .letter-peek .couple {font:500 36px 'Cormorant Garamond',serif;color:#51463b;margin-top:8px;}
    .env-front {
      position:absolute;inset:0;
      background:linear-gradient(145deg,#e8dcc9,#d8c6ad);
      clip-path:polygon(0 0,50% 55%,100% 0,100% 100%,0 100%);
      border-radius:4px;
    }
    .env-left {
      position:absolute;inset:0;background:linear-gradient(35deg,#d1bea4,#e4d5c0);
      clip-path:polygon(0 0,50% 55%,0 100%);
    }
    .env-right {
      position:absolute;inset:0;background:linear-gradient(325deg,#cdb99f,#e2d1ba);
      clip-path:polygon(100% 0,50% 55%,100% 100%);
    }
    .env-bottom {
      position:absolute;inset:0;background:linear-gradient(180deg,#e4d5c0,#d2bea3);
      clip-path:polygon(0 100%,50% 48%,100% 100%);
    }
    .env-flap {
      position:absolute;inset:0;background:linear-gradient(180deg,#eee3d2,#d9c7ad);
      clip-path:polygon(0 0,100% 0,50% 57%);
      transform-origin:top;transition:transform .85s ease;backface-visibility:hidden;
      z-index:4;
    }
    .wax {
      position:absolute;z-index:6;left:50%;top:52%;transform:translate(-50%,-50%);
      width:58px;height:58px;border-radius:50%;
      background:radial-gradient(circle at 35% 28%,#a97870,#774b48 68%,#613d3b);
      box-shadow:0 3px 7px rgba(62,35,32,.25),inset 0 0 0 1px rgba(255,255,255,.22);
      display:flex;align-items:center;justify-content:center;
      color:#f1dfca;font:500 20px 'Cormorant Garamond',serif;
      letter-spacing:-2px;
    }
    .envelope.is-open .env-flap {transform:rotateX(180deg);z-index:0;}
    .envelope.is-open .letter-peek {transform:translateY(-105px);top:0;}
    .envelope.is-open .wax {opacity:0;transition:opacity .2s;}
    .envelope-caption {font:italic 21px 'Cormorant Garamond',serif;color:#766a5c;margin:.35rem 0;}
    .envelope-names {font:500 clamp(2.8rem,8vw,4.2rem)/1 'Cormorant Garamond',serif;color:#423b34;letter-spacing:-.025em;}
    .amp {font-style:italic;color:#b49a72;padding:0 .13em;}
    .date-line {color:#928573;font-size:.65rem;letter-spacing:.23em;text-transform:uppercase;margin-top:1.3rem;}
    .open-hint {color:#8e8172;font-size:.78rem;letter-spacing:.04em;margin-top:1.2rem;}
    .ornament {color:#b49a72;font-size:18px;letter-spacing:8px;margin:1.1rem 0;}
    .invite-card {
      background:rgba(255,253,247,.86);border:1px solid #e4dacb;
      padding:2.3rem 2rem 2rem;text-align:center;box-shadow:0 18px 50px rgba(63,48,37,.07);
      position:relative;
    }
    .invite-card:before {content:"";position:absolute;inset:9px;border:1px solid rgba(179,154,114,.32);pointer-events:none;}
    .invite-small {font-size:.62rem;letter-spacing:.28em;text-transform:uppercase;color:#a28c6e;}
    .invite-title {font:500 2.25rem 'Cormorant Garamond',serif;color:#403a33;margin:.65rem 0;}
    .invite-copy {max-width:460px;margin:0 auto;color:#81766a;font:400 1.1rem/1.7 'Cormorant Garamond',serif;}
    .invite-date {font-size:.68rem;letter-spacing:.2em;color:#8d7d69;margin-top:1.2rem;}
    .section-title {font:500 2.1rem 'Cormorant Garamond',serif;text-align:center;color:#423b34;margin:2.5rem 0 .25rem;}
    .section-copy {text-align:center;color:#8b8175;font-size:.84rem;line-height:1.75;max-width:490px;margin:0 auto 1.4rem;}
    .upload-panel {background:rgba(255,253,247,.82);border:1px solid #e4dacb;padding:1.45rem 1.35rem;}
    [data-testid="stFileUploader"] {background:#fbf8f1;border:1px dashed #cdbda7;border-radius:2px;padding:.45rem;}
    [data-testid="stFileUploaderDropzone"] {background:transparent;border:0;}
    .stTextInput label,.stFileUploader label,.stCheckbox label {color:#5c5349!important;font-size:.8rem!important;font-weight:500!important;}
    [data-testid="stTextInput"] input {border-radius:2px;border:1px solid #ded3c4;background:#fffdf8;color:#39352f!important;}     [data-testid="stTextInput"] input::placeholder {color:#8d8274!important;opacity:1;}     [data-testid="stFileUploader"] section {color:#39352f!important;}     [data-testid="stAlert"] {color:#39352f!important;}     [data-testid="stAlert"] p,[data-testid="stAlert"] [data-testid="stMarkdownContainer"] {color:#39352f!important;}     [data-testid="stAlert"] a {color:#754e49!important;}
    .stButton>button,[data-testid="stFormSubmitButton"] button {
      background:#79524d;color:#fffaf2;border:1px solid #79524d;border-radius:2px;
      min-height:3.05rem;letter-spacing:.09em;text-transform:uppercase;font-size:.7rem;font-weight:600;
    }
    .stButton>button:hover,[data-testid="stFormSubmitButton"] button:hover {background:#63413d;color:#fffaf2;border-color:#63413d;}
    .privacy {text-align:center;color:#938779;font-size:.72rem;line-height:1.7;margin:1rem auto 0;max-width:440px;}
    .thanks {background:#f3f0e8;border:1px solid #ded5c7;color:#665c50;padding:1rem;line-height:1.7;font-size:.88rem;}
    .footer {text-align:center;color:#a29686;font-size:.62rem;letter-spacing:.22em;margin-top:2.7rem;}
    @media(max-width:520px){
      .block-container{padding:1rem .75rem 2.5rem;}
      .stage{min-height:510px;padding:1.4rem .6rem;}
      .envelope{height:220px;width:96%;}
      .invite-card{padding:2rem 1.1rem;}
      .invite-title{font-size:1.9rem;}
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="top-label">A little note for you · 08 November 2026</div>', unsafe_allow_html=True)

if not st.session_state.invitation_open:
    st.markdown(
        """
        <div class="stage">
          <div class="envelope-wrap">
            <div class="overline">You are warmly invited</div>
            <div class="envelope">
              <div class="env-back"></div>
              <div class="letter-peek">
                <div class="tiny">A day to remember</div>
                <div class="couple">Umut <i style="color:#b49a72">&</i> Melike</div>
                <div class="tiny" style="margin-top:8px">08 · 11 · 2026</div>
              </div>
              <div class="env-left"></div><div class="env-right"></div>
              <div class="env-bottom"></div><div class="env-front"></div>
              <div class="env-flap"></div>
              <div class="wax">U<span style="font-size:14px">&</span>M</div>
            </div>
            <div class="envelope-caption">A special day, shared with special people.</div>
            <div class="envelope-names">Umut <span class="amp">&</span> Melike</div>
            <div class="ornament">— ✳ —</div>
            <div class="date-line">08 Kasım 2026 · Nişan Günü</div>
            <div class="open-hint">Davetiyemizi açmak için aşağıya dokunun</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("ZARFI AÇ  ✳", use_container_width=True):
        st.session_state.invitation_open = True
        st.rerun()
else:
    st.markdown(
        """
        <div class="stage" style="min-height:0;padding:2rem 1rem;">
          <div class="invite-card">
            <div class="invite-small">With love & gratitude</div>
            <div class="ornament">✳</div>
            <div class="invite-title">Bu güzel anı bizimle paylaşın</div>
            <p class="invite-copy">
              En özel günler, sevdiklerimizle paylaştığımız küçük anlarda saklı.
              O gün çektiğiniz fotoğraf ve videoları bizimle paylaşarak
              anılarımızı çoğaltmanıza çok seviniriz.
            </p>
            <div class="ornament">— ❦ —</div>
            <div class="invite-small">Umut & Melike</div>
            <div class="invite-date">8 KASIM 2026 · NİŞAN GÜNÜ</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="section-title">Anılarımızı tamamlayalım</div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="section-copy">Telefonunuzdaki fotoğraf ve videoları seçerek bize gönderebilirsiniz. '
        'Paylaşımlarınız herkese açık bir galeride yayınlanmaz; yalnızca çiftin özel arşivine kaydedilir.</p>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="upload-panel">', unsafe_allow_html=True)
    with st.form("upload_form", clear_on_submit=False):
        guest_name = st.text_input("İsminiz (isteğe bağlı)", placeholder="Adınızı yazabilirsiniz", max_chars=60)
        files = st.file_uploader(
            "Fotoğraf veya video seçin",
            type=sorted(ALLOWED_EXTENSIONS),
            accept_multiple_files=True,
            max_upload_size=MAX_FILE_MB,
            help=f"JPG, PNG, HEIC, WEBP, MP4 veya MOV · Dosya başına en fazla {MAX_FILE_MB} MB · En fazla {MAX_FILES} dosya.",
        )
        consent = st.checkbox("Seçtiğim içeriklerin Umut ve Melike'nin özel arşivine kaydedilmesini kabul ediyorum.")
        submitted = st.form_submit_button("Anılarınızı gönderin", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="privacy">✧ İçerikleriniz yalnızca Umut & Melike’nin özel Google Drive arşivine aktarılır.</div>', unsafe_allow_html=True)

    if submitted:
        if not SCRIPT_URL or not UPLOAD_TOKEN:
            st.error("Yükleme sistemi henüz yapılandırılmadı. Lütfen daha sonra tekrar deneyin.")
        elif not consent:
            st.warning("Devam etmek için paylaşım onayını işaretleyin.")
        elif not files:
            st.warning("Lütfen en az bir fotoğraf veya video seçin.")
        elif len(files) > MAX_FILES:
            st.warning(f"Bir seferde en fazla {MAX_FILES} dosya gönderebilirsiniz.")
        else:
            invalid = []
            for f in files:
                ext = Path(f.name).suffix.lower().lstrip(".")
                if ext not in ALLOWED_EXTENSIONS or f.size > MAX_FILE_BYTES:
                    invalid.append(f.name)
            if invalid:
                st.error(f"Desteklenmeyen veya {MAX_FILE_MB} MB sınırını aşan dosyalar: " + ", ".join(invalid))
            else:
                progress = st.progress(0)
                status = st.empty()
                successes, failures = 0, []
                for i, f in enumerate(files, start=1):
                    status.caption(f"{i}/{len(files)} · {f.name} yükleniyor…")
                    payload = {
                        "token": UPLOAD_TOKEN,
                        "filename": f.name,
                        "mimeType": f.type or "application/octet-stream",
                        "guestName": guest_name.strip()[:60],
                        "fileBase64": base64.b64encode(f.getvalue()).decode("ascii"),
                    }
                    try:
                        response = requests.post(SCRIPT_URL, json=payload, timeout=180)
                        response.raise_for_status()
                        result = response.json()
                        if result.get("ok") is True:
                            successes += 1
                        else:
                            failures.append(f.name)
                    except Exception:
                        failures.append(f.name)
                    progress.progress(i / len(files))
                status.empty()
                if successes:
                    st.markdown(
                        f'<div class="thanks"><strong>Çok teşekkür ederiz.</strong><br>'
                        f'{successes} dosyanız başarıyla arşivimize eklendi. Bu güzel anıları bizimle paylaştığınız için mutluyuz. 🤍</div>',
                        unsafe_allow_html=True,
                    )
                if failures:
                    st.error("Bazı dosyalar gönderilemedi: " + ", ".join(failures) + ". Daha küçük dosyalarla tekrar deneyebilirsiniz.")

    if st.button("← Davetiyeye dön", use_container_width=True):
        st.session_state.invitation_open = False
        st.rerun()

st.markdown('<div class="footer">UMUT & MELİKE &nbsp; · &nbsp; 08 — 11 — 2026</div>', unsafe_allow_html=True)
