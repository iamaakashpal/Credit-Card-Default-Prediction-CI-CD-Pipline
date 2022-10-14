from flask import Flask
from creditcarddefault.logger import logging
app = Flask(__name__)

@app.route("/",methods=['GET','POST'])
def index():
    logging.info("We are testing logged module")
    return "CI CD Pipeline"

if __name__ == '__main__':
    app.run(debug=True)