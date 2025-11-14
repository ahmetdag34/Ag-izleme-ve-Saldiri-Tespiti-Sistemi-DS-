from flask import Flask, render_template, jsonify, request, redirect, url_for
import logging
import ids_core

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')


@app.route('/')
def index():
    stats = ids_core.get_stats()
    alerts = ids_core.get_alerts()
    return render_template('index.html', alerts=alerts, stats=stats)


@app.route('/start', methods=['POST'])
def start():
    threshold = int(request.form.get('threshold', 5))
    iface = request.form.get('interface') or None
    ids_core.start_sniffing(scan_threshold=threshold, iface=iface)
    return redirect(url_for('index'))


@app.route('/api/alerts')
def api_alerts():
    return jsonify(ids_core.get_alerts())


if __name__ == '__main__':
    # Varsayılan: sniffing otomatik başlamasın; kullanıcı arayüzünden başlatılsın
    app.run(host='0.0.0.0', port=5000, debug=False)
