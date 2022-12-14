from flask import Flask, request
import sys
import pip
from creditcarddefault.util.util import read_yaml_file, write_yaml_file
from matplotlib.style import context
from creditcarddefault.logger import logging,get_log_dataframe
from creditcarddefault.exception import CreditException
import os, sys
import json
from creditcarddefault.config.configuration import Configuartion
from creditcarddefault.constant import CONFIG_DIR, get_current_time_stamp
from creditcarddefault.pipeline.pipeline import Pipeline
from creditcarddefault.entity.creditcard_predictor import CreditCardData,CreditPredictor
from flask import send_file, abort, render_template

ROOT_DIR = os.getcwd()
LOG_FOLDER_NAME = "logs"
PIPELINE_FOLDER_NAME = "creditcarddefault"
SAVED_MODELS_DIR_NAME = "saved_models"
MODEL_CONFIG_FILE_PATH = os.path.join(ROOT_DIR, CONFIG_DIR, "model.yaml")
LOG_DIR = os.path.join(ROOT_DIR, LOG_FOLDER_NAME)
PIPELINE_DIR = os.path.join(ROOT_DIR, PIPELINE_FOLDER_NAME)
MODEL_DIR = os.path.join(ROOT_DIR, SAVED_MODELS_DIR_NAME)
CREDIT_CARD_DATA_KEY = "creditcarddata"
CREDIT_CARD_DEFAULTS_VALUE_KEY = "default"

app = Flask(__name__)


@app.route("/artifact", defaults={'req_path': 'creditcarddefault'})
@app.route('/artifact/<path:req_path>')
def render_artifact_dir(req_path):
    os.makedirs('creditcarddefault', exist_ok=True)
    # joining the base and reqested path
    print(f"req_path : {req_path}")
    abs_path = os.path.join(req_path)
    print(abs_path)
    # return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # check if path is a file and serve
    if os.path.isfile(abs_path):
        if ".html" in abs_path:
            with open(abs_path, 'r', encoding="utf-8") as file:
                context = ''
                for line in file.readlines():
                    context = f"{context}{line}"
                return context
        return send_file(abs_path)

    # Showing directory contexts
    files = {os.path.join(abs_path, file_name): file_name for file_name in os.listdir(abs_path)
             if "artifact" in os.path.join(abs_path, file_name)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template('files.html', result=result)


@app.route('/', methods=["GET", "POST"])
def index():
    try:
        return render_template("index.html")
    except Exception as e:
        return str(e)


@app.route("/view_experiment_hist", methods=['GET', 'POST'])
def view_experiment_history():
    experiment_df = Pipeline.get_experiments_status()
    context = {
        "experiment": experiment_df.to_html(classes="table table-stripod col-12")
    }
    return render_template('experiment_history.html', context=context)


@app.route('/train', methods=['GET', "POST"])
def train():
    message = ""
    pipeline = Pipeline(config=Configuartion(
        current_time_stamp=get_current_time_stamp()))
    if not Pipeline.experiment.running_status:
        message = "Training Started!"
        pipeline.start()
    else:
        message = "Training is already in progress."

    context = {
        "experiment": pipeline.get_experiments_status().to_html(classes="table table-stripod col-12"),
        "message": message
    }
    return render_template("train.html", context=context)


@app.route('/predict', methods=['GET', "POST"])
def predict():
    context = {
        CREDIT_CARD_DATA_KEY: None,
        CREDIT_CARD_DEFAULTS_VALUE_KEY: None
    }

    if request.method == 'POST':
        LIMIT_BAL = float(request.form['LIMIT_BAL'])
        GENDER = float(request.form['GENDER'])
        EDUCATION = float(request.form['EDUCATION'])
        MARRIAGE = float(request.form['MARRIAGE'])
        AGE = int(request.form['AGE'])
        PAY_1 = float(request.form['PAY_1'])
        PAY_2 = float(request.form['PAY_2'])
        PAY_3 = float(request.form['PAY_3'])
        PAY_4 = float(request.form['PAY_4'])
        PAY_5 = float(request.form['PAY_5'])
        PAY_6 = float(request.form['PAY_6'])
        BILL_AMT1 = float(request.form['BILL_AMT1'])
        BILL_AMT2 = float(request.form['BILL_AMT2'])
        BILL_AMT3 = float(request.form['BILL_AMT3'])
        BILL_AMT4 = float(request.form['BILL_AMT4'])
        BILL_AMT5 = float(request.form['BILL_AMT5'])
        BILL_AMT6 = float(request.form['BILL_AMT6'])
        PAY_AMT1 = float(request.form['PAY_AMT1'])
        PAY_AMT2 = float(request.form['PAY_AMT2'])
        PAY_AMT3 = float(request.form['PAY_AMT3'])
        PAY_AMT4 = float(request.form['PAY_AMT4'])
        PAY_AMT5 = float(request.form['PAY_AMT5'])
        PAY_AMT6 = float(request.form['PAY_AMT6'])

        creditcard_data = CreditCardData(LIMIT_BAL=LIMIT_BAL,
                                         GENDER=GENDER,
                                         EDUCATION=EDUCATION,
                                         MARRIAGE=MARRIAGE,
                                         AGE=AGE,
                                         PAY_1=PAY_1,
                                         PAY_2=PAY_2,
                                         PAY_3=PAY_3,
                                         PAY_4=PAY_4,
                                         PAY_5=PAY_5,
                                         PAY_6=PAY_6,
                                         BILL_AMT1=BILL_AMT1,
                                         BILL_AMT2=BILL_AMT2,
                                         BILL_AMT3=BILL_AMT3,
                                         BILL_AMT4=BILL_AMT4,
                                         BILL_AMT5=BILL_AMT5,
                                         BILL_AMT6=BILL_AMT6,
                                         PAY_AMT1=PAY_AMT1,
                                         PAY_AMT2=PAY_AMT2,
                                         PAY_AMT3=PAY_AMT3,
                                         PAY_AMT4=PAY_AMT4,
                                         PAY_AMT5=PAY_AMT5,
                                         PAY_AMT6=PAY_AMT6,
                                         )
        creditcard_df = creditcard_data.get_credit_card_input_data_frame()
        creditcard_predictor = CreditPredictor(model_dir=MODEL_DIR)
        creditcard_default = creditcard_predictor.predict(X=creditcard_df)
        context = {
            CREDIT_CARD_DATA_KEY: creditcard_data.get_credit_card_data_as_dict(),
            CREDIT_CARD_DEFAULTS_VALUE_KEY: creditcard_default,
        }
        return render_template('predict.html', context=context)
    return render_template("predict.html", context=context)


@app.route('/saved_models', defaults={'req_path': 'saved_models'})
@app.route('/saved_models/<path:req_path>')
def saved_models_dir(req_path):
    os.makedirs("saved_models", exist_ok=True)
    # Joining the base and the requested path
    print(f"req_path: {req_path}")
    abs_path = os.path.join(req_path)
    print(abs_path)
    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)

    # Show directory contents
    files = {os.path.join(abs_path, file): file for file in os.listdir(abs_path)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template('saved_models_files.html', result=result)


@app.route("/update_model_config", methods=['GET', 'POST'])
def update_model_config():
    try:
        if request.method == 'POST':
            model_config = request.form['new_model_config']
            model_config = model_config.replace("'", '"')
            print(model_config)
            model_config = json.loads(model_config)

            write_yaml_file(file_path=MODEL_CONFIG_FILE_PATH,
                            data=model_config)

        model_config = read_yaml_file(file_path=MODEL_CONFIG_FILE_PATH)
        return render_template('update_model.html', result={"model_config": model_config})

    except Exception as e:
        logging.exception(e)
        return str(e)


@app.route(f'/logs', defaults={'req_path': f'{LOG_FOLDER_NAME}'})
@app.route(f'/{LOG_FOLDER_NAME}/<path:req_path>')
def render_log_dir(req_path):
    os.makedirs(LOG_FOLDER_NAME, exist_ok=True)
    # Joining the base and the requested path
    logging.info(f"req_path: {req_path}")
    abs_path = os.path.join(req_path)
    print(abs_path)
    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        log_df = get_log_dataframe(abs_path)
        context = {"log": log_df.to_html(classes="table-striped", index=False)}
        return render_template('log.html', context=context)

    # Show directory contents
    files = {os.path.join(abs_path, file): file for file in os.listdir(abs_path)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template('log_files.html', result=result)


if __name__ == "__main__":
    app.run()