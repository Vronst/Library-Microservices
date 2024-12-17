# Library - by Adam and Mateusz

## Instaltion
Project is created in docker (this way it is easier to run it without much configuration of python and c#) so to run it you will only need [docker/docker-compose](https://docs.docker.com/desktop/setup/install/windows-install/) and a bit configuration.
After installing docker, you have to create .env file in the folder with docker-compose.yml
```cmd
echo > .env
```
Fill it with variables so it will look like:
```env
USER_DB = 'your_db_user'
PASSWORD_DB = 'password_for_db'
POSTGRES_DB = 'name_of_db'
SECRET_KEY = 'your_very_secret_key'
UI_PORT = port_number
OUR_API_PORT = port_number
SERVER = 'db:5432'  # default port for db, the 'db:' part must stay
```

Now run 
```bash
docker compose up --build
```
to build containers. If everything works you now only have to populate database for pro_sec.
Firstly copy backup file to container:
```bash
docker cp BD_semestr_V.bak `conteiner_ID`:var/backups
```
For that simply enter the terminal for your container
```bash
docker exec -it <id of your conteiner> /bin/bash
```
and inside type:
```bash
cd /opt/mssql-tools18/bin & ./sqlcmd -S localhost -U sa -P 'Mateusz12345' -C
```
This shouold log you into mysql database. Now few simple commends and you are done!
```sql
RESTORE DATABASE BD_semestr_V
FROM DISK = '/var/backups/BD_semestr_V.bak'
WITH MOVE 'BD_semestr_V' TO '/var/opt/mssql/data/BD_semestr_V.mdf',
     MOVE 'BD_semestr_V_log' TO '/var/opt/mssql/data/BD_semestr_V_log.ldf';
GO
```
Now restart the container with command:
```bash
docker compose up
```
### Remember not to use --build flag, it will clear the pro_sec database and you will have to redo these steps to fill it again


If you want to use this project without docker for some reason, visit README in following folders: ui_backend, dockerTest002.

There should be instructions how to set up both python and c#.