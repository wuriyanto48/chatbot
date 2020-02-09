### Chatbot Core

Requirements:

- Python 3.7 or Higher
- Virtualenv

#### Getting started

Install virtualenv
```shell
$ pip install virtualenv 
```

Create virtualenv
```shell
$ virtualenv env -p python3 --no-site-packages
```

Activate virtualenv
```shell
$ source env/bin/activate
```

Install requirements 
```shell
$ pip install -r requirements.txt
```

#### Run Trainer

```shell
$ ./train_bot.py
```

#### Run Bot as CLI App

```shell
$ ./cli_bot.py
```

#### Run Bot as Microservice

```shell
$ ./app.py
```

#
Wuriyanto 2020