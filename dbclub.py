import MySQLdb

def connectionClub():
    conn = MySQLdb.connect(host="bearcrawl.mysql.database.azure.com",
                          user="bearcrawladmin@bearcrawl",
                          passwd="BearCrawl2017",
                          db="bearcrawlclubs")
    c = conn.cursor()
    
    return c, conn