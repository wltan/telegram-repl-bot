# Telegram REPL Bot

A telegram bot to facilitate programming on the go. The bot can be found [here](https://t.me/the_REPL_bot).

## Team

Created as part of [Hack and Roll 2020](https://hacknroll2020.devpost.com/).

* Tan Wei Liang
* Yong Ping
* Ian Yong Yew Chuang

## Features

#### REPL (Read-Eval-Print-Loop)

A Read-Eval-Print-Loop (REPL), also termed a language shell, is an interactive environment which takes the user's inputs, evaluates them, and returns the result to the user. As of now, the bot supports the following REPLs:

* Python interpreter (Python)
* JShell (Java)
* Interactive GCC (C)
* Source REPL ([Source](https://github.com/source-academy/js-slang))

#### Batch Jobs

The bot also supports the processing of source files. These are the supported languages as of now:

* Python
* Java
* C
* C++

## Background

The modules CS1010 and its variants are notorious for being some of the most difficult and arduous modules in NUS. We wanted to create a tool to aid students in those modules in their learning. At the same time we envision said tool to be convenient, accessible and easy to use. A telegram bot is implemented because of its widespread usage across the campus and its fulfilling the above properties. 

We foresee much potential in the REPL bot's usage. It is undoubtedly useful for students to quickly check the correctness of their codes. It can also be used as a teaching tool in the classroom setting. 

## Getting Started

### Prerequisites

* Python 3.8.0
* pip3
* Docker

```
$sudo apt-get install python3.8
$sudo apt-get install python3-pip
$sudo apt-get install docker.io
```

### Installing

Clone the repository and `cd` into it.
```
$git clone https://github.com/wltan/telegram-repl-bot
$cd telegram-repl-bot
```
To set up the necessary Docker images, run `setup.sh`.
```
$sudo ./setup.sh
```
Finally, to run the telegram bot, run `launch.sh`.
```
$sudo ./launch.sh
```