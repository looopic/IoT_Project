from PIL import Image, ImageDraw, ImageFont

def draw_image(resolution,hum, pre,tem, cnt):
    # Create a new image with a black background
    width, height = resolution
    image = Image.new("RGB", (width, height), "black")

    # Create a drawing object
    draw = ImageDraw.Draw(image)

    # Set font for text
    font = ImageFont.load_default()

    # Draw "Milk inside" text and counter on the left side
    milk_text = "Milk inside"
    counter_value = cnt
    draw.text((20, 20), milk_text, fill="white", font=font)
    draw.text((20, 50), f"Counter: {counter_value}", fill="white", font=font)

    # Draw weather station GUI on the right side
    weather_station_x = width/2
    weather_station_y = 20

    # Draw temperature rectangle
    temperature_rect = [(weather_station_x, weather_station_y),
                        (weather_station_x + 100, weather_station_y + 50)]
    draw.rectangle(temperature_rect, outline="white", width=2)
    draw.text((weather_station_x + 10, weather_station_y + 10),
              f"Temp: {tem}°C", fill="white", font=font)

    # Draw humidity rectangle
    humidity_rect = [(weather_station_x, weather_station_y + 70),
                     (weather_station_x + 100, weather_station_y + 120)]
    draw.rectangle(humidity_rect, outline="white", width=2)
    draw.text((weather_station_x + 10, weather_station_y + 80),
              f"Humidity: {hum}%", fill="white", font=font)

    # Draw pressure rectangle
    pressure_rect = [(weather_station_x, weather_station_y + 140),
                     (weather_station_x + 100, weather_station_y + 190)]
    draw.rectangle(pressure_rect, outline="white", width=2)
    draw.text((weather_station_x + 10, weather_station_y + 150),
              f"Pressure: {pre} hPa", fill="white", font=font)

    # Save or display the image
    return image
