conn = pymysql.Connect(host=db_host,
                               user=db_user,
                               password=db_password,
                               database=db_name,
                               autocommit=True)