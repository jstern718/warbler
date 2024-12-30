import sqlite3

#Function for setting up warbler_db database.

try:
    db = sqlite3.connect('warbler_db')
    print('Connected to the SQLite database')
except:
    print('Error connecting to the SQLite database')

cursor = db.cursor()

cursor.execute('''
    CREATE TABLE customers (
        name TEXT PRIMARY KEY,
        customer_company TEXT,
        customer_identity TEXT,
        address_num TEXT,
        address_street TEXT,
        address_road_type TEXT,
        address_suite TEXT,
        address_city TEXT,
        address_state TEXT,
        address_zip TEXT,
        phone TEXT,
        password TEXT,
        email TEXT)
''')

customers = [
    ("adamapple", "acorp", "president", "1", "Main", "St.", "100", "Baltimore", "MD", "21201", "4108675309", "password1", "adam@acorp.com"),
    ("bobbaker", "bcorp", "president", "2", "Main", "St.", "200", "Baltimore", "MD", "21201", "4108675309", "password2", "bob@bcorp.com"),
    ("carlcake", "ccorp", "president", "3", "Main", "St.", "300", "Baltimore", "MD", "21201", "4108675309", "password3", "carl@ccorp.com")
]

cursor.executemany('''
    INSERT INTO customers (name, customer_company, customer_identity, address_num, address_street, address_road_type, address_suite, address_city, address_state, address_zip, phone, password, email)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', customers)

cursor.execute('''
    CREATE TABLE server_types (
        name TEXT PRIMARY KEY,
        price INTEGER)
''')

server_types = [
    ("Apache_Tomcat", 1100),
    ("IIS", 1200),
    ("Nginx", 1300),
    ("LiteSpeed", 1400)
]

cursor.executemany('''
    INSERT INTO server_types (name, price)
    VALUES (?, ?)
''', server_types)

cursor.execute('''
    CREATE TABLE resource_types (
        name TEXT PRIMARY KEY,
        price INTEGER)
''')

resource_types = [
    ("Number_of_Servers", 100),
    ("Memory_Usage", 50),
    ("Storage_Usage", 75),
    ("vCPUs", 250),
    ("Clustered_Servers", 500)
]

cursor.executemany('''
    INSERT INTO resource_types (name, price)
    VALUES (?, ?)
''', resource_types)

cursor.execute('''
    CREATE TABLE code_languages (
        language_name TEXT PRIMARY KEY)
''')

code_languages = [
    ("Java"),
    ("React.js"),
    ("Python"),
    ("Node.js"),
    ("C++"),
    ("C#")
]

cursor.executemany('''
    INSERT INTO code_languages (language_name)
    VALUES (?)
''', [(lang,) for lang in code_languages])
cursor.execute('''
    CREATE TABLE IF NOT EXISTS software_technologies (
        name TEXT PRIMARY KEY,
        price INTEGER
    )
''')

software_technologies = [
    ("Docker", 100),
    ("Elasticsearch", 200),
    ("Apache_Kafka", 300),
    ("Redis", 400),
    ("AI", 500)
]

cursor.executemany('''
    INSERT INTO software_technologies (name, price)
    VALUES (?, ?)
''', software_technologies)

cursor.execute('''
    CREATE TABLE IF NOT EXISTS servers_used (
        id INTEGER PRIMARY KEY,
        server_name TEXT,
        name TEXT,
        FOREIGN KEY(server_name) REFERENCES server_types(name),
        FOREIGN KEY(name) REFERENCES customers(name)
    )
''')

servers_used = [
    ("Apache_Tomcat", "adamapple"),
    ("IIS", "bobbaker"),
    ("Nginx", "carlcake")
]

cursor.executemany('''
    INSERT INTO servers_used (server_name, name)
    VALUES (?, ?)
''', servers_used)

cursor.execute('''
    CREATE TABLE IF NOT EXISTS resources_used (
        id INTEGER PRIMARY KEY,
        name TEXT,
        resource_name TEXT,
        resource_amount INTEGER,
        FOREIGN KEY(name) REFERENCES customers(name),
        FOREIGN KEY(resource_name) REFERENCES resource_types(name)
    )
''')

resources_used = [
    ("adamapple", "Number_of_Servers", 1),
    ("adamapple", "Memory_Usage", 100),
    ("adamapple", "Storage_Usage", 100),
    ("adamapple", "vCPUs", 1),
    ("adamapple", "Clustered_Servers", 0),
    ("bobbaker", "Number_of_Servers", 2),
    ("bobbaker", "Memory_Usage", 200),
    ("bobbaker", "Storage_Usage", 200),
    ("bobbaker", "vCPUs", 2),
    ("bobbaker", "Clustered_Servers", 1),
    ("carlcake", "Number_of_Servers", 3),
    ("carlcake", "Memory_Usage", 300),
    ("carlcake", "Storage_Usage", 300),
    ("carlcake", "vCPUs", 3),
    ("carlcake", "Clustered_Servers", 1)
]

cursor.executemany('''
    INSERT INTO resources_used (name, resource_name, resource_amount)
    VALUES (?, ?, ?)
''', resources_used)
cursor = db.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS technologies_used (
        id INTEGER PRIMARY KEY,
        name TEXT,
        technology_name TEXT,
        FOREIGN KEY(name) REFERENCES customers(name),
        FOREIGN KEY(technology_name) REFERENCES software_technologies(name)
    )
''')

technologies = [
    ("adamapple", "Docker"),
    ("adamapple", "Elasticsearch"),
    ("bobbaker", "Apache_Kafka"),
    ("bobbaker", "Redis"),
    ("carlcake", "AI")
]

cursor.executemany('''
    INSERT INTO technologies_used (name, technology_name)
    VALUES (?, ?)
''', technologies)

cursor.execute('''
    CREATE TABLE IF NOT EXISTS applications (
        application_name TEXT PRIMARY KEY,
        version_num TEXT,
        application_url TEXT,
        application_port TEXT,
        name TEXT,
        FOREIGN KEY(name) REFERENCES customers(name)
    )
''')

applications = [
    ("appa", "1", "https://appa.com", "3000", "adamapple"),
    ("appb", "2", "https://appb.com", "3000", "bobbaker"),
    ("appc", "3", "https://appc.com", "3000", "carlcake")
]

cursor.executemany('''
    INSERT INTO applications (application_name, version_num, application_url, application_port, name)
    VALUES (?, ?, ?, ?, ?)
''', applications)

cursor.execute('''
    CREATE TABLE IF NOT EXISTS languages_used (
        id INTEGER PRIMARY KEY,
        application_name TEXT,
        language_name TEXT,
        name TEXT,
        FOREIGN KEY(application_name) REFERENCES applications(application_name),
        FOREIGN KEY(language_name) REFERENCES code_languages(language_name),
        FOREIGN KEY(name) REFERENCES customers(name)
    )
''')

languages_used = [
    ("appa", "Node.js", "adamapple"),
    ("appa", "React.js", "adamapple"),
    ("appb", "Python", "bobbaker"),
    ("appb", "Java", "bobbaker"),
    ("appc", "C++", "carlcake"),
    ("appc", "C#", "carlcake")
]

cursor.executemany('''
    INSERT INTO languages_used (application_name, language_name, name)
    VALUES (?, ?, ?)
''', languages_used)

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        name TEXT PRIMARY KEY,
        password TEXT
    )
''')

users = [
    ("adamapple", "$2b$10$33u9zGQCcccim5Zm9xXpyuTaT7pPuSrh22.FaTDZYZHodvd.ZEAXO"),
    ("bobbaker", "$2b$10$OZ2QOsQrwRWsN5NDrLKGkO/U9w2u5VB121lGpcflVgDa56DfIZNAO"),
    ("carlcake", "$2b$10$Es2Oi59OkyGIV7jwAKG6PuxrVxvTGkMEIfAbMRb.SZao.5OETuE2e")
]

cursor.executemany('''
    INSERT INTO users (name, password)
    VALUES (?, ?)
''', users)

db.commit()
cursor.close()
db.close()


