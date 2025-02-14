# arraydb-postgre-performance-test
This repo runs various operations both for Tiledb and PostgreSQL db in isolated docker containers. To obtain performance differences on array data with different DBMSs

#install docker
sudo snap install docker

#build and run containers
sudo docker-compose up --build

#possible issue
if in the host machine there is postgresystem already running ports that are necessary might be exposed make sure to stop running postgre with
sudo systemctl stop postgresql

make sure that ports 5432 and 5433 are not already exposed in the host machine