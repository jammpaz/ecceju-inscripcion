override PYTHON_IMAGE = python:3.6-alpine3.7

install_dependencies:
	@docker run \
	  --rm \
	  --name install_dependencies \
	  -v $(shell pwd)/inscripcion:/inscripcion \
	  -w /inscripcion \
	  $(PYTHON_IMAGE) \
	sh  -c "python -m venv venv && source venv/bin/activate && pip install -r requirements.txt"

run_inscripcion:
	@docker run \
	  --rm \
	  --name run_inscripcion \
	  -v $(shell pwd)/inscripcion:/inscripcion \
	  -w /inscripcion \
	  --expose 5000 \
	  $(PYTHON_IMAGE) \
	  sh -c "source venv/bin/activate && python inscripcion.py"

ssh_inscripcion:
	@docker run \
	  --rm \
	  --name ssh_inscripcion \
	  -it \
	  -v $(shell pwd)/inscripcion:/inscripcion \
	  -w /inscripcion \
	  $(PYTHON_IMAGE) \
	  ash

