export PYTHON_VERSION = python3.7


venv: requirements.txt venv
	(virtualenv venv --python=$$PYTHON_VERSION && \
	. venv/bin/activate && \
	pip3 install -r requirements.txt)


clean:
	rm -rf venv