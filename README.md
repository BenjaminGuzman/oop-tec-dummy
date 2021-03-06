# oop-tec-dummy

## Backend requirements
`GNU/Linux`  (specifically the *Fedora 31*distro) is the only operative system supported, maybe other operative systems can run the backend (cause it's written in node.js) but no manual is provided for that cases.

It's assumed you've Node.js installed and MariaDB or MySQL also installed (could be in different servers). There is no containerization because of the time (and well, it's worthless doing, it's just a dummy app)

(Tip: a `sh` script inside `backend/database_creation/load.sh` has been created to make simple the creation of the database, also, no backup file was created)

Also there is a small documentation of the database in `db_dictionary.pdf` and the figure shown below is the relational diagram

![Relational diagram for the database](OOPTecDummy-relational-diagram.png)

### Create database schemas
The schemas declaration are inside `backend/database_creation/ddl.sql`

### Create database procedures
The procedures are inside `backend/database_creation/procedures.sql`

### Create database triggers
The triggers are inside `backend/database_creation/triggers.sql`

### Create database users
The users are inside `backend/database_creation/users.sql`

### Insert data
The insertions "queries" are inside `backend/database_creation/inserts.sql`

**Note**: The original "database" is `backend/database_creation/videoDB.csv`, while cleaning the database and checking for not null values, some data were omitted so the insertions could not have all the info `videoDB.csv` has (check below if you wanna know what I mean).

If you wanna know how those insertion were created open jupyter lab or notebook and read `backend/database_creation/video_cleaning_dump.ipynb`

### Install node requirements
 Cypress hill, just install `npm run install`
 
### Run the server
Just with `npm run start` (it's also worth reading `package.json` for more options)

## Fronted requirements
Unlike the backend, you can run it where you like most, win, linux or macos, just install the dependencies inside `requirements.txt`

`pip install -r requirements.txt`
 


