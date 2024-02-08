import pymysql

def dbconnect():
    conn = pymysql.connect(host='', user='', password='', db='', charset='utf8')
    return conn

def insert_data(conn):
    cur = conn.cursor()
    keyword = "상담"
    site_url = "www.nara.com"
    scrap_result = "<table></table>"
    sql = "INSERT INTO tbsys_web_scrap (site_url, keyword, scrap_result) VALUES('"+site_url+"', '"+keyword+"', '"+scrap_result+"')"
    cur.execute(sql)
    conn.commit()

def main():
    conn = dbconnect()
    print("Connect DB...")
    insert_data(conn)
    print("Insert DB..")
    
    conn.close()
    print("Finished DB..")

if __name__=="__main__":
    main()