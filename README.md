<p align="center">

<img src="https://i.imgur.com/bkB9LUA.png" width="320" alt="Shigoto Logo" />

</p>
<h2 align="center">Shigoto</h2>

<p align="center">
    <a href="https://github.com/Shigoto-Q/shigoto/actions/workflows/deployment.yml"><img alt="Continuous Deploymen" src="https://github.com/Shigoto-Q/shigoto/actions/workflows/deployment.yml/badge.svg"></a>
    <a href="https://github.com/Shigoto-Q/shigoto_q/actions/workflows/ci.yml"><img alt="ci" src="https://github.com/Shigoto-Q/shigoto_q/actions/workflows/ci.yml/badge.svg?branch=master"></a>
    <a href=""><img alt="madewith" src="https://img.shields.io/badge/Made%20with-Python-1f425f.svg"></a>
    <a href=""><img alt="license" src="https://img.shields.io/badge/License-GPL%20v3-yellow.svg"></a>
    <a href="https://github.com/psf/black"><img alt="format" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
    <a href="><img alt="codefactor" src="https://www.codefactor.io/repository/github/shigoto-q/shigoto_q/badge"></a>
    <a href="https://shigoto.com/api-docs/?badge=stable"><img alt="Documentation Status" src="https://readthedocs.org/projects/black/badge/?version=stable"></a>
    <a href="https://github.com/PyCQA/bandit"><img alt="Bandit check" src="https://img.shields.io/badge/security-bandit-yellow.svg"></a>
</p>
<p align="center">
<img src="https://i.imgur.com/58GNCsy.gif" width="320" alt="Shigoto Logo" />
 </p>


## About
A [Django](https://www.djangoproject.com/) project for easy cron job, task planning and monitoring.

## Features

- Backend technologies 

    - [Django](https://www.djangoproject.com/)
    - Separate settings for different environments (local/production/testing)
    - Python 3.6 or later
    - Accessible from port `8000` for local development
    - [DRF](https://www.django-rest-framework.org/) REST API


- Batteries
    - Docker / Docker Compose integration
    - Automated code-formatting using [black](https://black.readthedocs.io) and [prettier](https://prettier.io)
    - [py.test](http://pytest.org/) and [coverage](https://coverage.readthedocs.io/) integration
    - Out-of-the-box configuration for gunicorn, traefik
    - Includes [PyCharm](https://www.jetbrains.com/pycharm/) project config



- [Celery](http://www.celeryproject.org/), for background worker tasks
- [WhiteNoise](http://whitenoise.evans.io/en/stable/) for serving static files in production.



## Installation

- [X] Clone this repository
- [X] Install [python](https://www.python.org/)
- [X] Install [docker](https://docs.docker.com/docker-for-windows/install/) and [docker-compose](https://docs.docker.com/compose/install/) follow the instructions for you OS.
- [X] After installing navigate to the project directory and install the node packages

Running the backend locally is pretty simple, all you have to do is clone the repository and run:
```shell
$ docker-compose up
```

The server will be accessible at port `8000`. If you want to have the frontend as well, follow the frontend repository for instructions.

##### Running ELK Stack
You can run ELK stack in docker swarm
```sh
$ docker swarm init
$ docker stack deploy -c docker-elk-stack.yml elk
$ docker stack services elk
```
Go to `localhost:5601` and log in.
#### Running ELK stack as part of docker-compose
```sh
$ COMPOSE_FILE=docker-compose.yml:docker-compose-kibana-optional.yml
$ docker-compose up
```

### Running Grafana and influxDB locally
```shell
$ docker-compose-f docker-compose-grafana-chronograf.yml
```

## Running everything together
```shell
$ export COMPOSE_FILE=docker-compose.yml:docker-compose-kibana-optional.yml:docker-compose-grafana-chronograf.yml
```

## Sending e-emails

Locally MailHog is configured, meaning every e-mail is rerouted to `localhost:18000`.
##### Generating new e-mail tempates
For e-mails we use mjml framework. Simply install the package:
```shell
$ npm install
```
In `shigoto/emails/templates/src/...` create a directory or if it already exists for that namespace, create `.mjml` file.

Make sure to import the `header.mjml` and `footer.mjml` to the e-mail template.

After you've created the e-mail template, run:
```shell
$ mjml -m `emails/templates/src/path/to/template.mjml` -o `emails/templates/generated/path/to/template.html`
```

After creating the template, add your template in `shigoto.emails.constants.EmailTypes`.

Make sure to also add a title and a description for the template.

Next,in docker container run:
```shell
$ docker-compose exec django bash python manage.py generate_email_templates
```
This will generate `EmailTemplate` instance, and last but not least, send the e-mail:
```python
from shigoto_q.emails import services
from shigoto_q.emails.constants import EmailTypes, EmailPriority

services.send_email(
  template_name=EmailTypes.USER_SUBSCRIPTION, 
  priority=EmailPriority.NOW, 
  override_email='simeon.aleksov@shigo.to', 
  context={},
)
```


## Running Tests

To run tests, run the following command

```bash
  docker-compose -f local.yml run django pytest
```

## Internal REST Abstract Views


We provide a `ResourceView` and `ResourceListView` as an easier way to extend our app without repeating ourselves.

Both of the classes inherit from `BaseView` which inherits from `rest_framework.views.APIView`.

Class variables:

- serializer_dump_class: serializer class that is used to parse response
- serializer_load_class: serializer to parse request params
- exception_serializer: default serializer for 400 error
- owner_check: check whether the owner of the request matches the resource owner
- permission_classes = [IsAuthenticated]

With these views you can use load and dump serializers.

### ResourceListView

An example making GET request to fetch multiple objects:

```python
class DockerImageListView(ResourceListView):
serializer_dump_class = serializers.DockerImageSerializer
serializer_load_class = serializers.DockerImageSerializer
owner_check = True

    def fetch(self, filters, pagination):
        return fetch_and_paginate(
            func=docker_services.list_docker_images,
            filters=filters,
            pagination=pagination,
            serializer_func=DockerImage.from_dict,
            is_serializer_dataclass=True,
        )
```

`fetch()` is a callback function for `GET` requests.

The filters and pagination validation and parsing is handled by the Abstract class.

### ResourceView

```python
class DockerImageCreateView(ResourceView):
    serializer_dump_class = UserImageCreateDumpSerializer
    serializer_load_class = UserImageCreateLoadSerializer
    owner_check = True

    def execute(self, data):
        return task_services.create_docker_image(data=data)
```

`execute()` is a callback for `POST` requests.

```python
class DockerImageCreateView(ResourceView):
    serializer_dump_class = DockerViewSerializer
    serializer_load_class = DockerViewSerializer
    owner_check = True

    def find_one(self, data):
        return task_services.get_docker_image(data=data)
```

`find_one()` is a callback for `GET` requests.


## Custom camel case serializer

We have a custom serializer, keep snake_case in python, and camelCase in our javascript.
Usage:
```python
class DockerImageDeleteSerializer(CamelCaseSerializer):
    some_field = serializers.IntegerField()
```

When dumping it produces `someField`, and vice versa, when loading `some_field`.


### Fetching and paginating objects

If you need to return a lot of objects, use `fetch_and_paginate()`

```python
fetch_and_paginate:
    Args:
        func: typing.Callable,
        filters: dict,
        pagination: Page,
        serializer_func: typing.Union[dataclass, typing.Callable],
        is_serializer_dataclass=False,
```
