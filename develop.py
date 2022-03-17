#!/usr/bin/env python
import os

# Build out os independent paths
file_path = os.path.abspath(__file__)
repo_root = os.path.dirname(file_path)
frontend_dir = os.path.join(repo_root, "frontend")

os.chdir(repo_root)
# Remove previous containers so we get a fresh start.
os.system("docker rm -f $(docker ps -a -q);")

# Build the application server
os.system("docker-compose build app")

# Start postgres
os.system("docker-compose up -d db")

# Start app server
os.system("docker-compose up -d app")

# Build frontend assets js/css/fonts
os.chdir(frontend_dir)
os.system("npm run serve")
