# Umut & Melike — Nişan Anıları

Minimal krem/bej tasarımlı, yalnızca yükleme amaçlı fotoğraf ve video paylaşım sitesi. Etkinlik tarihi: **8 Kasım 2026**.

## Akış
Streamlit misafir arayüzü → Apps Script Web App → Google Drive (PHOTOS / VIDEOS).
Fotoğraflar sitede listelenmez; yükleme-only akışıdır.

## 1) Google Drive klasörü
1. Google Drive'da `NISAN_ANILARI` adlı ana klasör oluşturun.
2. Klasör URL'sindeki `/folders/` sonrasındaki kimliği (ID) kopyalayın.
3. Klasör paylaşımını herkese açık yapmayın.

## 2) Apps Script
1. https://script.google.com adresinde yeni proje açın.
2. `apps_script/Code.gs` içeriğini `Code.gs` dosyasına yapıştırın.
3. Project Settings → Script properties bölümüne iki özellik ekleyin:
   - `ROOT_FOLDER_ID` = Drive ana klasör ID'si
   - `UPLOAD_TOKEN` = uzun, rastgele bir gizli anahtar (en az 32 karakter)
4. Deploy → New deployment → Web app.
5. Execute as: **Me**. Who has access: **Anyone**.
6. Deploy edip `/exec` ile biten Web App URL'sini kopyalayın.

> Web App'i "Anyone" yapmak, Google hesabı olmayan misafirlerin dosya gönderebilmesi içindir. Gizli token sunucu tarafındaki Streamlit Secrets'ta tutulur; Drive klasörü herkese açılmaz. Endpoint URL'si ve token internette paylaşılmamalıdır.

## 3) Streamlit Secrets
Yerelde `.streamlit/secrets.toml` oluşturun (Git'e eklemeyin):

```toml
APPS_SCRIPT_URL = "https://script.google.com/macros/s/DEPLOYMENT_ID/exec"
UPLOAD_TOKEN = "AYNI_UZUN_GIZLI_ANAHTAR"
```

## 4) Yerelde çalıştırma

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 5) Streamlit Community Cloud
1. Bu klasörü GitHub reposuna yükleyin.
2. Streamlit Community Cloud'da repo ve `app.py` seçerek deploy edin.
3. App → Settings → Secrets içine `secrets.toml` içeriğini yapıştırın.

## MVP limitleri
- Dosya başına en fazla 15 MiB; aynı gönderimde en fazla 5 dosya.
- Fotoğraf: JPG/JPEG, PNG, HEIC, WEBP.
- Video: MP4, MOV, M4V.
- İlk sürümde galeri yoktur; yüklenen dosyalar sadece Drive'da tutulur.
- Google hesabının ücretsiz 15 GB kotası Gmail/Drive/Photos arasında ortaktır.

## Yayına almadan önce
- Test için önce 1 küçük JPG, sonra 1 küçük MP4 gönderin.
- Apps Script → Executions ekranından hata kontrolü yapın.
- Gerçek etkinlikte misafirlerin yüklediği dosyaları yedekleyin.
- 15 MiB sınırı, Apps Script'in gelen istek gövdesi için garanti edilmiş bir platform kotası değildir; etkinlikten önce gerçek telefonlardan test edin. Hata alınırsa dosya sınırını düşürün veya doğrudan istemciden Google Drive'a resumable upload gibi farklı bir mimariye geçin.
