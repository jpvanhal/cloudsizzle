from kpwrapper import SIBConnection, Triple
import sqlite3

SQLITE_FILE = '../webui/cloudsizzle/db.sqlite'

sqlconn = sqlite3.connect(SQLITE_FILE)
cursor = sqlconn.cursor()

#query the course codes
with SIBConnection('SIB console', 'preconfigured') as sc:
    results = sc.query(Triple(None, 'rdf:type', 'Course'))
    for triple in results:
        query = "INSERT INTO courselist_course VALUES ('%s','');" % triple.subject
        print(query)
        cursor.execute("INSERT INTO courselist_course VALUES (?,'');", (triple.subject,))

#sqlconn.commit()
cursor.close()
sqlconn.close()
