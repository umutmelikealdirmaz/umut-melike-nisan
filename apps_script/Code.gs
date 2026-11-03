/**
 * Nişan fotoğraf/video yükleme endpoint'i.
 * Apps Script > Project Settings > Script properties:
 *   UPLOAD_TOKEN = Streamlit Secrets'taki aynı gizli anahtar
 *   ROOT_FOLDER_ID = Google Drive ana klasörünün ID'si
 */
function doPost(e) {
  try {
    if (!e || !e.postData || !e.postData.contents) {
      return json_({ ok: false, error: 'empty_request' });
    }

    var body = JSON.parse(e.postData.contents);
    var props = PropertiesService.getScriptProperties();
    var expectedToken = props.getProperty('UPLOAD_TOKEN');
    var rootId = props.getProperty('ROOT_FOLDER_ID');

    if (!expectedToken || body.token !== expectedToken) {
      return json_({ ok: false, error: 'unauthorized' });
    }
    if (!rootId || !body.fileBase64 || !body.filename) {
      return json_({ ok: false, error: 'missing_fields' });
    }

    var bytes = Utilities.base64Decode(body.fileBase64);
    // Defensive server-side cap: 15 MiB decoded.
    if (bytes.length > 15 * 1024 * 1024) {
      return json_({ ok: false, error: 'file_too_large' });
    }

    var mime = String(body.mimeType || 'application/octet-stream');
    var isVideo = mime.indexOf('video/') === 0 || /\.(mp4|mov|m4v)$/i.test(body.filename);
    var root = DriveApp.getFolderById(rootId);
    var folderName = isVideo ? 'VIDEOS' : 'PHOTOS';
    var folder = getOrCreateFolder_(root, folderName);

    var safeName = String(body.filename).replace(/[\\/:*?"<>|#%{}~&]/g, '_').slice(0, 120);
    var stamp = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'yyyyMMdd_HHmmss');
    var random = Utilities.getUuid().slice(0, 8);
    var blob = Utilities.newBlob(bytes, mime, stamp + '_' + random + '_' + safeName);
    var file = folder.createFile(blob);
    file.setDescription('Nişan Anıları | Gönderen: ' + String(body.guestName || 'Belirtilmedi').slice(0, 60));

    return json_({ ok: true, fileId: file.getId() });
  } catch (err) {
    return json_({ ok: false, error: String(err && err.message ? err.message : err) });
  }
}

function getOrCreateFolder_(parent, name) {
  var folders = parent.getFoldersByName(name);
  return folders.hasNext() ? folders.next() : parent.createFolder(name);
}

function json_(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
