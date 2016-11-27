from flask import Flask, render_template
import client

app = Flask(__name__)
session = None


@app.route("/")
def hello():
    ram_by_user = client.ram_per_user(session)
    cpu_by_user = client.cpu_per_user(session)
    return render_template('app.html', ram_info=ram_by_user, cpu_info=cpu_by_user)


if __name__ == "__main__":
    print "loading configuration..."
    config = client.read_config('./config.yaml')
    print "initialize openstack session..."
    session = client.initialize_session(config['keystone_url'], config['user'], config['password'], config['tenant'])
    app.run()
