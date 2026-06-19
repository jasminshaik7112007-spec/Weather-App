from tkinter import *
import requests
from PIL import Image, ImageTk
from io import BytesIO
root = Tk()
root.title("Weather App")
root.geometry("500x500")
root.config(bg="blue")
API_KEY = "1a276bdc0919bb632e179d9a7102510b"
def get_weather(event=None):
    city = city_entry.get().strip()

    if city == "":
        result_label.config(text="⚠️ Please enter a city name", fg="red")
        return

    result_label.config(text="🔍 Fetching weather...", fg="white")
    icon_label.config(image="")  

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        if str(data.get("cod")) != "200":
            result_label.config(text="❌ City not found", fg="red")
            return
        city_name = data["name"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        weather = data["weather"][0]["description"].title()
        icon_code = data["weather"][0]["icon"]
        
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_response = requests.get(icon_url)
        img_data = icon_response.content

        img = Image.open(BytesIO(img_data))
        img = img.resize((100, 100))
        weather_icon = ImageTk.PhotoImage(img)

        icon_label.config(image=weather_icon)
        icon_label.image = weather_icon  
        result = (
           f"{'🏢 City':<15}: {city_name}\n"
           f"{'🌡 Temp':<15}: {temp} °C\n"
           f"{'🤒 Feels Like':<15}: {feels_like} °C\n"
           f"{'💧 Humidity':<15}: {humidity} %\n"
           f"{'⛅ Condition':<15}: {weather}"
       )
        result_label.config(text=result, fg="black")
    except requests.exceptions.RequestException:
        result_label.config(text="❎Network error", fg="red")
    except Exception as e:
        result_label.config(text="❌ Unexpected error", fg="red")
        print("Error:", e)
Label(root, text="Weather App",
      font=("Arial", 22, "bold"),
      bg="green", fg="white").pack(fill=X, pady=10)
city_entry = Entry(root, font=("Arial", 14), justify="center")
city_entry.pack(pady=15, ipady=5)
city_entry.bind("<Return>", get_weather)
Button(root, text="Get Weather",command=get_weather,bg="green", fg="white").pack(pady=10)
icon_label = Label(root, bg="blue")
icon_label.pack(pady=10)
result_label = Label(root, text="",font=("Arial", 13),bg="white", justify="center")
result_label.pack(pady=20)
root.mainloop()