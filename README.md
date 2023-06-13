# arm-duplisearcher-sqlite
duplisearcher with SQLite DB

привязка папки с конфигурационным файлом:
https://stackoverflow.com/questions/30652299/having-docker-access-external-files


если запускать из папки проекта:
source="$(pwd)"/data - папка на сервере
target=/app/data - папка внутри контейнера

running script:
sudo docker run -p 4005:8080 -d --restart unless-stopped --mount type=bind,source="$(pwd)"/data,target=/app/data -it expert-bot-dispatcher

В базе данных этого сервиса должны быть только ответы (ему ничего не надо знать про эталоны)

docker compose:
https://stackoverflow.com/questions/47699035/docker-docker-compose-restart-unless-stopped-loose-logs-in-console

https://stackoverflow.com/questions/40905761/how-do-i-mount-a-host-directory-as-a-volume-in-docker-compose