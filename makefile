all:
	deactivate & python2 setup.py sdist

clean:
	deactivate & rm -rf venv dist yasal.egg-info

deploy:
	twine upload dist/*

dev:
	virtualenv2 venv && . venv/bin/activate && pip install -e .
