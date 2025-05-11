import requests

class WeatherPy:

    def __init__(self):
        self.api_key = "30d2b786e1db2954cbbab1acef439ace"
        self.base_url = "http://api.openweathermap.org/data/2.5/weather?"
        self.location = "New York"
        self.search_mode = "city"
        self.units = "imperial"
        self.previous_location = None
        self.unit_symbol = "°F"

    @property
    def complete_url(self):
        """creates url with api_key"""
        if self.search_mode == "zip":
            return f"{self.base_url}appid={self.api_key}&zip={self.location},us&units={self.units}"
        else:
            return f"{self.base_url}appid={self.api_key}&q={self.location}&units={self.units}"
    
    def get_location(self):
        """returns current set location"""
        print(f"Current Location: {self.location}.")

    def set_location(self, new_location):
        """changes location and prints confirmation message"""
        self.previous_location = self.location
        self.location = new_location.strip()

        if self.location.isdigit():
            self.search_mode = "zip"
        else:
            self.search_mode = "city"
        
        print(f"Your updated location is now {self.location}.")

    def get_previous_location(self):
        """returns stored previous location"""
        return self.previous_location
    
    def undo_location(self):
        """revert location back to previously stored location"""
        self.location = self.previous_location
        print(f"Your location is {self.location} again.")
    
    def get_units(self):
        """print out currently used units for temp"""
        print(f"Your metrics are in {self.units} units.")
    
    def set_units(self, new_unit):
        """change units to either metric or imperial for temp usage"""
        if new_unit in ["metric", "imperial"]:
            self.units = new_unit
            if self.units == "imperial":
                self.unit_symbol = "°F"
            if self.units == "metric":
                self.unit_symbol = "°C"
                
            print(f"Your data will now be displayed as {self.units} units ({self.unit_symbol}).")
        else:
            print("Invalid units. Please choose either 'metric' or 'imperial.")

    def get_help(self):
        """prints all commands and helpful tips on how to use them"""
        print(
            """
---WeatherPy Help---

WeatherPy is a simple command-line weather app
______________________________________________________

Commands:

    weather 
        View current weather in set location
        Displays: temp, feels like temp, humidity, short weather description
    
    weather -temp
        Use -temp flag to just get the current temperature
    
    weather -day
        Use -day flag to get the high and low temps for the day

    change location
        Usage: Set location
        Required: City, State 
                State Example: CO or Colorado
        
        How To: 
        Step 1: Determine new location, such as “Denver, CO”
        Step 2: Enter required information
        >> change location 
        >> Enter new location name: 
        >> Denver
        >> Do you want to change your location to Denver? All weather data will be for this location. (y/n):
        Step 3: enter ‘y’ after confirmation prompt, if you want to proceed
        Step 4: Ensure location is set properly by reading confirmation message

    undo location
        Reset location to previously saved location

    get location
        Get current location

    change units
        Change the temperature units (imperial OR metric)

    help
        Print this help message
    
    exit
        Exit WeatherPy app
"""
            
        )


    def get_weather(self, temp=False, day=False):
        """
        Citation: https://www.geeksforgeeks.org/python-find-current-weather-of-any-city-using-openweathermap-api/
        Framework for weather API data retrieval editing from geeksforgeeks source code
        """
        response =  requests.get(self.complete_url)

        # store retrieved weather info from openweathermap API in weather_data
        weather_data = response.json()

        if weather_data["cod"] != "404":
            
            # store the value of "main" key in variable y
            y = weather_data["main"]
        
            # store the value corresponding to the "temp" key of y
            current_temperature = round(y["temp"])

            # if temp flag is True, only print current temp
            if temp:
                print(f"\nCurrent Temperature in {self.location}: {current_temperature}{self.unit_symbol}")
                return 
            
            # store the value corresponding to "temp_max" key of y
            day_max = round(y["temp_max"])

            # store the value corresponding to "temp_min" key of y
            day_min = round(y["temp_min"])

            # if day flag is True, only print min and max temps for the day
            if day:
                print(f"\nThe high for the day in {self.location} is: {day_max}{self.unit_symbol}")
                print(f"The low for the day in {self.location} is: {day_min}{self.unit_symbol}")
                return
            
            # store the value corresponding to the "humidity" key of y
            current_humidity = y["humidity"]

            # store the value corresponding to "feels_like" key of y
            feels_like = round(y["feels_like"])
        
            # store the value of "weather" key in variable z
            z = weather_data["weather"]
        
            # store the value corresponding to the "description" key 
            # at the 0th indeweather_data of z
            weather_description = z[0]["description"]
            
        
            # print full weather info 
            print(f"\nWeather in {self.location}:")
            print(f"Temperature: {current_temperature}{self.unit_symbol}")
            print(f"Feels like: {feels_like}{self.unit_symbol}")
            print(f"Humidity: {current_humidity}%")
            print(f"Description: {weather_description}")
                
    
        else:
            print(" Error: Location not found, please enter 'change location' with a valid location ")
        

def main():

    # create WeatherPy object
    w_app = WeatherPy()

    print(
        f""" 
-------------------------------
-----------WeatherPy-----------
-------------------------------
** Powered by OpenWeatherMap API **

WeatherPy is a simple command-line weather app. 
Find out the weather in your area right now or the daily highs and lows for the day.

Your current weather data is for: {w_app.location}
Enter 'change location' if you would like to change this
OR
Enter 'weather' if you would like to see the weather in {w_app.location}

Enter 'help' if you would like to explore WeatherPy's many functions!
            """
    )

    while True:

        # get user inputs in a loop
        command = input("\nEnter command: ").strip().lower()

        if command.startswith("weather"):
            # if temp flag set, set flag true
            if "-temp" in command:
                w_app.get_weather(temp=True)
            # if day flag set, set flag true 
            elif "-day" in command:
                w_app.get_weather(day=True)
            # no flag set, get full weather data
            else:
                w_app.get_weather()
        
        
        elif command == "get location":
            w_app.get_location()
        
        elif command == "change location":
            new_location = input("\nEnter new location name: ").strip()

            # check with user before changing location
            affirm_location = input(f"\nDo you want to change your location to {new_location}? Weather data is linked to location. (y/n): ").strip().lower()
            if affirm_location == "y":
                w_app.set_location(new_location)
            elif affirm_location == "n":
                print(f"Your location did not change.")
            else:
                print("Error: Command not recognized")

        elif command == "undo location":

            previous_location = w_app.get_previous_location()

            # if default location was never changed, there is no previous location, print error message
            if previous_location is None:
                print(f"There is no stored previous location. To change your location, enter 'change location'.")
            else:
                # check with user before reverting location
                affirm_undo = input(f"Do your want to change your location back to {previous_location}? (y/n): ").strip().lower()
                if affirm_undo == "y":
                    w_app.undo_location()
                elif affirm_undo == "n":
                    print(f"Your location did not change.")
                else:
                    print("Error: Command not recognized")
        
        elif command == "change units":
            unit_input = input(f"What units do you want to view temp in (metric/imperial)?: ")
            w_app.set_units(unit_input)
        
        elif command == "help":
            w_app.get_help()
        
        elif command == "exit":
            print("\nExiting...\n")
            break
        
        else:
            # user input a non-existant command
            print("I did not recognize that command. Enter 'help' to see all available commands")


if __name__ == "__main__":
    main()