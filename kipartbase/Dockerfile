from ubuntu:16.04


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

RUN apt-get install -y libgtk-3-dev
RUN apt-get install -y mesa-common-dev
RUN apt-get install -y libglu1-mesa-dev
#RUN apt-get install -y libgstreamer1.0-dev
RUN apt-get install -y libgtk2.0-dev libgtk-3-dev \
	libjpeg-dev libtiff-dev \
	libsdl1.2-dev libgstreamer-plugins-base0.10-dev \
	libnotify-dev freeglut3 freeglut3-dev libsm-dev \
	libwebkitgtk-dev libwebkitgtk-3.0-dev

RUN pip install pip --upgrade && \
        pip install kipartman 

COPY . /opt

EXPOSE 8100

CMD cd /opt && \
	python manage.py migrate && \
	kipartbase
