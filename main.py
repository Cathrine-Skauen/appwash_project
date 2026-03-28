import requests
import os
from dotenv import load_dotenv

load_dotenv()

URL = "https://www.involtum-services.com/api-rest/location/9033/connectorsv2"
TOKEN = os.getenv("APPWASH_TOKEN")
if TOKEN is None:
    raise ValueError("APPWASH_TOKEN not found. Did you set it in .env?")

HEADERS = {
    "accept": "*/*",
    "content-type": "application/json; charset=utf-8",
    "language": "NO",
    "origin": "https://user.appwash.com",
    "platform": "appWash",
    "token": TOKEN,
}

PAYLOAD = {
    "page": 1,
    "pageSize": 1000
}
washers = {
    "37353","37354","37355","37356","37357",
    "37575","37576","37577","37578","37579"
}

dryers = {
    "36447","36448","36449","36450",
    "37389","37390","37391","37392","37393"
}
favorites_wash = {"37353","37354", "37355", "37356"}
favorites_dry = {"37392", "37393", "37391", "37390", "37389"}  # dine tørkefavoritter
maintenance = {"37355"}
response = requests.post(URL, headers=HEADERS, json=PAYLOAD)
response.raise_for_status()

data = response.json()["data"]

wash_available = 0
wash_fav_available = 0

dry_available = 0
dry_fav_available = 0

wash_total = len(washers)
dry_total = len(dryers)

for machine in data:
    machine_id = machine["externalId"]
    state = machine["state"]

    is_available = state == "AVAILABLE"
    is_usable = machine_id not in maintenance

#vaskemaskiner
    if machine_id in washers and is_available and is_usable:
        wash_available += 1

        if machine_id in favorites_wash:
            wash_fav_available += 1

#tørketrumler
    if machine_id in dryers and is_available and is_usable:
        dry_available += 1

        if machine_id in favorites_dry:
            dry_fav_available += 1



print("\nVASK:")
print(f"Totalt ledige: {wash_available}/{wash_total} ledige")
print(f"Favoritter ledige: {wash_fav_available}")

print("\nTØRK:")
print(f"Totalt ledige: {dry_available}/{dry_total} ledige")
print(f"Favoritter ledige: {dry_fav_available}")

