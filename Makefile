# Arcane incantation to print all the other targets, from https://stackoverflow.com/a/26339924
help:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

# Create conda environment with required dependencies
conda-update:
	conda env update --prune -f environment.yml

# Compile and install exact pip packages
pip-tools:
	pip install pip-tools pystan==2.19.1.1
	pip-compile requirements/dev.in && pip-compile requirements/prod.in
	pip-sync requirements/prod.txt requirements/dev.txt
	conda install -c conda-forge nb_conda_kernels nbclient nbconvert nbformat notebook -y

# Download complete data
load-data:
	cd lib && python data.py

# Run FastAPI server
run-app:
	uvicorn api.app:app --reload --host 0.0.0.0 --port 8080

# Build and Run Docker Container
docker-run:
	cp requirements/prod.txt requirements.txt
	docker build -t registry.heroku.com/airq-forecast-app/web -f api/Dockerfile .
	docker run --name airq-forecast-app -e PORT=8008 -p 8008:8008 -d registry.heroku.com/airq-forecast-app/web:latest

docker-stop:
	docker stop airq-forecast-app
	docker rm airq-forecast-app

# Push docker image to registry and release it
heroku-docker:
	docker push registry.heroku.com/airq-forecast-app/web
	heroku container:release -a airq-forecast-app web


# Run streamlit app
st-run:
	streamlit run streamlit/app.py