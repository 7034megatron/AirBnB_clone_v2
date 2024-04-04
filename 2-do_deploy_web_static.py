#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""
from fabric.api import env, run, put
from os.path import exists


env.hosts = ['<IP web-01>', '<IP web-02>']  # Replace with your web servers' IPs
env.user = 'ubuntu'  # Replace with your SSH username
env.key_filename = '/path/to/your/ssh/private/key'  # Replace with the path to your SSH private key


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers

    Args:
        archive_path (str): Path to the archive to be deployed

    Returns:
        bool: True if all operations have been done correctly, False otherwise
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Extract the archive to the /data/web_static/releases/ directory
        archive_filename = archive_path.split('/')[-1]
        folder_name = archive_filename.split('.')[0]
        release_path = '/data/web_static/releases/{}'.format(folder_name)
        run('mkdir -p {}'.format(release_path))
        run('tar -xzf /tmp/{} -C {}'.format(archive_filename, release_path))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(archive_filename))

        # Move contents of extracted folder to parent directory
        run('mv {}/web_static/* {}'.format(release_path, release_path))

        # Delete the empty folder
        run('rm -rf {}/web_static'.format(release_path))

        # Update symbolic link
        current_link = '/data/web_static/current'
        run('rm -rf {}'.format(current_link))
        run('ln -s {} {}'.format(release_path, current_link))

        return True
    except Exception as e:
        return False


if __name__ == "__main__":
    # Usage example
    do_deploy("versions/web_static_20170315003959.tgz")
