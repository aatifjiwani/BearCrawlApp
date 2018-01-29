import MySQLdb

def connectionClub():
    conn = MySQLdb.connect(host="aatifjiwani.mysql.pythonanywhere-services.com", user="aatifjiwani", passwd="BearCrawl2017", db="aatifjiwani$bearcrawlclubs")
    c = conn.cursor()

    return c, conn