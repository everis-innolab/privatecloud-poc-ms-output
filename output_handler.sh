#!/bin/bash
cp -r ../python/OutputHandlerNode .
cp -r ../python/EurekaLabLibrary .
docker build -f output_handler .
rm -r OutputHandlerNode
rm -r EurekaLabLibrary





