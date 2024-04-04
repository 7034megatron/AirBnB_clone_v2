#!/usr/bin/env bash
# Script that sets up web servers for deployment of web_static

# Install Nginx if not already installed
if ! [ -x "$(command -v nginx)" ]; then
    sudo apt-get -y update
    sudo apt-get -y install nginx
fi

# Create necessary directories if they don't exist
sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared

# Create a fake HTML file for testing Nginx configuration
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to serve content of /data/web_static/current/ to hbnb_static
config_file="/etc/nginx/sites-available/default"
sudo sed -i '/^\tlocation \/ {/a\\n\t\tlocation /hbnb_static {\n\t\t\talias /data/web_static/current/;\n\t\t}\n' "$config_file"

# Restart Nginx
sudo service nginx restart

exit 0
