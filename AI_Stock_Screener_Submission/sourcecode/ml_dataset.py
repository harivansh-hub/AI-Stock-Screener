import pandas as pd


def create_labels(trades):

    trades["target"] = trades["profitable"]

    return trades