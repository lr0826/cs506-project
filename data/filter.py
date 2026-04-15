import pandas as pd

INFILE = "housing.csv"             
OUTFILE = "ma_boston_housing.csv"

# Boston-area keywords to match the "region" field
BOSTON_KEYWORDS = [
    "boston",
    "cambridge",
    "somerville",
    "brookline",
    "quincy",
    "newton",
    "medford",
    "malden",
    "everett",
    "revere",
    "chelsea",
    "waltham",
    "watertown",
    "arlington",
    "belmont",
]

df = pd.read_csv(INFILE)

# 1) Filter to Massachusetts
df["state"] = df["state"].astype(str).str.lower()
ma = df[df["state"] == "ma"].copy()

# 2) Filter to Boston-area regions (based on region text)
ma["region"] = ma["region"].astype(str).str.lower()
mask = False
for kw in BOSTON_KEYWORDS:
    mask = mask | ma["region"].str.contains(kw, na=False)

bos = ma[mask].copy()

# 3) Basic cleaning for rent prediction
bos["price"] = pd.to_numeric(bos["price"], errors="coerce")
bos["beds"] = pd.to_numeric(bos["beds"], errors="coerce")
bos["baths"] = pd.to_numeric(bos["baths"], errors="coerce")
bos["sqfeet"] = pd.to_numeric(bos["sqfeet"], errors="coerce")

# Keep valid prices and remove extreme outliers
bos = bos[bos["price"].notna()]
bos = bos[(bos["price"] >= 500) & (bos["price"] <= 15000)]

# Drop duplicates by listing id
bos = bos.drop_duplicates(subset=["id"])

bos.to_csv(OUTFILE, index=False)
