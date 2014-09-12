# coding: utf8
"""
Author: Ilcwd
"""
import datetime
import os


# noinspection PyPackageRequirements
from fabric.api import put, cd, sudo, local, lcd, env
# noinspection PyPackageRequirements
from fabric.decorators import task, hosts
# noinspection PyPackageRequirements
from fabric.contrib import files


# server name
PROJECT_NAME = 'hodao'

# configs need to replace
REPLACE_CONFIGS = [
    'deployment/config.json',
    'deployment/logging.yaml',
]


# deploy hosts
@task
def production():
    env.hosts = [
        'root@182.92.107.122',
    ]


# deploy user
env.user = 'chenwenda'


# some useful variables
LOCAL_CWD = os.getcwd()
TAR_NAME = "%s.%s.tar" % (PROJECT_NAME, datetime.datetime.now().strftime("%Y%m%d"),)
LOCAL_TAR_PATH = os.path.join(LOCAL_CWD, TAR_NAME)
REMOTE_PROJECT_PATH = os.path.join('/data/apps/', PROJECT_NAME)
REMOTE_APP_CURRENT_PATH = os.path.join(REMOTE_PROJECT_PATH, 'current')
REMOTE_APP_REAL_FOLDER = '%s.%s' % (PROJECT_NAME, datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
REMOTE_APP_REAL_PATH = os.path.join(REMOTE_PROJECT_PATH, REMOTE_APP_REAL_FOLDER)
REMOTE_TAR_PATH = os.path.join(REMOTE_PROJECT_PATH, TAR_NAME)
REMOTE_RUN_SCRIPT_NAME = 'runuwsgi.sh'
REMOTE_RUN_SCRIPT_PATH = os.path.join(REMOTE_PROJECT_PATH, REMOTE_RUN_SCRIPT_NAME)


# some useful functions
def init_env():
    if not files.exists(REMOTE_PROJECT_PATH, use_sudo=True):
        sudo('mkdir %s' % REMOTE_PROJECT_PATH)


def runuwsgi(cmd, warn_only=False):
    with cd(REMOTE_PROJECT_PATH):
        sudo("./%s %s" % (REMOTE_RUN_SCRIPT_NAME, cmd), warn_only=warn_only)


def debug(*a):
    now = datetime.datetime.now()
    print now, ' '.join(str(i) for i in a)


def upload(local, remote):
    return put(local, remote, use_sudo=True, mirror_local_mode=True)


################################
# Tasks
################################
@hosts('0.0.0.0')
@task
def pack():
    local("rm -f %s" % (TAR_NAME,))
    local("tar -czvf %s *" % (TAR_NAME, ))


def init():
    file_location = [
        ('deployment/hodao.logrotate.conf', '/etc/logrotate.d/hodao.logrotate.conf'),
        ('deployment/hodao.nginx.conf', '/etc/nginx/conf.d/hodao.nginx.conf'),
    ]

    for local_, remote in file_location:
        upload(local_, remote)

    if not files.exists(REMOTE_PROJECT_PATH, use_sudo=True):
        sudo('mkdir %s' % REMOTE_PROJECT_PATH)


@task
def uwsgi(cmd, warn_only=0):
    runuwsgi(cmd, bool(int(warn_only)))


@task
def deploy(start=1):
    # 1. initialize environment
    init_env()

    local("rm -f %s" % (TAR_NAME,))
    local("tar -czvf %s *" % (TAR_NAME, ))

    # 2. upload and extract source code
    put(LOCAL_TAR_PATH, REMOTE_TAR_PATH, use_sudo=True, mirror_local_mode=True)

    sudo("mkdir %s" % REMOTE_APP_REAL_PATH)
    with cd(REMOTE_PROJECT_PATH):
        sudo('mv %s %s' % (TAR_NAME, REMOTE_APP_REAL_PATH))

    with cd(REMOTE_APP_REAL_PATH):
        sudo('tar -xf %s' % TAR_NAME)
        sudo('rm -f %s' % TAR_NAME)

    # 3. if old code exists, try to stop service and replace configs
    if files.exists(REMOTE_APP_CURRENT_PATH, use_sudo=True):
        runuwsgi('stop', warn_only=True)

        # replace configs
        with cd(REMOTE_PROJECT_PATH):
            for c in REPLACE_CONFIGS:
                sudo('rm -f %s/%s' % (REMOTE_APP_REAL_FOLDER, c))
                sudo('cp %s/%s  %s/%s' % (REMOTE_APP_CURRENT_PATH, c, REMOTE_APP_REAL_FOLDER, c))

        sudo('rm -f %s' % REMOTE_APP_CURRENT_PATH)
    else:
        debug("[INFO]Remote folder(%s) does not exist." % (REMOTE_APP_CURRENT_PATH,))

    # 4. if `runuwsgi.sh` does not exist, copy from source code.
    if not files.exists(REMOTE_RUN_SCRIPT_PATH, use_sudo=True):
        with cd(REMOTE_PROJECT_PATH):
            sudo('cp %s/%s %s' % (REMOTE_APP_REAL_FOLDER, REMOTE_RUN_SCRIPT_NAME, REMOTE_RUN_SCRIPT_PATH))
        debug("[INFO]File `%s` does not exist, copy it from newly-upload code, "
              "you may need to modify it" %
              (REMOTE_RUN_SCRIPT_PATH,))

    # 5. make `current` soft link.
    sudo('ln -s %s %s' % (REMOTE_APP_REAL_PATH, REMOTE_APP_CURRENT_PATH))

    if int(start):
        # 6. start service
        runuwsgi('start')







