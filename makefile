all:
	python2 setup.py sdist

clean:
	rm -rf dist yasal.egg-info

deploy:
	twine upload dist/*
