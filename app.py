from flask import Flask, render_template, jsonify
import client
import operator

app = Flask(__name__)
session = None


@app.route("/")
def hello():
    return render_template('piechart.html')


@app.route("/plot/ram")
def plot_ram():
    data = sorted(client.ram_per_user(session), key=operator.itemgetter(1))
    return render_template('piechart.html', entries=data, title="RAM usage by userId")


@app.route("/plot/cpu")
def plot_cpu():
    data = sorted(client.cpu_per_user(session), key=operator.itemgetter(1))
    return render_template('piechart.html', entries=data, title="VCPUs usage by userId")


@app.route("/api/ram")
def api_ram():
    ram_by_user = sorted(client.ram_per_user(session), key=operator.itemgetter(1))
    return jsonify([{"label":u, "value":v} for u,v in ram_by_user])


@app.route("/api/cpu")
def api_cpu():
    cpu_by_user = sorted(client.cpu_per_user(session), key=operator.itemgetter(1))
    return jsonify([{"label":u, "value":v} for u,v in cpu_by_user])


if __name__ == "__main__":
    print "loading configuration..."
    config = client.read_config('./config.yaml')
    print "initialize openstack session..."
    session = client.initialize_session(config['keystone_url'], config['user'], config['password'], config['tenant'])
    app.run()
