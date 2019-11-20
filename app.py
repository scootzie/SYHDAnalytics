from flask import Flask
import teamx_grand_daddy_metrics as metrics

app = Flask(__name__)

generating_reports = False


@app.route('/')
def analytics_reports():
    global generating_reports
    if generating_reports:
        return
    else:
        generating_reports = True
        result = metrics.generate_reports()
        generating_reports = False
        return result


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
