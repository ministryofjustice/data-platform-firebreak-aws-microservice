lint:
	black .
	isort .
	flake8 .


runserver:
	uvicorn app.api.main:app --reload
