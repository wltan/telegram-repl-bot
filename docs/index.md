# Devpost

## Inspiration

The modules CS1010 and its variants are notorious for being some of the most difficult and arduous modules in NUS. We wanted to create a tool to aid students in those modules in their learning. At the same time we envision said tool to be convenient, accessible and easy to use. A telegram bot is implemented because of its widespread usage across the campus and its fulfilling the above characteristics. 

We foresee much potential in its usage. It is undoubtly useful for students to quickly check the correctness of their codes. It can also be used as a teaching tool in the classroom setting. 

## What it does

The bot has two modes: REPL mode and batch mode.

In REPL (Read-Evaluate-Print-Loop) mode, the user can input single expressions which will be piecewise evaluated immediately. It provides an interactive sandbox programming environment which is most useful in testing small chunks of code. 

In batch mode, the user can upload a file in one of the following file types (.txt, .c, .cpp, .java, .py) which the bot will compile in the corresponding language. 

The bot currently supports four languages: C, Java, Python and Source *(a subset of JavaScript that is predominantly used in SourceAcademy)*. These are the four languages used in the modules CS1010 and its variants. 

## How we built it

The bot is created using the official bot creator [BotFather](https://t.me/BotFather). At the front end, the bot is built using Python 3.8.0. At the back end, Docker SDK is used as an intermediate platform to handle the input and access an existing REPL or compiler to produce the ouput. Microsoft Azure's Container Registry and Web App for Containers are used to ...

## Challenges we ran into

Initial unfamiliarity with creation of Telegram Bots and usage of Docker SDK and Microsoft Azure services, which we had to pick up and use immediately within the span of 24 hours. 

Issue with credentials...

*THE FOLLOWING PARAGRAPH MAY BE OMITTED FROM THE FINAL DEVPOST*

There were a few issues with the Python REPL. Indentation is part of the syntax of Python, but it is impossible to input indentation (using tab characters) into the bot chat. At this stage, this issue has not yet been resolved yet (?) but a possible solution is to use "\t" literals in the raw message which then is converted into tab characters. 

## Accomplishments that we're proud of

Successfull creation and building a Telegram Bot using Python. 

Successful implementation of Docker SDK and Microsoft Azure's Container Registry and Web App for Containers. 

## What we learned

How to create a Telegram Bot

How to use Docker SDK and Microsoft Azure's Container Registry and Web App for Containers

## What's next for Telegram REPL Bot

Addition of other programming languages 