import sqlite3 as sqltor
mycon = sqltor.connect('Project.db')
c=mycon.cursor()

c.execute("create table WeatherApp(CityName varchar(20),\
                                    CountryName varchar(20),\
                                    Temperature float,\
                                    MaxTemperature float,\
                                    MinTemperature float,\
                                    Pressure float,\
                                    Humidity float,\
                                    WindSpeed float,\
                                    SunriseTime float,\
                                    SunsetTime float,\
                                    Description text)")
"""
#c.execute("select * from WeatherApp")
#c.execute('delete from WeatherApp where MaxTemperature=26.26')
data = c.fetchall()
for row in data:
    print(row)"""
mycon.commit()
mycon.close()
                                    
