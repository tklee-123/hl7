# config.py
from urllib.parse import quote_plus

DB_TYPE = "mongo"
# mongodb+srv://caothihoaithuongt66:LHWvnvPVQrhsdvDG@cluster0.8vl7mdu.mongodb.net/hl7_db?retryWrites=true&w=majority&appName=Cluster0
# Connection details
CONNECT = {
    "mongo": {
        "URL": "cluster0.8vl7mdu.mongodb.net",
        "DATABASE": "hl7_db",
        "USER": "caothihoaithuongt66",
        "PASSWORD": "LHWvnvPVQrhsdvDG",
    },
    "mysql": {
        "HOST": "localhost",
        "DATABASE": "mydb",
        "USER": "root",
        "PASSWORD": "password",
    },
    "sqlserver": {
        "HOST": "localhost",
        "DATABASE": "mydb",
        "USER": "sa",
        "PASSWORD": "password",
    },
    "postgresql": {
        "HOST": "localhost",
        "DATABASE": "mydb",
        "USER": "postgres",
        "PASSWORD": "password",
    },
}

# URL encode the username and password for MongoDB
username = quote_plus(CONNECT[DB_TYPE]["USER"])
password = quote_plus(CONNECT[DB_TYPE]["PASSWORD"])
CONNECT[DB_TYPE][
    "URL"
] = f"mongodb+srv://{username}:{password}@{CONNECT[DB_TYPE]['URL']}"

SCHEMA = {
    "HL7": "hl7_messages"
}
