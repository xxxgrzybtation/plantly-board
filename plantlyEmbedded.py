from machine import ADC, Pin
import network
import urequests
import utime
import ujson

api_url = "apiURL"

def get_capacitator_measurements():
    soil_adc = ADC(Pin(27)) # convert analog signal into digital
    max_moisture_value = 65535 # max value of uint16
    moistureData = 100 - ((soil_adc.read_u16()*100)/ max_moisture_value) # calculate moisture
    moisturePercentage = "%.2f" % moistureData
    print(f"moisture: {moisturePercentage}% (adc: {str(soil_adc.read_u16())})")
    return moisturePercentage

def connectToInternet(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

def makeGetRequest(url):
    print("Querying the user object")
    r = urequests.get(url)
    print(r.json())

def makePostRequest(data, api_url):
    data = {
        "name": "Test",
        "last_name": "Test",
        "purpose": data
    }

    json_data = ujson.dumps(data)
    response = urequests.post(api_url, data=json_data)
    response_text = response.text
    response.close()
    print("Response:", response_text)
    print(json_data)

if __name__ == "__main__":
    connectToInternet("name", "password")
    while True:
        moistureData = get_capacitator_measurements()
        makePostRequest(moistureData, api_url)
        utime.sleep(600)
