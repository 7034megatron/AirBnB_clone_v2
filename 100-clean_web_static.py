#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives
"""
from fabric.api import env, run, local, lcd
from datetime import datetime


env.hosts = ['<IP web-01>', '<IP web-02>']  # Replace with your web servers' IPs
env.user = 'ubuntu'  # Replace with your SSH username
env.key_filename = '/path/to/your/ssh/private/key'  # Replace with the path to your SSH private key


def do_clean(number=0):
    """
    Deletes out-of-date archives

    Args:
        number (int): Number of archives to keep. If 0 or 1, keep only the most recent archive.
                      If 2, keep the most recent and second most recent archives, etc.
    """
    try:
        number = int(number)
    except ValueError:
        print("Error: Please provide a valid integer for 'number'.")
        return

    if number < 0:
        print("Error: 'number' must be a non-negative integer.")
        return

    # Get list of archives sorted by modification time
    with lcd('versions'):
        archives = local("ls -t", capture=True).split("\n")

    # Delete unnecessary archives in versions folder
    for archive in archives[number:]:
        local("rm versions/{}".format(archive))

    # Delete unnecessary archives in /data/web_static/releases folder on both web servers
    for archive in archives[number:]:
        run("rm /data/web_static/releases/{}".format(archive))

    print("Old archives cleaned successfully!")


if __name__ == "__main__":
    # Usage example
    do_clean(2)
