# PolyBotConversation

PolyBotConversation is an experimental web application that allows you to have group chat conversations with humans and multiple LLM-powered chatbots with individualized "personalities."

For additional background, have a look at my blog post ["PolyBotConversation – An Experiment with LLM Group Chats"](https://kleiber.me/blog/2024/10/06/PolyBotConversation-llm-group-chat-experiment/).

## Important Notes

PolyBotConversation is purely experimental software and *not* designed for production. Most importantly, there are severe security and privacy implications. For example, conversations are not protected, and all users can see all conversations. Furthermore, due to the fact that "core memories" are, by default, generated for all conversations and bots, information will be retained after the deletion of chats.

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

`isort` and `ruff` are used for linting and formatting. I don't particularly like PEP-8's maximum line length, so ...

```bash
isort .
ruff check
ruff format --line-length 200
```
