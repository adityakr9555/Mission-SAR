# Simulated GPS location

latitude = 22.5726
longitude = 88.3639


def get_gps_location():

    global latitude, longitude

    # Simulate drone movement
    latitude += 0.0001
    longitude += 0.0001

    return latitude, longitude