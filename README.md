<p align="center">


![Shigoto Logo](https://i.imgur.com/MK7NlZI.png)

<h2 align="center">Shigoto</h2>


[![Build Status](https://travis-ci.com/SimeonAleksov/shigoto.svg?token=BRFSrDpxsFuTrxmdtyPy&branch=master)](https://travis-ci.com/SimeonAleksov/shigoto_q)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
[![CodeFactor](https://www.codefactor.io/repository/github/simeonaleksov/shigoto_q/badge)](https://www.codefactor.io/repository/github/simeonaleksov/shigoto_q)
<a href="https://shigoto.com/api-docs/?badge=stable"><img alt="Documentation Status" src="https://readthedocs.org/projects/black/badge/?version=stable"></a>
</p>

## Demo

![Demo gif](https://media2.giphy.com/media/SzKqAr6u2U6RdGFlL5/giphy.gif?cid=790b76117599548aca1f9e1325ce29870be94a01dfd095e6&rid=giphy.gif)

## About
A [Django](https://www.djangoproject.com/) project for easy cron job, task planning and monitoring.

## Features

- Django-based backend

    - [Django](https://www.djangoproject.com/)
    - Separate settings for different environments (local/production/testing)
    - Python 3.6 or later
    - Accessible from port `8000` for local development
    - [DRF](https://www.django-rest-framework.org/) REST API
    
    
- Frontend app with JavaScript (ES2015), React and Sass
    - Latest TypeScript features from [ES2015](https://babeljs.io/docs/learn-es2015/) and beyond, transpiled with
    - [React](https://facebook.github.io/react/) for fast modular user interfaces
    - [Sass](http://sass-lang.com/), [PostCSS](http://postcss.org/)
    - [Tailwind CSS](https://tailwindcss.com/)
    - Accessible from port `3000` for local development

- Batteries

    - Docker / Docker Compose integration
    - Linting of Python, JavaScript and Sass code with [Prospector](http://prospector.landscape.io/),
      [ESLint](http://eslint.org/) and [stylelint](https://stylelint.io/)
    - Automated code-formatting using [black](https://black.readthedocs.io) and [prettier](https://prettier.io)
    - [py.test](http://pytest.org/) and [coverage](https://coverage.readthedocs.io/) integration
    - Out-of-the-box configuration for gunicorn, traefik
    - Includes [PyCharm](https://www.jetbrains.com/pycharm/) project config



- [React](https://facebook.github.io/react/), for building interactive UIs
- [Celery](http://www.celeryproject.org/), for background worker tasks
- [WhiteNoise](http://whitenoise.evans.io/en/stable/) for serving static files in production.

For continuous integration, a [TravisCI](https://travis-ci.com/) configuration `.travis.yml` is included.



## API Reference

#### Get all users

```http
  /auth/users/
```

| HTTP Method | Authorization     | Response                |
| :-------- | :------- | :------------------------- |
| `GET` | **Bearer Token** | List of users |
| `POST` | None | Create a user |

`POST` data:
```json
{
    "email": "",
    "username": "",
    "first_name": "",
    "last_name": "",
    "company": "",
    "password": ""
}
```

#### Get current user

```http
  /auth/users/me/
```

| HTTP Method | Authorization     | Response                       |
| :-------- | :------- | :-------------------------------- |
| `GET`      | **Bearer Token** | Current user data |



```http
  /api/v1/products/
```

| HTTP Method | Authorization     | Response                       |
| :-------- | :------- | :-------------------------------- |
| `GET`      | None | List of available products and their price|


```http
  /api/v1/cron/
```

| HTTP Method | Authorization     | Response                       |
| :-------- | :------- | :-------------------------------- |
| `GET`      | **Bearer Token** | List of user created crontabs|
| `POST`      | **Bearer Token** | Create a crontab for the authorized user.|

`POST` body:

```json
    {
        "minute": "*",
        "hour": "*",
        "day_of_month": "*",
        "month_of_year": "*",
        "day_of_week": "*"
    }
```


## Installation

- [ ] Clone this repository
- [ ] Install [python](https://www.python.org/)
- [ ] Install [docker](https://docs.docker.com/docker-for-windows/install/) and [docker-compose](https://docs.docker.com/compose/install/) follow the instructions for you OS.
- [ ] Install [node js and npm](https://nodejs.org/en/download/)
- [ ] After installing navigate to the project directory and install the node packages
```shell script
$ cd shigoto_q/frontend/
$ npm i
```
######  Build the front end with
```shell script
$ npm run build
```
###### After you build the frontend go back to the root and build the containers
```shell script
$ cd ..
$ docker-compose -f local.yml build 
``` 
###### After the containers are built run 
```shell script
$ docker-compose -f local.yml up
```

## Running Tests

To run tests, run the following command

```bash
  docker-compose -f local.yml run django pytest
```
