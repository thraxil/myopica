from fabric.api import run, sudo, local, cd, env

env.hosts = ['orlando.thraxil.org']
nginx_hosts = ['lolrus.thraxil.org']
env.forward_agent = True

def restart_gunicorn():
    sudo("restart myopica")

def prepare_deploy():
    local("./manage.py test")

def deploy():
    code_dir = "/var/www/myopica/myopica"
    with cd(code_dir):
        run("git pull origin master")
        run("./bootstrap.py")
        run("./manage.py migrate")
        run("./manage.py collectstatic --noinput --settings=myopica.settings_production")
        for n in nginx_hosts:
            run(("rsync -avp --delete media/ "
                 "%s:/var/www/myopica/myopica/media/") % n)
    restart_gunicorn()
