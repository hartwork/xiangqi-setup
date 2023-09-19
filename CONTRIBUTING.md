# Contributing to xiangqi-setup

**xiangqi-setup** is considered feature complete.
If you consider contributing a new feature, please [open a new issue](https://github.com/hartwork/xiangqi-setup/issues/) to discuss the feature and its suitability to **xiangqi-setup**, first. Thank you!


# Developing xiangqi-setup locally

In order to develop or debug **xiangqi-setup** locally, you could do:

```shell
cd "$(mktemp -d)"
git clone --depth 1 https://github.com/hartwork/xiangqi-setup  # or your clone's repo URI
cd xiangqi-setup/
python3 -m venv venv
source venv/bin/activate
pip3 install -e '.[tests]'

xiangqi-setup --help             # method a, uses venv/bin/xiangqi-setup
python3 -m xiangqi_setup --help  # method b, uses __main__.py
```
