#!/usr/bin/env python3
# Modern HTML sayfası oluştur

html_content = '''<!DOCTYPE html>
<html lang="tr">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Basit IDS - Web Arayüzü</title>
    <style>
      :root {
        --bg: #ffffff;
        --fg: #333333;
        --border: #e0e0e0;
        --card-bg: #f9f9f9;
        --header-bg: #2c3e50;
        --header-fg: #ffffff;
        --btn-bg: #3498db;
        --btn-hover: #2980b9;
        --alert-bg: #fff3cd;
        --alert-border: #ffc107;
        --table-header: #ecf0f1;
        --table-alt: #f8f9fa;
        --danger: #e74c3c;
      }

      [data-theme="dark"] {
        --bg: #1e1e1e;
        --fg: #e0e0e0;
        --border: #404040;
        --card-bg: #2d2d2d;
        --header-bg: #1a1a1a;
        --header-fg: #e0e0e0;
        --btn-bg: #0066cc;
        --btn-hover: #0052a3;
        --alert-bg: #3d3000;
        --alert-border: #ff9800;
        --table-header: #3d3d3d;
        --table-alt: #252525;
        --danger: #ff6b6b;
      }

      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }

      html, body {
        font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
        background-color: var(--bg);
        color: var(--fg);
        transition: background-color 0.3s, color 0.3s;
      }

      .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 20px;
      }

      header {
        background-color: var(--header-bg);
        color: var(--header-fg);
        padding: 2rem 0;
        margin-bottom: 2rem;
        border-bottom: 3px solid var(--btn-bg);
      }

      header h1 {
        font-size: 28px;
        font-weight: 700;
        letter-spacing: 1px;
      }

      .header-flex {
        display: flex;
        justify-content: space-between;
        align-items: center;
      }

      .theme-toggle {
        background-color: var(--btn-bg);
        border: none;
        color: white;
        padding: 10px 15px;
        border-radius: 5px;
        cursor: pointer;
        font-size: 14px;
        transition: background-color 0.3s;
      }

      .theme-toggle:hover {
        background-color: var(--btn-hover);
      }

      h2 {
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-size: 20px;
        border-left: 4px solid var(--btn-bg);
        padding-left: 10px;
      }

      .card {
        background-color: var(--card-bg);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        transition: box-shadow 0.3s;
      }

      .card:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
      }

      .controls {
        background-color: var(--card-bg);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
      }

      .form-group {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        align-items: center;
      }

      .form-group label {
        font-weight: 600;
        margin-right: 5px;
      }

      .form-group input {
        padding: 10px;
        border: 1px solid var(--border);
        border-radius: 5px;
        background-color: var(--bg);
        color: var(--fg);
        font-size: 14px;
        transition: border-color 0.3s;
      }

      .form-group input:focus {
        outline: none;
        border-color: var(--btn-bg);
      }

      .form-group button {
        padding: 10px 20px;
        background-color: var(--btn-bg);
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 14px;
        font-weight: 600;
        transition: background-color 0.3s;
      }

      .form-group button:hover {
        background-color: var(--btn-hover);
      }

      .stats {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-bottom: 1.5rem;
      }

      .stat-item {
        background: linear-gradient(135deg, var(--btn-bg), var(--btn-hover));
        color: white;
        padding: 1.5rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
      }

      .stat-item .value {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 0.5rem;
      }

      .stat-item .label {
        font-size: 14px;
        opacity: 0.9;
      }

      .mock-warning {
        background-color: var(--alert-bg);
        border-left: 4px solid var(--alert-border);
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
        color: var(--danger);
      }

      .mock-warning::before {
        content: "⚠ ";
        font-weight: bold;
      }

      table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 1rem;
        background-color: var(--card-bg);
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
      }

      th {
        background-color: var(--table-header);
        color: var(--header-fg);
        padding: 12px;
        text-align: left;
        font-weight: 600;
        border-bottom: 2px solid var(--border);
      }

      td {
        padding: 12px;
        border-bottom: 1px solid var(--border);
      }

      tr:hover {
        background-color: var(--table-alt);
      }

      tr:last-child td {
        border-bottom: none;
      }

      .no-alerts {
        text-align: center;
        padding: 2rem;
        color: var(--fg);
        font-style: italic;
        background-color: var(--card-bg);
        border-radius: 8px;
      }

      @media (max-width: 768px) {
        .header-flex {
          flex-direction: column;
          gap: 1rem;
          text-align: center;
        }

        .form-group {
          flex-direction: column;
        }

        .form-group input,
        .form-group button {
          width: 100%;
        }

        .stats {
          grid-template-columns: 1fr;
        }

        table {
          font-size: 12px;
        }

        td, th {
          padding: 8px;
        }
      }
    </style>
  </head>
  <body>
    <header>
      <div class="container header-flex">
        <h1>🛡️ Basit IDS - Network Monitor</h1>
        <button class="theme-toggle" id="themeToggle">🌙 Dark Mode</button>
      </div>
    </header>

    <div class="container">
      <div class="controls">
        <h2>⚙️ Ayarlar</h2>
        <form method="post" action="/start">
          <div class="form-group">
            <label for="threshold">Eşik (Threshold):</label>
            <input type="number" id="threshold" name="threshold" value="5" min="1" />
            
            <label for="interface">Arayüz (Interface):</label>
            <input type="text" id="interface" name="interface" placeholder="ör. Ethernet" />
            
            <button type="submit">▶️ Sniff Başlat</button>
          </div>
        </form>
      </div>

      <div class="stats">
        <div class="stat-item">
          <div class="value">{{ stats.tracked_ips }}</div>
          <div class="label">İzlenen IP</div>
        </div>
        <div class="stat-item">
          <div class="value">{{ stats.alerts }}</div>
          <div class="label">Toplam Uyarı</div>
        </div>
        <div class="stat-item">
          <div class="value">{% if stats.scapy_available %}✓{% else %}✗{% endif %}</div>
          <div class="label">Scapy Durumu</div>
        </div>
      </div>

      {% if stats.mock_mode %}
      <div class="mock-warning">
        MOCK MOD - Sahte veriler kullanılıyor (Npcap/WinPcap yüklü değil)
      </div>
      {% endif %}

      <div class="card">
        <h2>📋 Tespit Edilen Uyarılar</h2>
        {% if alerts %}
        <table>
          <thead>
            <tr>
              <th>⏰ Zaman</th>
              <th>🔗 Kaynak IP</th>
              <th>🔌 Portlar</th>
            </tr>
          </thead>
          <tbody>
            {% for a in alerts %}
            <tr>
              <td>{{ a.time_human }}</td>
              <td><strong>{{ a.source_ip }}</strong></td>
              <td>{{ a.ports|join(", ") }} <span style="opacity: 0.7;">({{ a.count }})</span></td>
            </tr>
            {% endfor %}
          </tbody>
        </table>
        {% else %}
        <div class="no-alerts">
          📭 Henüz uyarı yok. Sniff başlat butonuna tıkla!
        </div>
        {% endif %}
      </div>
    </div>

    <script>
      const html = document.documentElement;
      const themeToggle = document.getElementById("themeToggle");
      
      const savedTheme = localStorage.getItem("theme") || "light";
      html.setAttribute("data-theme", savedTheme);
      updateThemeButton(savedTheme);

      themeToggle.addEventListener("click", () => {
        const currentTheme = html.getAttribute("data-theme");
        const newTheme = currentTheme === "light" ? "dark" : "light";
        html.setAttribute("data-theme", newTheme);
        localStorage.setItem("theme", newTheme);
        updateThemeButton(newTheme);
      });

      function updateThemeButton(theme) {
        themeToggle.textContent = theme === "light" ? "🌙 Dark Mode" : "☀️ Light Mode";
      }

      setInterval(() => {
        location.reload();
      }, 5000);
    </script>
  </body>
</html>'''

with open('c:\\Users\\ahmet\\Desktop\\Ağ İzleme ve Saldırı Tespiti Sistemi (IDS)\\templates\\index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✓ Modern web arayüzü başarıyla yazıldı!")
