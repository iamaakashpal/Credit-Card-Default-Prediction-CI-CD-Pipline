from flask import Flask
import sys
from creditcarddefault.logger import logging
from creditcarddefault.exception import CreditException
app = Flask(__name__)


@app.route("/",methods=['GET','POST'])
def index():
    try:
        raise Exception(" !!! We are testing custom Exception !!! ")
    except Exception as e:
        creditcard = CreditException(e,sys)
        logging.info(creditcard.error_message)
        logging.info("We are testing logging module")
    return "CI CD Pipeline"


if __name__ == '__main__':
    app.run(debug=True)