FROM python:3.9-bullseye

ENV PYTERRIER_VERSION='5.7'
ENV PYTERRIER_HELPER_VERSION='0.0.7'

RUN apt-get update \
	&& apt-get install -y git openjdk-11-jdk \
	&& pip3 install python-terrier pandas jupyterlab runnb \
	&& python3 -c "import pyterrier as pt; pt.init(version='${PYTERRIER_VERSION}', helper_version='${PYTERRIER_HELPER_VERSION}');" \
	&& python3 -c "import pyterrier as pt; pt.init(version='${PYTERRIER_VERSION}', helper_version='${PYTERRIER_HELPER_VERSION}', boot_packages=['com.github.terrierteam:terrier-prf:-SNAPSHOT']);"

ENV TRANSFORMERS_CACHE=/data/model/transformer-cache/
ENV IR_DATASETS_HOME=/data/dataset/ir_datasets-cache/

COPY . . 
RUN pip install -r requirements.txt

ENV METHOD='pyterrier'
ENV TYPE='index'

ENTRYPOINT ["python","./run.py"]
