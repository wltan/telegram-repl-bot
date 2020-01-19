# Devpost

## Inspiration

CS1010 and its variants are notorious for being some of the most difficult and arduous modules in NUS. We wanted to create a tool to aid students in their learning, and at the same time is easy to setup and use. A telegram bot is used because of its convenience and accessibility. 

## What it does

The bot has two modes: REPL mode and batch mode.

In REPL (Read-Evaluate-Print-Loop) mode, the user can input single expressions which will be immediately evaluates each expression. It provides an interactive programming environment which is useful in testing small chunks of code. 

In batch mode, the user can upload a file of one of the four file types (.c, .cpp, .java, .py) which the bot will compile in the corresponding language. 

The bot currently supports four languages: C, Java, Python and Source *(a subset of JavaScript that is predominantly used in SourceAcademy)*. These are the four languages that are used in the modules CS1010 and its variants. 

## How we built it

On the front end, the bot was built using Python 3.8.0. On the back end, Docker SDK is used as an intermediate platform to handle the input and access an existing REPL or compiler to produce the ouput. Microsoft Azure's Container Registry and Web App for Containers were used to...

## Challenges we ran into

A fuckload

## Accomplishments that we're proud of

Successfully creating a useful tool which our peers could benefit from.

## What we learned

How to use Docker SDK
How to use Microsoft Azure's Container Registry and Web App for Containers
...

## What's next for Telegram REPL Bot

