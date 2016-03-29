#!/bin/bash
cp -r ../python-eureka-library .
docker build -f Dockerfile .
rm -r python-eureka-library 





