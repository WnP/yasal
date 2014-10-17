all:
	python setup.py sdist

clean:
	rm -rf dist yasal.egg-info

deploy:
	twine upload dist/*
