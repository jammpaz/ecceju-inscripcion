override PYTHON_IMAGE = python:3.6-alpine3.7
override APPLICATION_SCRIPT = inscripcion.py
override APPLICATION_FOLDER = inscripcion
override IMAGE_TAG = ecceju/inscripcion

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
	  -e FLASK_APP=$(APPLICATION_SCRIPT) \
	  -w /$(APPLICATION_FOLDER) \
	  $(PYTHON_IMAGE) \
	  sh -c "source venv/bin/activate && ash"

test:
	@docker run \
	  --rm \
	  --name test_inscripcion \
	  -v $(shell pwd)/$(APPLICATION_FOLDER):/$(APPLICATION_FOLDER) \
	  -w /$(APPLICATION_FOLDER) \
	  -e SECRET_KEY='secret' \
	  -e FLASK_APP=$(APPLICATION_SCRIPT) \
	  $(PYTHON_IMAGE) \
	  sh -c "source venv/bin/activate && flask test"


build_image:
	@docker build \
	  -t $(IMAGE_TAG):latest \
	  -f $(APPLICATION_FOLDER)/Dockerfile \
	  $(APPLICATION_FOLDER)


run_container:
	@docker run \
	  --rm \
	  --name ecceju-inscripcion-container \
	  -e PORT=5000 \
	  -e SECRET_KEY=secure-key \
	  --expose 5000 \
	  $(IMAGE_TAG):latest


define deploy_to
	docker tag $(IMAGE_TAG):latest registry.heroku.com/$(1)/web
	@docker login --username=_ --password=$(2) registry.heroku.com
	docker push registry.heroku.com/$(1)/web
endef

deploy_to_qa:
	$(call deploy_to,ecceju-inscripcion-qa,$(TOKEN))

deploy_to_prod:
	$(if $(filter no, $(BUILD_DEBUG)), \
	  $(call deploy_to,ecceju-inscripcion,$(TOKEN)), \
	  @echo "INFO: This build will not be deployed on production environment")

setup_credentials:
	@echo $(value HEROKU_SECRETS) | base64 --decode > ~/.netrc

clean_credentials:
	rm ~/.netrc
