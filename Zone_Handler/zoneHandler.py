import json
import os

QUESTION_TYPES = {
    b"\x00\x01": "a"
}
ZONES = {}  # Holds hostname -> record data, cannot grow as server runs


def load_zones():
  global ZONES
  json_zone = {}
  zones_path = "Zones"
  files = []
  try:
        files = os.listdir(zones_path)
  except FileNotFoundError:
        zones_path = "..\Zones"
        files = os.listdir(zones_path)
  for zone_file in files:
    with open(os.path.join(zones_path, zone_file), "r") as f:
      data = json.load(f)
      zone_name = data["$origin"]
      json_zone[zone_name] = data
  return json_zone


ZONES = load_zones()


def get_zone(zone_name:str):
  global ZONES
  zone = {}
  try:
    zone = ZONES[zone_name]
  except KeyError:
    return None
  return zone
