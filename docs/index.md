# Devpost

## Inspiration

The modules CS1010 and its variants are notorious for being some of the most difficult and arduous modules in NUS. We wanted to create a tool to aid students in those modules in their learning. At the same time we envision said tool to be convenient, accessible and easy to use. A telegram bot is implemented because of its widespread usage across the campus and its fulfilling the above properties. 

We foresee much potential in the REPL bot's usage. It is undoubtedly useful for students to quickly check the correctness of their codes. It can also be used as a teaching tool in the classroom setting. 

## What it does

The bot has two modes: REPL mode and batch mode.

In REPL (Read-Evaluate-Print-Loop) mode, the user can input single expressions which will be piecewise evaluated immediately. It provides an interactive sandbox programming environment which is most useful in testing small chunks of code. 

In batch mode, the user can upload a file in one of the following file types (.txt, .c, .cpp, .java, .py) which the bot will compile in the corresponding language. 

The bot currently supports five languages: C, C++, Java, Python and Source *(a subset of JavaScript that is predominantly used in SourceAcademy, the main programming platform of CS1101S)*. These languages are used in the modules CS1010 and its variants. 

## How we built it

The bot is created using the official bot creator [BotFather](https://t.me/BotFather). At the front end, the bot is built using Python 3.8.0. At the back end, Docker SDK is used as an intermediate platform in the form of containers to handle the input and access an existing REPL or compiler to produce the ouput. Microsoft Azure's Virtual Machine service, Container Registry and Web App for Containers are used to manage the container images. 

## Challenges we ran into

Initial unfamiliarity with the creation of Telegram Bots and usage of Docker SDK and Microsoft Azure services, which we had to pick up and implement immediately within the span of 24 hours. 

There was a major issue with the Python REPL. Indentation is part of the syntax of Python, but it is impossible to input indentation into the bot chat because Telegram automatically removes leading white spaces. The  solution implemented uses "\t" literals in the raw message which then is converted into tab characters. 

## Accomplishments that we're proud of

Successfull creation and building a Telegram Bot using Python. 

Successful implementation of Docker SDK and Microsoft Azure's Container Registry and Web App for Containers. 

## What we learned

How to create a Telegram Bot

How to use Docker SDK and Microsoft Azure's Virtual Machines, Container Registry and Web App for Containers

## What's next for Telegram REPL Bot

Addition of other programming languages