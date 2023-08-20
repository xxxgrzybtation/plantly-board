from machine import ADC, Pin
import utime

def get_capacitator_measurements():
    soil_adc = ADC(Pin(27)) #convert analog signal into digital on pin27
    max_moisture_value = 65535 #max value of uint16
    while True:
        moisture = 100 - ((soil_adc.read_u16()*100)/ max_moisture_value) #calculate moisture
        print("moisture: " + "%.2f" % moisture +"% (adc: "+ str(soil_adc.read_u16()) + ")")
        utime.sleep(0.5)
        
get_capacitator_measurements()