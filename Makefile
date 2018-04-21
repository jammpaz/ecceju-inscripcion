override PYTHON_IMAGE = python:3.6-alpine3.7

install_dependencies:
	@docker run \
	  --rm \
	  --name install_dependencies \
	  -v $(shell pwd)/inscripcion:/inscripcion \
	  -w /inscripcion \
	  $(PYTHON_IMAGE) \
	sh  -c "python -m venv venv && source venv/bin/activate && pip install -r requirements.txt"

run:
	@docker run \
	  --rm \
	  --name run_inscripcion \
	  -it \
	  -v $(shell pwd)/inscripcion:/inscripcion \
	  -w /inscripcion \
	  --expose 5000 \
	  -e FLASK_APP=inscripcion.py \
	  $(PYTHON_IMAGE) \
	  sh -c "source venv/bin/activate && flask run --host=0.0.0.0"

ssh:
	@docker run \
	  --rm \
	  --name ssh_inscripcion \
	  -it \
	  -v $(shell pwd)/inscripcion:/inscripcion \
	  -w /inscripcion \
	  $(PYTHON_IMAGE) \
	  ash

test:
	@docker run \
	  --rm \
	  --name test_inscripcion \
	  -v $(shell pwd)/inscripcion:/inscripcion \
	  -w /inscripcion \
	  -e FLASK_APP=inscripcion.py \
	  $(PYTHON_IMAGE) \
	  sh -c "source venv/bin/activate && flask test"

