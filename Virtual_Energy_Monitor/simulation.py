# code for simulating virtual energy
import random
import datetime

def simulate_appliance(name, is_on=True):
    if not is_on:
        return {
            "appliance": name,
            "voltage": 0.0,
            "current": 0.0,
            "power": 0.0,
            "timestamp": datetime.datetime.now()
        }

    voltage = random.uniform(210, 240)
    current = random.uniform(0.1, 2.0)
    power = round(voltage * current, 2)
    return {
        "appliance": name,
        "voltage": round(voltage, 2),
        "current": round(current, 2),
        "power": power,
        "timestamp": datetime.datetime.now()
    }

def generate_data(status_dict):
    return [simulate_appliance(appliance, status_dict[appliance]) for appliance in status_dict]
