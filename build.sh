#!/bin/bash

# use git bash|bash

pyinstaller --onefile --icon=atom.ico --clean --dist=bin src/atom.py
rm -r build
rm atom.spec

cp bin/atom.exe C:\\atom-prototype-release-v1\\bin
