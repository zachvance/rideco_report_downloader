FIRST_DATE = '2021-11-01'

SECOND_DATE = '2021-11-30'

# Possible export types: ride, fare, vehicle_hours, fare_segment, online, nearby_driver_supply_alerts, acceptance,
# search, driver_transition
EXPORT_TYPES = ['ride', 'vehicle_hours']

# Adjust these program codes as required
program_001 = '268298b4-73bb-415c-8fb5-6a5524ccceb6'  # St. Catharines program code
program_002 = 'a0b63f37-a251-4e15-a769-36432ad8c00d'  # Thorold program code
PROGRAMS = [program_001, program_002]

PAYLOAD = {'username': 'EMAIL/USERNAME', 'password': 'PASSWORD'}

#URL subdomain (https://dash.[SUBDOMAIN].rideco.com)
URL_SUBDOMAIN = 'sctc'
