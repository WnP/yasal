all:
	python setup.py sdist

clean:
	rm -rf build dist yasal.egg-info

deploy:
	twine upload dist/*
