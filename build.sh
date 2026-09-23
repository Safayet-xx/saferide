#!/usr/bin/env bash
# Render runs this once per deploy: installs Python deps and builds React into frontend/dist
set -o errexit
pip install -r requirements.txt
cd frontend
npm install
npm run build
