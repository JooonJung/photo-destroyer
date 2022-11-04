from flask import Flask
import time

app = Flask(__name__)

@app.route('/api/v1/')
def main():
    return {
        "time" : time.time(),
    }

if __name__ == "__main__":
    app.run(debug = True)
