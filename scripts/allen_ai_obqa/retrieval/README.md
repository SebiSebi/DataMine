About PyLucene
----------------

`PyLucene` is very painful to install. We recommend to run the code in
this [docker container](`https://hub.docker.com/r/coady/pylucene/) that
comes up with `PyLucene` already installed. The `Docker` image is part
of [Lupyne](https://github.com/coady/lupyne) and is actively maintained.

Run the docker with (to get a terminal):
```
docker run -it --entrypoint=/bin/bash coady/pylucene
```

Run the docker with a shared directory (example):
```
docker run -v ~/GitHub/DataMine/scripts/allen_ai_obqa/retrieval/token_based:/root/token_based -it --entrypoint=/bin/bash coady/pylucene
```
