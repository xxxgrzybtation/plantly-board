from machine import ADC, Pin
import network
import urequests
import utime
import ujson
import config

data = []

def get_current_timestamp():
    current_time_tuple = utime.localtime()
    unix_timestamp = utime.mktime(current_time_tuple)
    return unix_timestamp

def get_capacitator_measurements():
    soil_adc = ADC(Pin(27)) # convert analog signal into digital
    max_moisture_value = 65535 # max value of uint16
    moisture_data = 100 - ((soil_adc.read_u16()*100)/ max_moisture_value) # calculate moisture
    moisture_percentage = int(moisture_data)
    print(f"moisture: {moisture_percentage}% (adc: {str(soil_adc.read_u16())})")
    return moisture_percentage

def create_new_datapoint():
    timestamp = get_current_timestamp()
    measurement = get_capacitator_measurements()
    datapoint = {"timestamp": timestamp, "value": measurement}
    return datapoint

def connect_to_internet(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

def make_get_request(url):
    print("Querying the user object")
    r = urequests.get(url)
    print(r.json())

def make_post_request(name, data, api_url):
    data = {
        "name": name,
        "data": data
    }

    json_data = ujson.dumps(data)
    response = urequests.post(api_url, data=json_data)
    response_text = response.text
    response.close()
    print("Response:", response_text)
    print(json_data)

if __name__ == "__main__":
    connect_to_internet(config.ssid, config.password)
    while True:
        datapoint = create_new_datapoint()
        data.append(datapoint)    
        if len(data) == 30:
            make_post_request("Drzewko Owocowe", data, config.apiURL)
            break
        utime.sleep(600)
