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
  - Setup local_settings: `mv settings/local.py.example settings/local.py`
  - Edit `settings/local.py` to tailor to your machine.
