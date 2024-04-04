#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the web_static folder
"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder

    Returns:
        str: Path to the archive if it has been correctly generated, None otherwise
    """
    try:
        # Create versions directory if it doesn't exist
        local("mkdir -p versions")

        # Generate timestamp for archive name
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")

        # Create the .tgz archive
        archive_path = "versions/web_static_{}.tgz".format(timestamp)
        local("tar -cvzf {} web_static".format(archive_path))

        return archive_path
    except Exception as e:
        return None


if __name__ == "__main__":
    do_pack()
