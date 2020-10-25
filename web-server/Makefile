export PYTHON_VERSION = python3.7


venv: requirements.txt
	(virtualenv venv --python=$$PYTHON_VERSION && \
	. venv/bin/activate && \
	pip3 install -r requirements.txt)


runserver: venv
	(. venv/bin/activate && \
	python manage.py runserver 3001)


clean:
	rm -rf venv