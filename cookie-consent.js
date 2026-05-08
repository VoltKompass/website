(function () {
  const STORAGE_KEY = 'vk-cookie-consent';
  const VERSION = 1;
  const listeners = new Set();

  const defaultPrefs = {
    necessary: true,
    media: false,
    version: VERSION,
    savedAt: null
  };

  function readPrefs() {
    try {
      const saved = JSON.parse(localStorage.getItem(STORAGE_KEY));
      if (!saved || saved.version !== VERSION) return null;
      return { ...defaultPrefs, ...saved, necessary: true };
    } catch {
      return null;
    }
  }

  function currentPrefs() {
    return readPrefs() || { ...defaultPrefs };
  }

  function savePrefs(nextPrefs) {
    const prefs = {
      ...defaultPrefs,
      ...nextPrefs,
      necessary: true,
      version: VERSION,
      savedAt: new Date().toISOString()
    };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(prefs));
    closePanel();
    listeners.forEach((listener) => listener(prefs));
  }

  function hasConsent(category) {
    const prefs = readPrefs();
    return Boolean(prefs && prefs[category]);
  }

  function closePanel() {
    document.querySelectorAll('[data-cookie-root]').forEach((el) => el.remove());
  }

  function renderPanel(options = {}) {
    closePanel();

    const prefs = currentPrefs();
    const showDetails = Boolean(options.showDetails);
    const root = document.createElement('div');
    root.className = 'cookie-consent';
    root.setAttribute('data-cookie-root', '');
    root.setAttribute('role', 'dialog');
    root.setAttribute('aria-modal', 'true');
    root.setAttribute('aria-labelledby', 'cookieTitle');

    root.innerHTML = `
      <div class="cookie-panel">
        <div class="cookie-copy">
          <span class="eyebrow">Datenschutz</span>
          <h2 id="cookieTitle">Cookie-Einstellungen</h2>
          <p>Wir nutzen notwendige Speicherungen f&uuml;r den Betrieb der Website. Externe Medien wie YouTube laden wir erst, wenn du zustimmst.</p>
        </div>

        <div class="cookie-options"${showDetails ? '' : ' hidden'}>
          <label class="cookie-option cookie-option-disabled">
            <input type="checkbox" checked disabled />
            <span>
              <strong>Notwendig</strong>
              <small>Speichert deine Auswahl und sorgt daf&uuml;r, dass die Website technisch funktioniert.</small>
            </span>
          </label>
          <label class="cookie-option">
            <input type="checkbox" data-cookie-media ${prefs.media ? 'checked' : ''} />
            <span>
              <strong>Externe Medien</strong>
              <small>Erlaubt das Laden eingebetteter YouTube-Inhalte und externer Video-Vorschauen.</small>
            </span>
          </label>
        </div>

        <div class="cookie-actions">
          <button type="button" class="btn btn-ghost" data-cookie-necessary>Nur notwendige</button>
          <button type="button" class="btn btn-ghost" data-cookie-custom>${showDetails ? 'Auswahl speichern' : 'Auswahl anpassen'}</button>
          <button type="button" class="btn btn-primary" data-cookie-all>Alle akzeptieren</button>
        </div>
      </div>
    `;

    document.body.append(root);
    root.querySelector('[data-cookie-all]').addEventListener('click', () => savePrefs({ media: true }));
    root.querySelector('[data-cookie-necessary]').addEventListener('click', () => savePrefs({ media: false }));
    root.querySelector('[data-cookie-custom]').addEventListener('click', () => {
      if (!root.querySelector('.cookie-options').hidden) {
        savePrefs({ media: root.querySelector('[data-cookie-media]').checked });
        return;
      }
      renderPanel({ showDetails: true });
    });
  }

  function openSettings() {
    renderPanel({ showDetails: true });
  }

  function onChange(listener) {
    listeners.add(listener);
    return () => listeners.delete(listener);
  }

  window.VKCookieConsent = {
    getPreferences: currentPrefs,
    hasConsent,
    onChange,
    openSettings
  };

  document.addEventListener('click', (event) => {
    const trigger = event.target.closest('[data-cookie-settings]');
    if (!trigger) return;
    event.preventDefault();
    openSettings();
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      if (!readPrefs()) renderPanel();
    });
  } else if (!readPrefs()) {
    renderPanel();
  }
})();
