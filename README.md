# PolyBotConversation

PolyBotConversation is an experimental web application that allows you to have group chat conversations with humans and multiple LLM-powered chatbots with individualized "personalities."

For additional background, have a look at my blog post ["PolyBotConversation – An Experiment with LLM Group Chats"](https://kleiber.me/blog/2024/10/06/PolyBotConversation-llm-group-chat-experiment/).

## Important Notes

PolyBotConversation is purely experimental software and *not* designed for production. Most importantly, there are severe security and privacy implications. For example, conversations are not protected, and all users can see all conversations. Furthermore, due to the fact that "core memories" are, by default, generated for all conversations and bots, information will be retained after the deletion of chats.

## Key Features

* Multi-user (group) chats with both humans and LLM-powered chatbots with individual "personalities"
* @mention and conversation-based triggers for chatbot responses
* Automatically establishing so-called "core memories" that shape a bot's "personality" across conversation
* Automatically naming conversations (LLM-powered)

## Setup

### Python Environment

* Create a Python environment (e.g., using `venv`, `conda`, `poetry` or `uv`).
* Install the dependencies in `requiements.txt`.

### OpenAI Key

You will need to set your OpenAI Key (if you are using OpenAI) as an environmental variable.

Windows

```cmd
set OPENAI_API_KEY=sk-...
```

Linux

```bash
export OPENAI_API_KEY=sk...
```

### Configuration and Start (Development Environment)

First, have a look at both the `settings.py` and the `prompt_templates.py`. Here, you can make changes to how the system functions.

Then, run the setup script:

```bash
python manage.py setup
```

Now you can run the development server:

```bash
python manage.py runserver
```

In a different terminal, run the following in order to start the task manager:

```bash
python manage.py qcluster
```

## Development

Feel free to tinker around with this and make suggestions! PRs are absolutely welcome!

### Notes for Developers

Here are a few notes about the design of the application that hopefully will help you to get started!

* The application is based on [Django](https://www.djangoproject.com/) and uses [htmx](https://htmx.org/) for the chat itself. [Bootstrap](https://getbootstrap.com/) is used as a CSS framework. Both htmx and bootstrap are shipped here in the `static/js` folder. Of course, they don't fall under the same license as this project.
* The application makes heavy use of `django-q2`. `tasks.py` holds the key tasks that are being performed by the task manager. Some tasks are being issued on the fly, e.g., the generation of core memories in `views.py`.
* There is a simple "prompt library" in `prompt_templates.py`. These are populated using `.format()` before usage with the API.
* `bot.py` contains functions for generating messages and replying in conversations. `llm.py` contains functions for interacting with the OpenAI (compatible) endpoint and other LLM tasks.
* The general flow looks like this: A task (`tasks.py`) runs triggers from `triggers.py`. These use functions from `bot.py` (which uses `llm.py`) in order to generate new message.

### Linting and Formatting

`isort` and `ruff` are used for linting and formatting. I don't particularly like PEP-8's maximum line length, so ...

```bash
isort .
ruff check
ruff format --line-length 200
```
