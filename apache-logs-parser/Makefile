.PHONY: venv
venv:
	python3.11 -m venv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements.txt

.PHONY: run
run:
	podman compose up --build
