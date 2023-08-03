from os import environ

name = environ.get('name')
if name:
    name = name.lower()
else:
    name = 'sqlite'

driver = environ.get('driver')
if driver:
    driver = driver.lower()

database = environ.get('database')
if not database:
    print('using default database')
    database = 'log_db'

if environ.get('windowsAuth') == None:
    username = environ.get('username')
    password = environ.get('password')

port = environ.get('port')
if port is None:
    print('using default ports, please override where required')
    if name in ("postgresql",):
        port = 5432
    elif name in ('mysql', ):
        port = 3306
    elif name in ('oracle', ):
        port = 1521
    elif name in ('microsoft sql server', 'mssql'):
        port = 1433

host = environ.get('host')

def create_connection_string():
    try:
        # dialect+driver://username:password@host:port/database
        connection_string = f'+{driver}://{username}:{password}@{host}:{port}/{database}'
    except NameError:
        print('trying principal token based login')
        #connection_string = f'://{host}/{database};'
        connection_string = f'://{host}/{database}?trusted_connection=yes'
        if driver:
            connection_string += f'&driver={driver}'
    #except Exception as er:
        #raise Exception(er)
    
    if name in ("postgresql",):
        return "postgresql" + connection_string

    elif name in ('mysql', ):
        return 'mysql' + connection_string

    elif name in ('oracle', ):
        return "oracle" + connection_string

    elif name in ('microsoft sql server', 'mssql'):
        return "mssql" + connection_string

    elif name in ("sqlite", 'sqlite3'):
        # sqlite://<nohostname>/<path>
        return f'sqlite:///{database}.sqlite3'
