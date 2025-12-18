# GDPR Search

This is the repository of the https://gdpr.algolia.com/ website.

## Getting started

1. Clone this repository `git clone git@github.com:algolia/gdpr-search.git`
2. Install the needed tools:
    * [`pipenv`](https://docs.pipenv.org/#install-pipenv-today): `brew install pipenv`
    * [`yarn`](https://yarnpkg.com/lang/en/docs/install/): `brew install yarn`
    * [`psql`](https://www.postgresql.org/): `brew install postgresql`
3. Install the dependencies:
    * Python: `pipenv install --python 3.9`
    * JS: `yarn install`
4. Setup the database and the env variables:
    * `createdb gdprsearch`
    * Copy the `.env.template` and edit / `source` it.
5. Start the project:
    * Activate the python env: `pipenv shell`
    * Populate the database (Ask for a dump to the team)
    * Start the Django `django-admin runserver`
    * Start the webpack watch: `yarn run watch`


## Repo Structure
* `gdpr/crawler`: contains the `Scrapy` spiders populating the database
* `gdpr/gdpr`: contains the Django app
* `gdpr/static/js`: contains the `Search` part of the website, in React.

## Deployment
Deployed manually to Heroku