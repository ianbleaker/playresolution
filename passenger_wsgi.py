import sys, os
cwd = os.getcwd()
sys.path.append(cwd)
sys.path.append(cwd + '/resolutionrpg')

INTERP = os.path.expanduser("~/venv/bin/python")

if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)

sys.path.insert(0,'$HOME/venv/bin')
sys.path.insert(0,'$HOME/venv/lib/python3.5/site-packages/django')
sys.path.insert(0,'$HOME/venv/lib/python3.5/site-packages')

os.environ['DJANGO_SETTINGS_MODULE'] = "resolutionrpg.settings"
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()