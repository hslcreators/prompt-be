# prompt-be

This is a `Python / Django` project.

<img align="left" alt="Python" width="40px" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" />

<img align="left" alt="Django" width="40px" src="https://github.com/devicons/devicon/blob/v2.15.1/icons/django/django-plain.svg" />

<h1></h1>

## Getting Started

After cloning the repository, here are the things to do:

First, navigate to the folder where the repository was cloned too it should have a python file `manage.py` in it. This is your root_directory.

> Note: The term 'root_directory' is a term used to describe the folder wher `manage.py` is located

Secondly, create a virtual environment folder in the root_directory:

```bash
python -m venv env
```

> Note!! You may have to install virtualenv with the command `pip install virtualenv`

Then , activate the virtual environment :

```bash
.\env\Scripts\activate
```

> Please note to make use of backslash `\` and not frontslash `/` as seen above.

Now you should see `(env)` on your terminal. This indicates that your virtual environment has been created and activated.

And install all the requirements:

```bash
pip install -r requirements.txt
```

You should see all the python requirements installing in your terminal.

Once all the downloads have finished, you can run the server using this command:

```bash
python manage.py runserver
```

The following log message should be displayed in console output:

```bash
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.
November 15, 2023 - 20:40:12
Django version 4.2.6, using settings 'PromptBE.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

> Note!! If the schema was updated, run the following command to apply the updated changes: `python manage.py makemigrations` then `python manage.py migrate`.

Visit `http://127.0.0.1:8000/test/` in your browser just to confirm routes are configured and working properly. If all is working properly, you should get the below response on browser.

```python
Everythings working fine!
```

## Environmental Variable

Create a `.env` file inside the `root_directory` and include the following content:

```bash
DEBUG_MODE=True
SECRET_KEY = your_secret_key
EMAIL_BACKEND = the_email_backend
EMAIL_HOST = the_email_host
EMAIL_PORT = the_email_port
EMAIL_USE_TLS = the_email_tls
EMAIL_HOST_USER = the_host_email
EMAIL_HOST_PASSWORD = the_host_email_password
```

> Note!! you need to get the values for the Environmental Variables from your Team Lead. <a href='https://github.com/TSavage101'> Bayode </a>

That's as far as the application setup goes.

# Routes

This is a brief overview of the route structure in my Django project.

## Project-level URLs

The main URL configuration for the entire project is defined in the `urls.py` file at the project level. Here's an example:

```python
# prompt-be/PromptBE/urls.py

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', include('app.urls')),
    # Other app-specific URLs
]
```

## App-level URLs

An app URL configuration for a particular app is defined in the `urls.py` file at the app level. Here's an example:

```python
# prompt-be/apps/{app_name}/urls.py

from django.urls import path

from . import views

urlpatterns = [
   path('url_route/', views.url_view, name='url_route_name'),
   # More URL routes for this app
]
```

> `Do Not Touch the Base file within the controller directory. It should only be inherited from.`

# Commit Standards

## Branches

- **dev** -> pr this branch for everything `backend` related
- **main** -> **dont touch** this branch, this is what is running in production.

## Contributions

Prompt is open to contributions, but I recommend creating an issue or replying in a comment to let us know what you are working on first that way we don't overwrite each other.

## Contribution Guidelines

1. Clone the repo `git clone https://github.com/hslcreators/prompt-be`.
2. Open your terminal & set the origin branch: `git remote add origin https://github.com/hslcreators/prompt-be.web.git`
3. Pull origin `git pull origin dev`
4. Create a new branch for the task you were assigned to, eg : `git checkout -b feat-file-parser`
5. After making changes, do `git add .`
6. Commit your changes with a descriptive commit message : `git commit -m "your commit message"`.
7. To make sure there are no conflicts, run `git pull upstream dev`.
8. Push changes to your new branch, run `git push -u origin feat-file-parser`.
9. Create a pull request to the `dev` branch not `main`.
10. Ensure to describe your pull request.
11. > If you've added code that should be tested, add some test examples.

### _Commit CheatSheet_

| Type     |                          | Description                                                                                                 |
| -------- | ------------------------ | ----------------------------------------------------------------------------------------------------------- |
| feat     | Features                 | A new feature                                                                                               |
| fix      | Bug Fixes                | A bug fix                                                                                                   |
| docs     | Documentation            | Documentation only changes                                                                                  |
| style    | Styles                   | Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)      |
| refactor | Code Refactoring         | A code change that neither fixes a bug nor adds a feature                                                   |
| perf     | Performance Improvements | A code change that improves performance                                                                     |
| test     | Tests                    | Adding missing tests or correcting existing tests                                                           |
| build    | Builds                   | Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)         |
| ci       | Continuous Integrations  | Changes to our CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs) |
| chore    | Chores                   | Other changes that don't modify backend, frontend or test files                                             |
| revert   | Reverts                  | Reverts a previous commit                                                                                   |

> _Sample Commit Messages_

- `chore: Updated README file` := `chore` is used because the commit didn't make any changes to the backend, frontend or test folders in any way.
- `feat: Added plugin info endpoints` := `feat` is used here because the feature was non-existent before the commit.
