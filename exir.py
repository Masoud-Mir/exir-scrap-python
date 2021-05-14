import requests
import mysql.connector

url = "https://api.exir.io/v1/trades"


 mydb = mysql.connector.connect(
   host="your-host-name",
   user="your-username",
   password="your-passwor",
   database="your-DbName"
 )

 mycursor = mydb.cursor()


 mycursor.execute("CREATE TABLE IF NOT EXISTS trades (id INT AUTO_INCREMENT PRIMARY KEY, pair_name VARCHAR(255), first_name VARCHAR(255), second_name VARCHAR(255), size FLOAT(10,8), price INT, timestamp VARCHAR(255), side VARCHAR(255))")

 sql = "INSERT INTO trades (pair_name, first_name, second_name, size, price, side, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s)"



 r = requests.get(url)

 parsed_data = r.json()


 val = []

 for item in parsed_data:
     splited_name = item.split('-')
     first_name = splited_name[0]
     second_name = splited_name[1]

     for trade in parsed_data[item]:
         trade_data = (item, first_name, second_name, trade['size'], trade['price'], trade['side'], trade['timestamp'])
         val.append(trade_data)

     mycursor.executemany(sql, val)
     mydb.commit()




 while True:
     r2 = requests.get(url)
     parsed_data_2 = r2.json()

     for item in parsed_data_2:
         splited_name = item.split('-')
         first_name = splited_name[0]
         second_name = splited_name[1]

         for trade in parsed_data_2[item]:
             trade_data_2 = (item, first_name, second_name, trade['size'], trade['price'], trade['side'], trade['timestamp'])

             if trade_data_2 not in val[len(val)-(len(item)*50):]:
                 val.append(trade_data_2)
                 print(trade_data_2)
                 mycursor.executemany(sql, val)
                 mydb.commit()


