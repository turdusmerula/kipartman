#!/bin/bash

xpl_path=$(cd -P -- "$(dirname -- "$0")" && pwd -P)
cd $xpl_path

if [ ! -f /tmp/swagger-codegen-cli.jar ]
then
	wget http://central.maven.org/maven2/io/swagger/swagger-codegen-cli/2.2.2/swagger-codegen-cli-2.2.2.jar -O /tmp/swagger-codegen-cli.jar
fi

# generate client
rm -rf client
java -jar /tmp/swagger-codegen-cli.jar generate \
  -i api.yaml \
  -l python \
  -o client/

# copy client inside kipartman
cd client
swagger_client=${xpl_path}/../kipartman/swagger_client
rsync --delete -rv swagger_client/ ${swagger_client}
cd -

# generate server
rm -rf server
java -jar /tmp/swagger-codegen-cli.jar generate \
  -i api.yaml \
  -l python-flask \
  -o server/ \
  -D supportPython2=true

# patch main to change flask parameters
sed -i -e "s/8080/8200, debug=True/g" server/swagger_server/__main__.py
sed -i -e "s/\.encoder/encoder/g" server/swagger_server/__main__.py

# patch category.py to remove wrong recursive import
sed -i -e "s/from swagger_server.models.part_category import PartCategory//g" server/swagger_server/models/part_category.py

# copy server inside kipartbase
cd server
swagger_server=${xpl_path}/../kipartbase/swagger_server
mkdir -p ${swagger_server}
if [ ! -d ${swagger_server}/controllers ]
then
	cp -vr swagger_server/controllers ${swagger_server}
fi
if [ ! -d ${swagger_server}/test ]
then
	cp -vr swagger_server/test ${swagger_server}
fi
cp -f swagger_server/*.py $swagger_server
rsync --delete -rv swagger_server/models/ ${swagger_server}/models
rsync --delete -rv swagger_server/swagger/ ${swagger_server}/swagger
cd -
