from fabric.api import run, sudo, local, cd, env

env.hosts = ['orlando.thraxil.org']
env.user = 'anders'

def restart_gunicorn():
    sudo("restart myopica", shell=False)

def prepare_deploy():
    local("./manage.py test")

def deploy():
    code_dir = "/var/www/myopica/myopica"
    with cd(code_dir):
        run("git pull origin master")
        run("make migrate")
        run("make collectstatic")
        run("make compress")
    restart_gunicorn()
