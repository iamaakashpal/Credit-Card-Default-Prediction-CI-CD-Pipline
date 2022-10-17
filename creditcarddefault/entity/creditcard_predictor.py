import os
import sys

from creditcarddefault.exception import CreditException
from creditcarddefault.util.util import load_object
import pandas as pd


class CreditCardData:

    def __init__(self,
                 LIMIT_BAL: float,
                 GENDER: int,
                 EDUCATION: int,
                 MARRIAGE: int,
                 AGE: int,
                 PAY_1: int,
                 PAY_2: int,
                 PAY_3: int,
                 PAY_4: int,
                 PAY_5: int,
                 PAY_6: int,
                 BILL_AMT1: float,
                 BILL_AMT2: float,
                 BILL_AMT3: float,
                 BILL_AMT4: float,
                 BILL_AMT5: float,
                 BILL_AMT6: float,
                 PAY_AMT1: float,
                 PAY_AMT2: float,
                 PAY_AMT3: float,
                 PAY_AMT4: float,
                 PAY_AMT5: float,
                 PAY_AMT6: float,
                 DEFAULTS: int = None
                 ):
        try:
            self.LIMIT_BAL = LIMIT_BAL,
            self.GENDER = GENDER,
            self.EDUCATION = EDUCATION,
            self.MARRIAGE = MARRIAGE,
            self.AGE = AGE,
            self.PAY_1 = PAY_1,
            self.PAY_2 = PAY_2,
            self.PAY_3 = PAY_3,
            self.PAY_4 = PAY_4,
            self.PAY_5 = PAY_5,
            self.PAY_6 = PAY_6,
            self.BILL_AMT1 = BILL_AMT1,
            self.BILL_AMT2 = BILL_AMT2,
            self.BILL_AMT3 = BILL_AMT3,
            self.BILL_AMT4 = BILL_AMT4,
            self.BILL_AMT5 = BILL_AMT5,
            self.BILL_AMT6 = BILL_AMT6,
            self.PAY_AMT1 = PAY_AMT1,
            self.PAY_AMT2 = PAY_AMT2,
            self.PAY_AMT3 = PAY_AMT3,
            self.PAY_AMT4 = PAY_AMT4,
            self.PAY_AMT5 = PAY_AMT5,
            self.PAY_AMT6 = PAY_AMT6,
            self.DEFAULTS = DEFAULTS
        except Exception as e:
            raise CreditException(e, sys) from e

    def get_credit_card_input_data_frame(self):

        try:
            credit_card_input_dict = self.get_credit_card_data_as_dict()
            return pd.DataFrame(credit_card_input_dict)
        except Exception as e:
            raise CreditException(e, sys) from e

    def get_credit_card_data_as_dict(self):
        try:
            input_data = {
                'LIMIT_BAL': [self.LIMIT_BAL],
                'GENDER': [self.GENDER],
                'EDUCATION': [self.EDUCATION],
                'MARRIAGE': [self.MARRIAGE],
                'AGE': [self.AGE],
                'PAY_1': [self.PAY_1],
                'PAY_2': [self.PAY_2],
                'PAY_3': [self.PAY_3],
                'PAY_4': [self.PAY_4],
                'PAY_5': [self.PAY_5],
                'PAY_6': [self.PAY_6],
                'BILL_AMT1': [self.BILL_AMT1],
                'BILL_AMT2': [self.BILL_AMT2],
                'BILL_AMT3': [self.BILL_AMT3],
                'BILL_AMT4': [self.BILL_AMT4],
                'BILL_AMT5': [self.BILL_AMT5],
                'BILL_AMT6': [self.BILL_AMT6],
                'PAY_AMT1': [self.PAY_AMT1],
                'PAY_AMT2': [self.PAY_AMT2],
                'PAY_AMT3': [self.PAY_AMT3],
                'PAY_AMT4': [self.PAY_AMT4],
                'PAY_AMT5': [self.PAY_AMT5],
                'PAY_AMT6': [self.PAY_AMT6]}
            return input_data
        except Exception as e:
            raise CreditException(e, sys)


class CreditPredictor:

    def __init__(self, model_dir: str):
        try:
            self.model_dir = model_dir
        except Exception as e:
            raise CreditException(e, sys) from e

    def get_latest_model_path(self):
        try:
            folder_name = list(map(int, os.listdir(self.model_dir)))
            latest_model_dir = os.path.join(self.model_dir, f"{max(folder_name)}")
            file_name = os.listdir(latest_model_dir)[0]
            latest_model_path = os.path.join(latest_model_dir, file_name)
            return latest_model_path
        except Exception as e:
            raise CreditException(e, sys) from e

    def predict(self, X):
        try:
            model_path = self.get_latest_model_path()
            model = load_object(file_path=model_path)
            credit_card_value = model.predict(X)
            return credit_card_value
        except Exception as e:
            raise CreditException(e, sys) from e