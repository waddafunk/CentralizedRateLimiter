.PHONY: all help install format lint strip_notebooks

all: install strip_notebooks upgrade format lint 

help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  install           Install package dependencies"
	@echo "  format            Format code using black"
	@echo "  lint              Lint code using pylint"
	@echo "  strip_notebooks   Strip notebooks using nbstripout"
	@echo "  all               Run all targets"


install: 
	@echo "Installing dependencies..."
	pip install -r requirements.txt

format: 
	@echo "Formatting code..."
	 black .
	 nbqa black .
	 isort .
	 nbqa isort .

upgrade:
	@echo "Upgrading code"
	pyupgrade src/*/*.py
	nbqa pyupgrade notebooks/*.ipynb

lint: 
	@echo "Linting code..."
	pylint src/core/*.py --disable=C0114,C0115,C0116,R1725,C0103,W0621,W0603,R0914,E1101,W0622,R0903,W0702,W0212,W0102,R0912,R0915,C0301
	pylint src/cardano/*.py --disable=C0114,C0115,C0116,R1725,C0103,W0621,W0603,R0914,E1101,W0622,R0903,W0702,W0212,W0102,R0912,R0915,C0301
	pylint src/cosmos/*.py --disable=C0114,C0115,C0116,R1725,C0103,W0621,W0603,R0914,E1101,W0622,R0903,W0702,W0212,W0102,R0912,R0915,C0301

strip_notebooks: 
	@echo "Stripping notebooks..."
	nbstripout notebooks/*.ipynb

test: 
	@echo "Testing..."
	pytest -v --cov=src tests