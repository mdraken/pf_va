.PHONY: clean train-nlu train-core cmdline server

TEST_PATH=./

help:
	@echo "    clean"
	@echo "        Remove python artifacts and build artifacts."
	@echo "    train-nlu"
	@echo "        Trains a new nlu model using the projects Rasa NLU config."
	@echo "    train-core"
	@echo "        Trains a new dialogue model using the story training data."
	@echo "    action-server"
	@echo "        Starts the server for custom action."
	@echo "    interactive"
	@echo "        Starts interactive training using the current model."
	@echo "    cmdline"
	@echo "        This will load the assistant in your terminal for you to chat."
	@echo "    run-cmdline"
	@echo "        This will load the assistant in your terminal for you to chat in debug mode."
clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f  {} +
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf docs/_build

train-nlu:
	python  -m rasa_nlu.train -c nlu_config.yml --data data/nlu_data.md -o models --fixed_model_name nlu --project current --verbose

train-core:
	python -m rasa_core.train -d domain.yml -s data/core -o models/current/dialogue -c core_config.yml

interactive:
	python -m rasa_core.train interactive --core models/current/dialogue -d domain.yml -c core_config.yml -u models/current/nlu --endpoints endpoints.yml --debug

cmdline:
	python -m rasa_core.run -d models/current/dialogue -u models/current/nlu --endpoints endpoints.yml

action-server:
	python -m rasa_core_sdk.endpoint --actions actions

run-cmdline:
	python -m rasa_core.run -d models/current/dialogue -u models/current/nlu --debug --endpoints endpoints.yml

telegram:
	python -m rasa_core.run -d models/current/dialogue -u models/current/nlu --port 5005 --credentials credentials.yml --endpoints endpoints.yml

Restapi:
    python -m rasa_core.run -d models/current/dialogue -u models/current/nlu --endpoints endpoints.yml --port 5002 --credentials credentials.yml

