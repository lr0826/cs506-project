# Boston Rent Prediction from Listings (CS506 Project Proposal)

## Description of the project
This project aims to study and predict monthly apartment rent prices in the Boston area using information from online rental listings. I will collect real listing data (price and listing attributes) and build a dataset that can be used to analyze which factors (bedrooms, bathrooms, neighborhood/location, amenities, listing text) are most associated with rent differences. The final outcome will be a clean dataset and a prediction task focused on estimating rent from listing features.

## Clear goal(s)
- **Primary goal:** Successfully build a model that can predict the monthly rent price of a Boston-area apartment listing using listing features, and outperform a baseline model that always predicts the median rent.
- **Secondary goal:** Identify which listing features appear most influential for rent (for example, bedrooms/bathrooms, neighborhood, and common amenities).

## Data collection plan (what data + how to collect it)

### Data needed
For each rental listing, I plan to collect:
- Rent price
- Bedrooms / bathrooms
- Neighborhood or location label
- Other listing attributes when available (e.g., square footage, laundry, parking, pets allowed, furnished)
- Listing title + description text (to capture amenities/keywords not in structured fields)
- Posting date (to track time effects and support time-based analysis if needed)

### How I will collect it
- I will collect rental data from multiple potential sources, including Craigslist Boston housing listings, the Kaggle Craigslist Housing dataset (filtered to the Boston area), and publicly available housing/rent data from platforms such as Zillow and Redfin.
- I will write a Python script to scrape listing pages and extract the fields above into a structured format (CSV/JSON).

### Backup plan (if scraping becomes difficult)
If scraping is unreliable or restricted, I will use a public housing listings dataset (such as the Kaggle Craigslist housing dataset filtered to the Boston area) and proceed with the same prediction goal and analysis plan.

## Project timeline (rough estimate by subtask)
- Data collection (scraping / dataset gathering): ~2 weeks
- Data cleaning + deduplication + formatting: ~1–2 weeks
- Exploratory data analysis: ~1 week
- Modeling (first real model): ~1 week
- Feature engineering (amenities from text, neighborhood encoding, etc.): ~1–2 weeks
- Model iteration + evaluation (compare models, error analysis): ~3 weeks
- Final packaging (Makefile, minimal tests, workflow, README write-up, presentation): ~3 days
