# Boston Rent Prediction from Listings (CS506 Final Project)

**Video (10-min presentation):** *https://youtu.be/xtHtk_HQah4?si=AKNFNNAYu08PARAb*

---

## How to run (reproduce results)
**Requirements:** `make` + Python **3.11+** (CI uses Python 3.11).
From the repo root:

```bash
make setup
make test
make run_notebook
```

- `make setup` creates a fresh virtual environment and installs dependencies.
- `make test` runs lightweight sanity tests (data load + feature logic).
- `make run_notebook` executes `notebooks/Final_Analysis.ipynb` end-to-end and writes:
  - `notebooks/executed_Final_Analysis.ipynb` (generated artifact; not committed)

> The full analysis (code + plots + results) lives in `notebooks/Final_Analysis.ipynb`.

---

## Project Goal

**Primary goal:** Predict the monthly rent (`price`) of a Boston-area rental listing using listing features, and **outperform a baseline** that always predicts the **median rent**.

**Metric:** Mean Absolute Error (MAE) in USD (lower is better).

**Why MAE:** MAE is a good choice here because it measures the average rent error in dollars, is easy to interpret (e.g., “off by $260 on average”), and is less sensitive to extreme outliers than squared-error metrics like MSE/RMSE.

---

## Repository Organization

- `data/`
  - `ma_boston_housing.csv` — Boston-area filtered dataset used for modeling
  - `filter.py` — script that filters the original USA housing dataset to MA + Boston region
- `notebooks/`
  - `Final_Analysis.ipynb` — main analysis notebook (data cleaning, features, plots, models, tuning)
- `tests/`
  - `test_basic.py` — minimal unit tests for CI + reproducibility
- `.github/workflows/`
  - `test.yml` — GitHub Actions workflow to run tests
- `Makefile`, `requirements.txt`, `.gitignore`

---

## Data Collection

**Data source:** Kaggle “USA Housing Listings” dataset (Craigslist-based listings). link: https://www.kaggle.com/datasets/austinreese/usa-housing-listings

**Method:** I used the public Kaggle dataset and implemented filtering in code to isolate Massachusetts and the Boston region.

**What’s included in this repo:**
- data/ma_boston_housing.csv is included so results reproduce without downloading the full dataset

**How to regenerate ma_boston_housing.csv (optional):**
The full Kaggle dataset file is large (hundreds of MB), so it is not committed.
- Download the Kaggle dataset CSV and rename it to housing.csv
- Place it in data/
- Run:
- cd data
- python filter.py

**Filtering approach (implemented in `data/filter.py`):**
- Keep only `state == "ma"`
- Further filter to `region == "boston"`

This produces `data/ma_boston_housing.csv`, which is the dataset used in the notebook.


---

## Data Cleaning

To reduce noise and keep the dataset consistent for modeling:

- **Type conversion (make columns usable):**
  - Converted `price`, `beds`, `baths`, `sqfeet`, `lat`, and `long` to numeric (invalid entries → `NaN`)
  - Filled missing `description` with `""` so text processing works consistently
- **Price cleaning:**
  - Removed missing/invalid prices
  - Removed extreme outliers by keeping `500 <= price <= 15000`
- **Deduplication:**
  - Deduplicated listings using listing `id`

**Location data quality (important update):**
- A small number of rows had clearly incorrect coordinates (lat/long far outside Boston).
- Instead of dropping those listings entirely, I **masked invalid coordinates to `NaN`** so they do not corrupt:
  - distance-based features (e.g., `dist_downtown`)
  - geo clustering (`geo_cluster`)
  - distance-based models (KNN)
- Listings without valid coordinates are handled safely by assigning `geo_cluster = -1`.

---

## Feature Extraction

### 1) Structured listing attributes
- Numeric: `beds`, `baths`, `sqfeet`
- Categorical (one-hot encoded): `type`, `laundry_options`, `parking_options`

### 2) Location & neighborhood signals
Because official neighborhood labels are not provided, I use location proxies:
- `lat`, `long` (masked to `NaN` if outside the Boston bounding box)
- `dist_downtown`: Euclidean distance to downtown Boston (simple location premium proxy)
- `geo_cluster`: KMeans clustering on valid lat/long (neighborhood-like groups)
  - Missing/invalid coordinates use `geo_cluster = -1`

### 3) Text description signals
Important rent signals are often only present in the listing text.

**A) Engineered keyword features (interpretable)**
- `luxury_score`: counts luxury/amenity keywords (e.g., “luxury”, “renovated”, “doorman”, “roof deck”)
- `transit_score`: counts transit keywords (e.g., “near T”, “MBTA”, line names, “station”)
- `no_fee`: binary indicator for “no fee”

**B) LSA text representation (TF-IDF → SVD)**
- TF-IDF with unigrams + bigrams (`ngram_range=(1,2)`) to capture phrases like “roof deck”, “no fee”
- TruncatedSVD (LSA) to compress sparse text vectors into a dense space where similarity is meaningful

---

## Model Training & Evaluation

### Train/test split
- 80/20 split using `train_test_split(test_size=0.2, random_state=42)`

### Baseline
- Predict the **median rent** from the training set for every test listing

### Model 1 (main): LSA + KNN regression
- Preprocessing: text TF-IDF → SVD (LSA), plus numeric/categorical/engineered features
- Regressor: `KNeighborsRegressor(weights="distance")`
- Best tuned settings (from the notebook):
  - `n_components = 25`
  - `KNN k = 7`
  - `k_geo = 12` and **include both** `lat/long` + `geo_cluster`

**Why KNN:** Rent behaves like “comparable listings” (comps). KNN naturally models this by predicting from the most similar listings in feature space.

### Model 2 (comparison): LinearSVR
- Same feature set and preprocessing pipeline
- Tuned hyperparameters `(C, epsilon)` to improve performance
- Used as a global baseline model for comparison against KNN

---

## Results (MAE on held-out test set)

| Model | MAE (USD) |
|---|---:|
| Median baseline | **602.59** |
| LinearSVR (best tuned) | **324.80** |
| KNN + LSA (best tuned) | **263.67** |

**Takeaway:** KNN + LSA performs best because rent has strong local structure (neighborhood + quality segments). A global linear model (LinearSVR) cannot adapt as well to these segmented patterns.

---

## Visualizations (in `notebooks/Final_Analysis.ipynb`)

The notebook contains final-quality, well-labeled visualizations used to justify claims and support modeling decisions:

1. **Rent distribution histogram**  
   Shows the overall spread and skew of Boston-area rents.

2. **Rent by bedrooms (boxplot)**  
   Demonstrates rent increases with bedroom count, but with large overlap/variance.

3. **Rent vs square footage (scatter)**  
   Shows a general upward trend with substantial variance (size alone does not explain rent).

4. **Median rent by laundry option (bar chart)**  
   A categorical feature example showing certain amenities correlate with higher median rent.

5. **Rent vs luxury keyword count bucket (boxplot)**  
   Supports the claim that luxury/amenity language in descriptions is associated with higher rent.

6. **Median rent by distance-to-downtown bin (line plot)**  
   Shows a location premium trend: closer-to-downtown bins tend to have higher median rent.

7. **Geo-clusters (lat/long scatter + colorbar)**  
   Shows KMeans geo-clusters are spatially coherent neighborhood proxies.

8. **Geo-clusters over a Boston basemap (interactive Plotly map)**  
   - Makes cluster interpretation easier by showing where clusters fall geographically.
   - the basemap needs internet; otherwise it may not render.

9. **Monthly rent by geo-cluster (boxplot, includes -1)**  
   Shows geo-clusters have distinct rent distributions, supporting the neighborhood-proxy feature choice.

10. **Model performance comparison (bar chart of MAE)**  
   Directly visualizes baseline vs LinearSVR vs KNN performance (rubric requirement).

---

## Testing & Continuous Integration

- Minimal tests in `tests/test_basic.py`
- GitHub Actions workflow runs tests automatically on push/PR (`.github/workflows/test.yml`)

---

## Limitations

- Some fields are noisy or missing (sqft, coordinates, inconsistent text).
- Geo-clusters are **data-driven proxies**, not official neighborhood boundaries.
- KNN can underperform on rare “one-of-one” luxury listings because there may be few truly comparable neighbors.
