#--DESCRIPTION OF THE PROGRAM--
'''The Name of the Project is: "Real-Time GUI Weather Application"
This project makes use of the Python Programming Language to design a real time GUI
based Interactive Weather Application, which is aimed to provide the
weather data for a large number of cities, some minor cities. The application
can fetch the weatger data for any significantly major city, anywher on the planet.
The Project makes the use of "Openweather API".'''

# import all modules
from tkinter import *
import requests
from PIL import Image, ImageTk
from datetime import datetime
import sqlite3 as sq

#import modules present in the same folder
import API_info as cw
import Ccode as cc

# Driver code 
if __name__ == "__main__" : 
  
    #creating the GUI window
    root = Tk()
    root.title("Weather-GUI Application ")

    #Function to collect details of the weather
    def format_response(weather):
        #Globaling variables for using them in different parts of the code
        global name, temp, temp_max, temp_min, prs, humid, wind_sp, sun_r, sun_s, desc

        #weather contains list of nested dictionaries. Now, if the value of the "cod" key is not equal to "404", 
        #then city is found, otherwise city is not found.
        if weather['cod'] != "404":
            #storing the values of different keys and storing them in their respective variables.
            name = weather['name']
            temp = round((weather['main']['temp'] - 273),2)
            temp_max = round((weather['main']['temp_max'] -273),2)
            temp_min = round((weather['main']['temp_min'] - 273),2)
            prs = (weather['main']['pressure'])/1000
            humid = weather['main']['humidity']
            wind_sp = round((weather['wind']['speed']*18/5),2)
            sun_r = datetime.fromtimestamp(weather['sys']['sunrise'])
            sun_s = datetime.fromtimestamp(weather['sys']['sunset'])
            desc = weather['weather'][0]['description']
            #Collecting all key values in report
            report =  'City: %s \
                        \nTemperature: %s°C \
                        \nMaximum Temperature: %s°C \
                        \nMinimum Temperature: %s°C \
                        \nPressure: %sbar \nHumidity: %s \
                        \nWind Speed: %skm/h \
                        \nSunrise: %s \
                        \nSunset: %s \
                        \nDescription: %s' \
                        % (name, temp, temp_max, temp_min,  prs,  humid,  wind_sp, sun_r, sun_s, desc)
            print("The Weather Details of ",name,",",country, " has been reported." )
        else:
            report = "Invalid Data"
            print("Invalid Data")
        return report    

    #Function to check and take input for the city and the respective country(assigned to button1)
    def weather(city):
        #Globalizing variables for using them in different parts of the code
        global api_key
        global base_url
        global country
        city_name = entry.get()             #Entering the city name in the entry field
        if city_name == "":
            print("No City Entered.")
        else:    
            api_key = cw.api_key
            base_url = cw.base_url

            country=input("Enter Country: ")
            if country == "":
                print("No Country Entered.")
            else:
                for i in cc.l:
                    if i["name"]==country:
                        code = i["code"]
                        break
                
        # complete_url variable to store complete url address                                        
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name + "," + code

        # get method of requests module return response object 
        response = requests.get(complete_url)

        # json method of response object convert json format data into python format data 
        weather = response.json()

        results['text'] = format_response(weather)

        icon_name = weather['weather'][0]['icon']
        open_image(icon_name)
        
    #Function for showing icons indicating respectice icons for respective weather
    def open_image(icon):
        size = int(lower_frame.winfo_height()*0.25)
        img = ImageTk.PhotoImage(Image.open('./img/'+icon+'.png').resize((size, size)))
        weather_icon.delete("all")
        weather_icon.create_image(0,0, anchor='nw', image=img)
        weather_icon.image = img
    #Creating the Canvas
    canvas = Canvas(root, height=600, width=800)
    canvas.pack()

     #Creating a background image for the Application
    background_image = PhotoImage(file="D:\\SHEKHAR\\CBSE XII\\Computer Science\\COMPUTER SCIENCE INVESTIGATORY PROJECT\\background.png")
    background_label = Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)

    #Creating the Heading label
    label1 = Label(root, text = "REAL-TIME WEATHER GUI APPLICATION")
    label1.config(font = ('algerian', 18))
    canvas.create_window(400, 25, window=label1)

    #Creating the main frame of the Canvas
    frame = Frame(root, bg='sky blue', bd=7)
    frame.place(relx = 0.5, rely =0.1, relwidth=0.9, relheight=0.1, anchor = 'n')

    #Entry field for inputting the cities
    entry = Entry(frame, font=40)
    entry.place(relwidth=0.3, relheight=1)

    #Function to Clear City Name from the entry field(assigned to button2)
    #Function to connect to the sql database(assigned to button3) 
    def connect():
        con = sq.connect('Project.db')
        print("Connected to Database Project.")
        c = con.cursor()

        c.execute('insert into WeatherApp(CityName, CountryName,\
                                            Temperature, MaxTemperature,\
                                            MinTemperature, Pressure, Humidity,\
                                            WindSpeed, SunriseTime, SunsetTime, Description)\
                                            values(:CityName,:CountryName,:Temperature,:MaximumTemperature,\
                                            :MinimumTemperature,:Pressure,:Humidity,:WindSpeed,:SunriseTime,\
                                            :SunsetTime,:Description)',\
                                            {'CityName':name, 'CountryName':country, 'Temperature':temp,\
                                             'MaximumTemperature':temp_max, 'MinimumTemperature':temp_min,\
                                             'Pressure':prs, 'Humidity':humid, 'WindSpeed':wind_sp,\
                                             'SunriseTime':sun_r, 'SunsetTime':sun_s, 'Description':desc})
        print("Record Inserted")

        c.execute("select * from WeatherApp")
        #fetching data from the table
        data = c.fetchall()
        for row in data:
            print(row)

        con.commit()
        con.close()

    #Function to Clear City Name from the entry field(assigned to button2)
    def clear():
        entry.delete(0, END)
        print("Cleared")
        country_code=0    

    #Creating buttons for different purposes, in the main frame of the Canvas
    button1 = Button(frame, text = "GET WEATHER", command=lambda: weather(entry.get()), bg='brown', fg='white', font=('garamond', 15, 'bold'))
    button1.place(relx=0.31, relwidth=0.28, relheight=1)

    button2 = Button(frame, text = "ADD TO DB", command = connect, bg='brown', fg='white', font=('garamond', 15, 'bold'))
    button2.place(relx=0.60, relwidth=0.2, relheight=1)

    button3 = Button(frame, text = "CLEAR", command = clear, bg='brown', fg='white', font=('garamond', 15, 'bold'))
    button3.place(relx=0.81, relwidth=0.19, relheight=1)

    #Creating the lower frame of the Canvas for showing the end result
    lower_frame = Frame(root, bg='sky blue', bd=12)
    lower_frame.place(relx=0.5, rely=0.25, relwidth=0.9, relheight=0.6, anchor='n')

    results = Label(lower_frame, anchor='nw', justify='left', bd=4)
    results.config(font=40, bg='white')
    results.place(relwidth=1, relheight=1)

    #Creating a place in the lower frame, in the Canvas to show the icon for the respective weather
    weather_icon = Canvas(results, bg='white', bd=0, highlightthickness=0)
    weather_icon.place(relx=.75, rely=0, relwidth=1, relheight=0.5)

    #Start the GUI
    root.mainloop()
