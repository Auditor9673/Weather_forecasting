import requests
API_KEY = "46fa1607fdeaf0e1f1c5faae6f658edd"

def get_data(place, days, data_type):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={place}&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()
    data_list = data.get('list', data.get('message'))

    if data_list == "city not found":
        status = "not_found"
        return status

    else:
        no_of_data = days*8
        dates = []
        temperature = []
        sky = []

        for date in data_list[:no_of_data]:
            dates.append(date['dt_txt'])

        if data_type == "Temperature":
            for temp_data in data_list[:no_of_data]:
                temperature.append((temp_data['main']['temp'])-273.15)
            return {"data":temperature, "dt": dates}

        elif data_type == "Sky-condition":
            for sky_data in data_list[:no_of_data]:
                sky.append(sky_data['weather'][0]['main'])
            return {"data":sky, "dt": dates}

if __name__ == "__main__":
    print(get_data("delhi", 1, "Sky-condition"))