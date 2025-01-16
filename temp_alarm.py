import json
import time  # for adding pauses in the program
from boltiot import Bolt  # bringing in Bolt from the boltiot library
import conf  # configuration file

# Initialize the Bolt device
mybolt = Bolt(conf.bolt_api_key, conf.device_id)


def get_sensor_value(pin):

  """Gets the sensor value. Returns -999 if there is an error."""
  try:
    response = mybolt.analogRead(pin)
    data = json.loads(response)
    if data["success"] != 1:
       print("Request was not successful")
       print("Received response:", data)
    return -999
    sensor_value = int(data["value"])
    return sensor_value
  except Exception as e:
          print("An error occurred while fetching the sensor value")
          print(e)
          return -999

while True:
    # Step 1: Get the sensor value from LM35 on pin A0
    sensor_value = get_sensor_value("A0")
    
    if sensor_value == -999:
        print("Request failed. Skipping this round.")
        time.sleep(10)
        continue

    # Convert raw sensor value to temperature
    temperature = (100 * sensor_value) / 1024
    print("Current temperature:", temperature, "degrees Celsius")
    # Step 3: Compare temperature with threshold and control the buzzer
    if temperature >= conf.threshold:
        print("Warning: Temperature has exceeded the limit")
        response = mybolt.digitalWrite('0', 'HIGH') # Activate the buzzer
        time.sleep(10) # Buzzer will stay on for 10 seconds
        response = mybolt.digitalWrite('0', 'LOW') # Deactivate the buzzer

    # Step 4: Pause for 10 seconds before the next reading
    time.sleep(10)    