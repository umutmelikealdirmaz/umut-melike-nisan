import base64
import os
from pathlib import Path

import requests
import streamlit as st


EVENT_DATE = "08 KASIM 2026"
MAX_FILE_MB = 15
MAX_FILE_BYTES = MAX_FILE_MB * 1024 * 1024
MAX_FILES = 5
ALLOWED_EXTENSIONS = ("jpg", "jpeg", "png", "webp", "heic", "mp4", "mov", "m4v")

st.set_page_config(
    page_title="Umut & Melike | Anılarımız",
    page_icon="🤍",
    layout="centered",
    initial_sidebar_state="collapsed",
)


def load_upload_settings():
    """Read Streamlit secrets, with environment variables as a local fallback."""
    try:
        script_url = st.secrets.get("APPS_SCRIPT_URL", "")
        upload_token = st.secrets.get("UPLOAD_TOKEN", "")
    except Exception:
        script_url = os.getenv("APPS_SCRIPT_URL", "")
        upload_token = os.getenv("UPLOAD_TOKEN", "")
    return str(script_url).strip(), str(upload_token).strip()


SCRIPT_URL, UPLOAD_TOKEN = load_upload_settings()

if "invitation_open" not in st.session_state:
    st.session_state.invitation_open = False


st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@400;500;600&display=swap');

    :root {
      --ink: #302a27;
      --muted: #756b65;
      --soft: #f7f3ee;
      --paper: #fffdfa;
      --line: #e9dfd4;
      --rose: #9a625d;
      --rose-dark: #784743;
      --gold: #b69466;
    }
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    .stApp {
      background:
        radial-gradient(ellipse at 50% 0%, rgba(255,255,255,.97) 0%, rgba(255,255,255,0) 48%),
        linear-gradient(160deg, #f5eee6 0%, #fcfaf7 48%, #f3ece5 100%);
      color: var(--ink);
    }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stToolbar"] { right: 1rem; }
    #MainMenu, footer { visibility: hidden; }
    .block-container {
      width: 100%; max-width: 820px; margin: 0 auto;
      padding: 2rem 1.25rem 3.25rem;
    }
    .brand {
      display:flex; align-items:center; justify-content:center; gap:.65rem;
      color:#6e5b50; font-size:.72rem; font-weight:700; letter-spacing:.22em;
      text-transform:uppercase; margin:.2rem auto 1.8rem;
    }
    .brand-mark {
      display:inline-flex; align-items:center; justify-content:center;
      width:2rem; height:2rem; border:1px solid #d7c5ad; border-radius:50%;
      color:var(--rose); font-family:'Playfair Display',serif; font-size:1rem;
    }
    .hero {
      position:relative; overflow:hidden; text-align:center;
      background:rgba(255,253,250,.86); border:1px solid var(--line);
      border-radius:22px; padding:clamp(2rem,6vw,4.2rem) clamp(1.2rem,6vw,4.4rem);
      box-shadow:0 22px 70px rgba(69,49,37,.07);
    }
    .hero:before,.hero:after {
      content:""; position:absolute; width:190px; height:190px; border:1px solid rgba(182,148,102,.20);
      border-radius:50%; pointer-events:none;
    }
    .hero:before { top:-142px; left:-112px; }
    .hero:after { right:-125px; bottom:-148px; }
    .eyebrow {
      color:var(--rose); font-size:.68rem; font-weight:700; letter-spacing:.2em;
      text-transform:uppercase; margin:0 0 1rem;
    }
    .hero h1 {
      color:var(--ink); font:500 clamp(2.3rem,7vw,4.15rem)/1.08 'Playfair Display',serif;
      letter-spacing:-.035em; margin:0 auto .9rem; max-width:650px;
    }
    .hero p {
      color:var(--muted); font-size:clamp(.98rem,2.4vw,1.12rem); line-height:1.8;
      margin:.5rem auto 0; max-width:570px;
    }
    .date-pill {
      display:inline-flex; margin:1.4rem auto 0; padding:.62rem 1rem;
      border:1px solid #eadbc7; border-radius:999px; color:#715c45;
      background:#fbf6ef; font-size:.72rem; font-weight:700; letter-spacing:.12em;
    }
    .section-heading {
      color:var(--ink); text-align:center; font:500 clamp(1.8rem,5vw,2.55rem)/1.2 'Playfair Display',serif;
      margin:2.45rem 0 .45rem;
    }
    .section-copy {
      color:var(--muted); text-align:center; font-size:.96rem; line-height:1.75;
      max-width:620px; margin:0 auto 1.35rem;
    }
    .form-card {
      padding:clamp(1.1rem,4vw,2rem); border:1px solid var(--line); border-radius:18px;
      background:rgba(255,253,250,.92); box-shadow:0 14px 42px rgba(69,49,37,.045);
    }
    .helper {
      color:#786e66; font-size:.83rem; line-height:1.65;
      background:#f8f3ed; border-left:3px solid #c9a97f;
      padding:.75rem .9rem; border-radius:0 8px 8px 0; margin:.3rem 0 1rem;
    }
    .stTextInput label,.stFileUploader label,.stCheckbox label {
      color:#4b413b!important; font-size:.9rem!important; font-weight:600!important;
    }
    [data-testid="stTextInput"] input {
      color:#302a27!important; background:#fff!important; border:1px solid #d9cec4!important;
      border-radius:10px!important; min-height:3rem;
    }
    [data-testid="stTextInput"] input::placeholder { color:#8b8178!important; opacity:1; }
    [data-testid="stFileUploader"] {
      background:#fbf8f4!important; border:1px dashed #c9b8a5!important; border-radius:12px!important;
      padding:.65rem!important;
    }
    [data-testid="stFileUploaderDropzone"] { background:transparent!important; border:0!important; }
    [data-testid="stFileUploader"] section,[data-testid="stFileUploader"] small { color:#4b413b!important; }
    [data-testid="stAlert"] { border-radius:10px!important; }
    [data-testid="stAlert"] p,[data-testid="stAlert"] [data-testid="stMarkdownContainer"] { color:#302a27!important; }
    .stButton>button,[data-testid="stFormSubmitButton"] button {
      width:100%; min-height:3.2rem; border:1px solid var(--rose-dark)!important;
      border-radius:10px!important; background:var(--rose-dark)!important; color:#fff!important;
      font-size:.82rem!important; font-weight:700!important; letter-spacing:.08em;
      box-shadow:0 8px 18px rgba(120,71,67,.14); transition:all .18s ease;
    }
    .stButton>button:hover,[data-testid="stFormSubmitButton"] button:hover {
      background:#633936!important; border-color:#633936!important; transform:translateY(-1px);
    }
    .stButton>button:focus,[data-testid="stFormSubmitButton"] button:focus { box-shadow:0 0 0 .2rem rgba(154,98,93,.22)!important; }
    .privacy-note {
      color:#746a62; text-align:center; font-size:.78rem; line-height:1.7;
      margin:1rem auto 0; max-width:600px;
    }
    .footer-note {
      color:#92867b; text-align:center; font-size:.68rem; letter-spacing:.16em;
      margin:2.5rem auto 0; text-transform:uppercase;
    }
    @media(max-width:600px) {
      .block-container { padding:1rem .75rem 2rem; }
      .brand { margin-bottom:1.15rem; }
      .hero { border-radius:16px; padding:2.1rem 1.15rem; }
      .section-heading { margin-top:2rem; }
      .form-card { border-radius:14px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    '<div class="brand"><span class="brand-mark">U&amp;M</span><span>Umut &amp; Melike</span></div>',
    unsafe_allow_html=True,
)

if not st.session_state.invitation_open:
    st.markdown(
        f"""
        <section class="hero">
          <div class="eyebrow">Sevgiyle davetlisiniz</div>
          <h1>Bu güzel günü bizimle paylaşın</h1>
          <p>Nişan günümüzde çektiğiniz fotoğraf ve videoları bizimle paylaşın.
             Her kare, birlikte biriktirdiğimiz anılara eklenecek.</p>
          <div class="date-pill">{EVENT_DATE} &nbsp;·&nbsp; NİŞAN GÜNÜ</div>
        </section>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div class='section-heading'>Anılarımızı birlikte tamamlayalım</div>", unsafe_allow_html=True)
    st.markdown(
        "<p class='section-copy'>Telefonunuzdan en sevdiğiniz fotoğraf ve videoları seçin. "
        "Paylaştıklarınız herkese açık bir galeride yayınlanmaz; çiftin özel arşivine kaydedilir.</p>",
        unsafe_allow_html=True,
    )
    if st.button("FOTOĞRAF VE VİDEO PAYLAŞ  →", use_container_width=True):
        st.session_state.invitation_open = True
        st.rerun()
else:
    st.markdown(
        f"""
        <section class="hero">
          <div class="eyebrow">Umut &amp; Melike · {EVENT_DATE}</div>
          <h1>Bu anıları bizimle paylaşın</h1>
          <p>Seçtiğiniz fotoğraf ve videolar yalnızca özel Google Drive arşivimize aktarılır.</p>
        </section>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div class='section-heading'>Fotoğraf veya video ekle</div>", unsafe_allow_html=True)
    st.markdown(
        f"<p class='section-copy'>En fazla {MAX_FILES} dosya seçebilirsiniz. "
        f"Her dosya en çok {MAX_FILE_MB} MB olabilir.</p>",
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        st.markdown('<div class="helper">Dosyalarınız özel arşivimize gönderilir. Lütfen paylaşma izniniz olan içerikleri seçin.</div>', unsafe_allow_html=True)
        with st.form("memory_upload", clear_on_submit=False):
            guest_name = st.text_input(
                "Adınız (isteğe bağlı)",
                placeholder="Örn. Ayşe Yılmaz",
                max_chars=60,
                key="guest_name",
            )
            files = st.file_uploader(
                "Fotoğraf veya video seçin",
                type=list(ALLOWED_EXTENSIONS),
                accept_multiple_files=True,
                max_upload_size=MAX_FILE_MB,
                key="guest_media_upload",
                help="JPG, PNG, WEBP, HEIC, MP4, MOV veya M4V",
            )
            consent = st.checkbox(
                "Seçtiğim içeriklerin özel arşive kaydedilmesini kabul ediyorum.",
                key="upload_consent",
            )
            submitted = st.form_submit_button("ANILARI GÖNDER", use_container_width=True)

    st.markdown(
        '<div class="privacy-note">🔒 İçerikler yalnızca Umut &amp; Melike’nin özel arşivine kaydedilir.</div>',
        unsafe_allow_html=True,
    )

    if submitted:
        if not SCRIPT_URL or not UPLOAD_TOKEN:
            st.error("Yükleme servisi henüz yapılandırılmamış. Lütfen daha sonra tekrar deneyin.")
        elif not consent:
            st.warning("Göndermeden önce paylaşım onayını işaretleyin.")
        elif not files:
            st.warning("Lütfen en az bir fotoğraf veya video seçin.")
        elif len(files) > MAX_FILES:
            st.warning(f"Bir seferde en fazla {MAX_FILES} dosya gönderebilirsiniz.")
        else:
            invalid_files = []
            for uploaded in files:
                extension = Path(uploaded.name).suffix.lower().lstrip(".")
                if extension not in ALLOWED_EXTENSIONS or uploaded.size > MAX_FILE_BYTES:
                    invalid_files.append(uploaded.name)

            if invalid_files:
                st.error("Desteklenmeyen veya boyut sınırını aşan dosyalar: " + ", ".join(invalid_files))
            else:
                progress = st.progress(0, text="Gönderim hazırlanıyor…")
                status = st.empty()
                successes = 0
                failures = []

                for index, uploaded in enumerate(files, start=1):
                    status.info(f"{index}/{len(files)} · {uploaded.name} Drive arşivine gönderiliyor…")
                    payload = {
                        "token": UPLOAD_TOKEN,
                        "filename": uploaded.name,
                        "mimeType": uploaded.type or "application/octet-stream",
                        "guestName": guest_name.strip()[:60],
                        "fileBase64": base64.b64encode(uploaded.getvalue()).decode("ascii"),
                    }
                    try:
                        response = requests.post(SCRIPT_URL, json=payload, timeout=(20, 180))
                        response.raise_for_status()
                        result = response.json()
                        if result.get("ok") is True:
                            successes += 1
                        else:
                            reason = str(result.get("error") or "Apps Script yüklemeyi kabul etmedi.")
                            failures.append(f"{uploaded.name}: {reason[:220]}")
                    except requests.exceptions.Timeout:
                        failures.append(f"{uploaded.name}: 180 saniyede yanıt alınamadı.")
                    except requests.exceptions.HTTPError as exc:
                        code = exc.response.status_code if exc.response is not None else "bilinmiyor"
                        failures.append(f"{uploaded.name}: sunucu HTTP {code} hatası döndürdü.")
                    except requests.exceptions.RequestException as exc:
                        failures.append(f"{uploaded.name}: bağlantı kurulamadı ({type(exc).__name__}).")
                    except (ValueError, TypeError) as exc:
                        failures.append(f"{uploaded.name}: sunucu yanıtı okunamadı ({type(exc).__name__}).")
                    progress.progress(index / len(files), text=f"{index}/{len(files)} dosya işlendi")

                status.empty()
                progress.empty()
                if successes:
                    st.success(f"{successes} dosya arşive eklendi. Bizimle paylaştığınız için çok teşekkür ederiz 🤍")
                if failures:
                    st.error("Bazı dosyalar gönderilemedi: " + " · ".join(failures))

    if st.button("← DAVETİYEYE DÖN", use_container_width=True):
        st.session_state.invitation_open = False
        st.rerun()

st.markdown(
    f'<div class="footer-note">Umut &amp; Melike · {EVENT_DATE}</div>',
    unsafe_allow_html=True,
)
