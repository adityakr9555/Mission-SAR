import re


# Alert log file
log_file = "sar_alerts.txt"


# Read alert log
with open(log_file, "r", encoding="utf-8") as file:
    data = file.read()


# Find all alerts
alerts = re.findall(r"ALERT\s+\d+", data)


# Find GPS locations
gps_locations = re.findall(
    r"GPS Latitude:\s*([\d.-]+)\s*GPS Longitude:\s*([\d.-]+)",
    data
)


# Count alerts
total_alerts = len(alerts)


# Print Mission Report
print()
print("======================================")
print("       MISSION-SAR REPORT")
print("======================================")

print(f"Total SAR Alerts     : {total_alerts}")
print(f"GPS Locations Logged : {len(gps_locations)}")

print()
print("Latest GPS Locations:")
print("--------------------------------------")


# Show last 5 GPS locations
for latitude, longitude in gps_locations[-5:]:
    print(f"Latitude  : {latitude}")
    print(f"Longitude : {longitude}")
    print("--------------------------------------")


print()
print("Mission Status : COMPLETE")
print("======================================")