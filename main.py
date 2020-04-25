from flask import Flask, render_template, request
import backend

app = Flask(__name__, static_url_path="/static")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        ip_address = request.remote_addr
        future, location, long_date, current_weathericon, current_temp, current_conditions = backend.run(ip_address)
        return render_template('data.html', future=future, 
                                            location=location, 
                                            date=long_date, 
                                            current_weathericon=current_weathericon, 
                                            current_temp=current_temp, 
                                            current_conditions=current_conditions)
    
if __name__ == '__main__':
    app.debug = True    # Change to False when deploying app
    app.run()