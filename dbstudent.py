import MySQLdb

def connectionStudent():
    conn = MySQLdb.connect(host="bearcrawl.mysql.database.azure.com",
                          user="bearcrawladmin@bearcrawl",
                          passwd="BearCrawl2017",
                          db="bearcrawlstudents")
    c = conn.cursor()
    
    return c, conn