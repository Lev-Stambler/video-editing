#!/bin/sh
# chmod all necessary files
chmod +x ./setup.sh
chmod +x _scripts/download-deps.sh
chmod +x _scripts/install-opencv.sh


./_scripts/download-deps.sh
./_scripts/install-opencv.sh