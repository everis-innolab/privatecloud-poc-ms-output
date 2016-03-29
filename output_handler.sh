#!/bin/bash
cp -r ../python-eureka-library .
docker build -f output_handler .
rm -r python-eureka-library 





