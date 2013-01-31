#!/bin/sh
rm -rf *.pyc
java -Xmx1000M -jar ISSVis.jar -exec ./cli.py -beta $1