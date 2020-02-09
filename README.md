### Chatbot Core

Machine Learning Deep Neural Network Chatbot 

[<img src="https://upload.wikimedia.org/wikipedia/commons/4/46/Colored_neural_network.svg" width="300">](https://github.com/wuriyanto48/chatbot)
<br/><br/>

Requirements:

- Python 3.7 or Higher
- Virtualenv
- Nodejs

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

Run `Bot` first

```shell
$ ./app.py
```

Then run  `chat-server`
```shell
$ cd chat-server
$ npm start
```

#
Wuriyanto 2020