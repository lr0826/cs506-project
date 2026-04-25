.PHONY: setup run_notebook test clean

VENV=.venv
PY=$(VENV)/bin/python

setup:
	python3 -m venv $(VENV)
	$(PY) -m pip install --upgrade pip
	$(PY) -m pip install -r requirements.txt

run_notebook:
	$(PY) -m jupyter nbconvert --to notebook --execute notebooks/Final_Analysis.ipynb --output executed_Final_Analysis.ipynb

test:
	$(PY) -m pytest -q

clean:
	rm -f notebooks/executed_Final_Analysis.ipynb