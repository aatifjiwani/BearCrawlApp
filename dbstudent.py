import MySQLdb

def connectionStudent():
    conn = MySQLdb.connect(host="aatifjiwani.mysql.pythonanywhere-services.com", user="aatifjiwani", passwd="BearCrawl2017", db="aatifjiwani$bearcrawlstudents")
    c = conn.cursor()

    return c, conn