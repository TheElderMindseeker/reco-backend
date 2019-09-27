install:
	python setup.py develop

run:
	export DATABASE_URI="postgres://mwgmwexo:gMBph3c8C0UTflHDIq07jmfEM_2USKf8@balarama.db.elephantsql.com:5432/mwgmwexo"
	gunicorn trash:app

test:
	export TEST_DATABASE_URI="sqlite:///tmp/trash.db"
	pytest -v
