from flask import Flask
import teamx_grand_daddy_metrics as metrics
 
app = Flask(__name__)
 
 
@app.route('/')
def hello_whale():
    return metrics.generate_reports()
 
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')