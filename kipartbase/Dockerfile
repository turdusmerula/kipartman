from debian:jessie


RUN apt-get update && \
        apt-get upgrade -y && \
        apt-get install -y \
        	bash \
        	vim \
        	python \
        	python-pip \
        	zlib1g-dev \
        	libjpeg-dev \
        	python-dev 

RUN pip install pip --upgrade && \
        pip install \
			kipartman

COPY . /opt

EXPOSE 8100

CMD cd /opt && \
	python manage.py migrate && \
	kipartbase
