#!/bin/bash

xpl_path=$(cd -P -- "$(dirname -- "$0")" && pwd -P)
cd $xpl_path

if [ ! -f /tmp/swagger-codegen-cli.jar ]
then
#	wget http://central.maven.org/maven2/io/swagger/swagger-codegen-cli/2.2.2/swagger-codegen-cli-2.2.2.jar -O /tmp/swagger-codegen-cli.jar
	wget http://central.maven.org/maven2/io/swagger/swagger-codegen-cli/2.2.3/swagger-codegen-cli-2.2.3.jar -O /tmp/swagger-codegen-cli.jar
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
#sed -i -e "s/8080/8200, debug=True/g" server/swagger_server/__main__.py
#sed -i -e "s/\.encoder/encoder/g" server/swagger_server/__main__.py
#cat static_files.py.tpl >> server/swagger_server/__main__.py

# patch py files to remove wrong recursive imports
sed -i -e "s/from swagger_server.models.part_category import PartCategory//g" server/swagger_server/models/part_category.py
sed -i -e "s/from swagger_server.models.part import Part//g" server/swagger_server/models/part.py
sed -i -e "s/from swagger_server.models.footprint_category import FootprintCategory//g" server/swagger_server/models/footprint_category.py
sed -i -e "s/from swagger_server.models.model_category import ModelCategory//g" server/swagger_server/models/model_category.py
sed -i -e "s/from swagger_server.models.storage_category import StorageCategory//g" server/swagger_server/models/storage_category.py

# patch py files to allow usage of name Model
find server/swagger_server -name "*.py" -exec sed -i -e "s#from .base_model_ import Model#from .base_model_ import Model as BaseModel#g" {} \;
find server/swagger_server -name "*.py" -exec sed -i -e "s#(Model)#(BaseModel)#g" {} \;

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
# add an init for packaging
touch ${swagger_server}/swagger/__init__.py
cd -

echo "-------- ${swagger_server}"
cat __main__.py.tpl
cat __main__.py.tpl > ${swagger_server}/__main__.py

