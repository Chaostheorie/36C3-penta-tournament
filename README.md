# 36C3-penta-tournament

36C3 Penta Tournament special edition by Cobalt

## Installation

You will need a working python 3.5+ installation and pip. First you need to clone the repository via git or download it via your browser and unzip it.

For installing dependencies with pip use:

```bash
pip3 install -r requeriments.txt
```

Now you only need to start the local flask devolepement server with:

```bash
python3 main.py
```

It can happen that at the first startup, while the db is created, the instance may happen to crash or malfunction. Just restart and restart the `main.py` file.

Notes:

- For persistent tournament name usw. use preenv.json (`36C3-penta-tournament/preenv.json` See wiki for more <https://github.com/Penta-Game/36C3-penta-tournament/wiki/Preenv.json---Persistent-Tournament>)
