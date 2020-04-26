from flask import Flask, render_template, request
from werkzeug.middleware.proxy_fix import ProxyFix
import backend

app = Flask(__name__, static_url_path="/static")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data/', methods=['GET'])
def data():
    if request.method == 'GET':
        ip_address = request.remote_addr
        future, location, long_date, current_weathericon, current_temp, current_conditions = backend.run(ip_address)
        return render_template('data.html', future=future, 
                                            location=location, 
                                            date=long_date, 
                                            current_weathericon=current_weathericon, 
                                            current_temp=current_temp, 
                                            current_conditions=current_conditions)
app.wsgi_app = ProxyFix(app.wsgi_app)   

    
if __name__ == '__main__':
    app.debug = True    # Change to False when deploying app
    app.run()