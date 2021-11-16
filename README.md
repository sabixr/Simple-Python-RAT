[![Stargazers][stars-shield]][stars-url]

## About

Windows Remote Access Tool with support for uploads, downloads and fun commands.

### Built With

* [Python 3](https://www.python.org/)
* [Colorama](https://github.com/tartley/colorama)

### Prerequisites

* colorama
  ```sh
  pip install colorama
  ```

### Setup

1. Clone the repo
   ```sh
   git clone https://github.com/k200-dev/Windows-Python-RAT/
   ```
2. Fill in the values in `client.py` and `server.py`
   ```python
   ratClient = RATConnector("ENTER IP ADDRESS", ENTER PORT)
   activeServer = Server("ENTER IP ADDRESS", ENTER PORT)
   ```

## Usage

Run `server.py` on your local machine and `client.py` on the target machine.
Run `ratHelp` in the terminal to see a list of commands

![Image of the RAT server](https://files.k200.site/github-Windows-Python-RAT-example.png)

[stars-shield]: https://img.shields.io/github/stars/github_username/repo_name.svg?style=for-the-badge
[stars-url]: https://github.com/k200-dev/Windows-Python-RAT/stargazers
