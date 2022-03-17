#!/usr/bin/env python
import os

# Build out os independent paths
file_path = os.path.abspath(__file__)
repo_root = os.path.dirname(file_path)
frontend_dir = os.path.join(repo_root, "frontend")

os.system("npm install npm@latest -g")
os.system("sudo npm install -g @vue/cli")
os.chdir(frontend_dir)
os.system("npm install")

os.chdir(repo_root)
# Remove previous containers so we get a fresh start.
os.system("docker rm -f $(docker ps -a -q);")

# Build the application server
os.system("docker-compose build app")

# Start postgres
os.system("docker-compose up -d db")

# Build frontend assets js/css/fonts
os.chdir(frontend_dir)
os.system("npm run build")

# Start NGINX
os.chdir(repo_root)
os.system("docker-compose up -d nginx")

# Start app server
os.system("docker-compose up app")
