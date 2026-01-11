#docker --context homeserver compose --env-file .env.homeserver run --rm -it utils_declaration --build
docker --context homeserver compose --env-file .env.homeserver build
docker --context homeserver compose --env-file .env.homeserver up -d