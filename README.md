# About

## What is hostloc-login

A Python script for logging into Hostloc daily and visiting other users to earn points.

## How to use

- According to your account information, modify the settings in `config.yml`.
- Run ```docker-compose up -d``` to start the srcipt. 

## Two examles of Config.yml

#### No login question

```
username: 'your name'
passwd: 'your password'
login_time: '08:00'
```
#### Has login question

Assume you set the second question

```
username: 'your name'
passwd: 'your password'
login_time: '08:00'
question_id: 2
answer: 'your answer'
```