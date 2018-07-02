override PYTHON_IMAGE = python:3.6-alpine
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
	  sh  -c "apk --no-cache add build-base postgresql-dev && python -m venv venv && venv/bin/pip install -r requirements.txt && venv/bin/pip install psycopg2 psycopg2-binary"

run_db:
	@docker container run \
	  --name db_inscripcion \
	  --rm \
	  -d \
	  --env-file $(shell pwd)/.db.env \
	  postgres:10.4-alpine

stop_db:
	@docker container rm --force db_inscripcion

run_dev:
	@docker container run \
	  --rm \
	  --name run_inscripcion \
	  -it \
	  -v $(shell pwd)/$(APPLICATION_FOLDER):/$(APPLICATION_FOLDER) \
	  -w /$(APPLICATION_FOLDER) \
	  --expose 5000 \
	  -p 5000:5000 \
	  -e FLASK_APP=$(APPLICATION_SCRIPT) \
	  -e FLASK_DEBUG=1 \
	  --env-file $(shell pwd)/.db.env \
	  --env-file $(shell pwd)/.env \
	  --link db_inscripcion:db_inscripcion \
	  $(PYTHON_IMAGE) \
	  sh -c "apk --no-cache add build-base postgresql-dev && source venv/bin/activate && flask run --host=0.0.0.0"

ssh:
	@docker run \
	  --rm \
	  --name ssh_inscripcion \
	  -it \
	  -v $(shell pwd)/$(APPLICATION_FOLDER):/$(APPLICATION_FOLDER) \
	  -e FLASK_APP=$(APPLICATION_SCRIPT) \
	  --env-file $(shell pwd)/.env \
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
	  -e SECRET_KEY=secret \
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
	heroku container:release web --app $(1)
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
