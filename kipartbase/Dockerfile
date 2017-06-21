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
                django \
                django-mptt \
                djangorestframework \
                django-filters \
                Pillow

COPY . /opt

EXPOSE 8100

CMD cd /opt && \
	python manage.py migrate && \
	python manage.py runserver 0.0.0.0:8100
