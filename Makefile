run:
	uvicorn main:app --reload

seed:
	python scripts/seed_minimal.py

install:
	pip install -r requirements.txt