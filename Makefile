override PYTHON_IMAGE = python:3.6-alpine3.7
override APPLICATION_SCRIPT = inscripcion.py
override APPLICATION_FOLDER = inscripcion

install_dependencies:
	@docker run \
	  --rm \
	  --name install_dependencies \
	  -v $(shell pwd)/$(APPLICATION_FOLDER):/$(APPLICATION_FOLDER) \
	  -w /$(APPLICATION_FOLDER) \
	  $(PYTHON_IMAGE) \
	  sh  -c "python -m venv venv && source venv/bin/activate && pip install -r requirements.txt"

run_dev:
	@docker run \
	  --rm \
	  --name run_inscripcion \
	  -it \
	  -v $(shell pwd)/$(APPLICATION_FOLDER):/$(APPLICATION_FOLDER) \
	  -w /$(APPLICATION_FOLDER) \
	  --expose 5000 \
	  -p 5000:5000 \
	  -e FLASK_APP=$(APPLICATION_SCRIPT) \
	  -e FLASK_DEBUG=1 \
	  --env-file $(shell pwd)/.env \
	  $(PYTHON_IMAGE) \
	  sh -c "source venv/bin/activate && flask run --host=0.0.0.0"

ssh:
	@docker run \
	  --rm \
	  --name ssh_inscripcion \
	  -it \
	  -v $(shell pwd)/$(APPLICATION_FOLDER):/$(APPLICATION_FOLDER) \
	  -w /$(APPLICATION_FOLDER) \
	  $(PYTHON_IMAGE) \
	  sh -c "source venv/bin/activate && ash"

test:
	@docker run \
	  --rm \
	  --name test_inscripcion \
	  -v $(shell pwd)/$(APPLICATION_FOLDER):/$(APPLICATION_FOLDER) \
	  -w /$(APPLICATION_FOLDER) \
	  -e FLASK_APP=$(APPLICATION_SCRIPT) \
	  $(PYTHON_IMAGE) \
	  sh -c "source venv/bin/activate && flask test"
