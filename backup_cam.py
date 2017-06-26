from gpiozero import DistanceSensor
from signal import pause
import pygame
import pygame.camera
import os
from gtk import gdk
import sys
import RPi.GPIO
import time

pin = 22

RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setwarnings(False)
RPi.GPIO.setup(pin, RPi.GPIO.IN)

state = 0


sensor = DistanceSensor(echo = 17,trigger =4, max_distance=5)

def launch_cam(sensor_io):
    print 'launch'   
    BLACK = 0,0,0
    GREEN = 0,255,0
    RED = 255,0,0
     
    if not os.getenv('SDL_FBDEV'):
        os.putenv('SDL_FBDEV', '/dev/fb1')
     
    if not os.getenv('SDL_VIDEODRIVER'):
        os.putenv('SDL_VIDEODRIVER', 'fbcon')

    # disables autofocus for Microsoft LifeCam
    os.system("uvcdynctrl --set='Focus, Auto' 0")

    screen_size = (gdk.screen_width(), gdk.screen_height())
    pygame.init()
    size = (640,480)
    lcd = pygame.display.set_mode((0,0))
    pygame.mouse.set_visible(False)
    lcd.fill(BLACK)
    pygame.display.update()
     
    pygame.camera.init()
      
    cam = pygame.camera.Camera('/dev/video0', size, 'RGB')
     
    cam.start()
    font_big = pygame.font.Font(None, 100)
    surf = pygame.Surface(size)

    colour = GREEN
    image_loc = (screen_size[0]/2 - size[0]/2, 0) #top center
    running = True
    
    while running:
        lcd.fill(BLACK)
        cam.get_image(surf)
        lcd.blit(surf, (image_loc[0],image_loc[1])) #top and center
        cm = int(sensor_io.distance * 100)
        if cm < 30:
            colour = RED

            text_surface = font_big.render('STOP', True, colour)
            rect = text_surface.get_rect(center=(image_loc[0] + size[0]/2,image_loc[1] + size[1]/2))
            lcd.blit(text_surface, rect)
     
        if cm < 120:
            pygame.draw.circle(lcd, colour, (image_loc[0] + size[0]/2,image_loc[1] + size[1]/2), (150-cm), 5)

        if cm > 120:
            colour = GREEN

        text_surface = font_big.render('%dcm'%cm, True, colour)
        rect = text_surface.get_rect(center=(image_loc[0]+ size[0]/2,image_loc[1]+size[1]+100))
        lcd.blit(text_surface, rect)
        pygame.display.update()
        
        input_state = RPi.GPIO.input(pin)
        if input_state == False:
            break
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                running = False
    pygame.quit()
    cam.stop()
    print "pygame quit"
    return 0


while True:
    input_state = RPi.GPIO.input(pin)
    if input_state == False and state == 0:
        state = 1
        x = launch_cam(sensor)
        print state
        while RPi.GPIO.input(pin) == 1:
            time.sleep(0.1)
    input_state = RPi.GPIO.input(pin)
    if input_state == False and state == 1:
        state = 0
        print state
        pygame.display.quit()
        pygame.quit()
        while RPi.GPIO.input(pin) == 1:
            time.sleep(0.1)
