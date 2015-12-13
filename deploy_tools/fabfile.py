from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

"""
Fabric is a tool which lets you automate commands
that you want to run on servers.

usually how to run:
fab function_name,host=SERVER_ADDRESS

specifically (from above):
fab deploy:host=gob@staging.mangojollyjolly.xyz
"""

REPO_URL = 'http://github.com/jessechiem/tddexample.git'

def deploy():
    # env.host will contain the address of the server
    # we've specified at the command line,
    # e.g, staging.mangojollyjolly.xyz
    site_folder = '/home/%s/sites/%s' % (env.user, env.host)
    source_folder = site_folder + '/source'
    # why underscore? to indicate that they're not
    # meant to be part of the "public API" of the fabfile.
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)

def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run('mkdir -p %s/%s' % (site_folder, subfolder))

def _get_latest_source(source_folder):
    """ pull down our source code """
    if exists(source_folder + '/.git'):
        run('cd %s && git fetch' % (source_folder,))
    else:
        # alternatively, we use git clone with the
        # repo URL to bring down a fresh source tree
        run('git clone %s %s' % (REPO_URL, source_folder))

    # local is just a wrapper around subprocess.Popen
    current_commit = local("git log -n 1 --format=%H", capture=True)
    # reset --hard to that commit
    run('cd %s && git reset --hard %s' % (source_folder, current_commit))

def _update_settings(source_folder, site_name):
    """ update our settings file, to set the ALLOWED_HOSTS
    and DEBUG, and to create a new secret key. """
    settings_path = source_folder + '/superlists/settings.py'
    # string sub from True to False
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path,
        'ALLOWED_HOSTS =.+$',
        'ALLOWED_HOSTS = ["%s"]' % (site_name,)
    )
    secret_key_file = source_folder + '/superlists/secret_key.py'
    # generate a new key to import into settings,
    # if there isn't one there already
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '%s'" % (key,))
    # use relative import to be ABSOLUTELY SURE we're
    # importing the local module, rather than the one
    # from somewhere else on sys.path
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')

def _update_virtualenv(source_folder):
    """ Create or update the virtualenv """
    virtualenv_folder = source_folder + '/../virtualenv'
    # check if pip already exists
    if not exists(virtualenv_folder + '/bin/pip'):
        run('virtualenv --python=python3 %s' % (virtualenv_folder,))
    run('%s/bin/pip install -r %s/requirements.txt' % (
        virtualenv_folder, source_folder
    ))

def _update_static_files(source_folder):
    # make sure we use the virtualenv version of Django,
    # and not the system one.
    run('cd %s && ../virtualenv/bin/python3 manage.py collectstatic --noinput' % (
        source_folder,
    ))

def _update_database(source_folder):
    """ update the database with manage.py migrate """
    run('cd %s && ../virtualenv/bin/python3 manage.py migrate --noinput' % (source_folder,))
