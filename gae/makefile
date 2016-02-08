.PHONY: all clean run upload

PYTHON = C:\Python27\python.exe
APP_SERVER = $(PYTHON) "$(ProgramFiles)\Google\google_appengine\dev_appserver.py" --storage_path=.\ --enable_task_running=yes app.yaml
APP_CFG = $(PYTHON) "$(ProgramFiles)\Google\google_appengine\appcfg.py"

DEL = rm

all: run

run:
	$(APP_SERVER)
	#dev_appserver.py ./app.yaml

upload:
	$(APP_CFG) update app.yaml
#	gcloud config set project mfl-pipetechnology
#	gcloud preview app deploy app.yaml

clean:
	-$(DEL) *.pyc >nul
