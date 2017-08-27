# Fairblogs

Source of www.fairblogs.nl, including
- Django website setup and standard HTML, CSS, JS files.

Site code structure:

- **Dependencies**
  - Python 3.6.0
  - Django 1.11.2
  - See requirements.txt for package dependencies 
  - Note that iPython and its dependencies are not strictly necessary

- **Installation**
  - Create virtualenvironment: `virtualenv venv` op toplevel
  - Activate virtualenv: `source venv/bin/activate`
  - Create debug directory: `mkdir -p venv/debug`

  - Install required packages: `pip install -r requirements.txt`
  - Create static/img dir: `mkdir -p static/img`
  - Setup local_settings: `mv settings/local.py.example settings/local.py`
  - Edit `settings/local.py` to tailor to your machine.


- ** Add development url to Site **
  - Only needed when using latest mysql dump converted to sqlite3 db
  - In [1]: `from django.contrib.sites.models import Site`
  - In [2]: `new_site = Site.objects.create(domain="127.0.0.1:8000", name="127.0.0.1:8000")`
  - In [3]: `new_site = Site.objects.create(domain="localhost:8000", name="localhost:8000")`

- ** Production **
  - `mkdir -p static/img static/_versions`
  - `setfacl -R -d -m u::rwx,u:www-data:rwx,g::rwx,o:rx static`
  - `setfacl -R -d -m u::rwx,u:fairblogs:rwx,g::rwx,o:rx static`
  - `setfacl -R -m u::rwx,u:www-data:rwx,g::rwx,o:rx static`
  - `setfacl -R -m u::rwx,u:fairblogs:rwx,g::rwx,o:rx static`
