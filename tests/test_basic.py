import pandas as pd
import numpy as np

def test_data_loads():
    df = pd.read_csv("data/ma_boston_housing.csv")
    assert len(df) > 0
    assert "price" in df.columns

def test_price_reasonable_range():
    df = pd.read_csv("data/ma_boston_housing.csv")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df = df.dropna(subset=["price"])
    assert (df["price"] > 0).all()

def test_keyword_score_logic():
    def keyword_score(text, keywords):
        t = str(text).lower()
        return sum(1 for kw in keywords if kw in t)

    kws = ["roof deck", "luxury", "gym"]
    assert keyword_score("Luxury building with ROOF DECK", kws) == 2
    assert keyword_score("no amenities here", kws) == 0