from gpiozero import DistanceSensor
from time import sleep

def get_distance(echo_io, trigger_io):
    sensor = DistanceSensor(echo = echo_io, trigger = trigger_io)
    return sensor.distance
