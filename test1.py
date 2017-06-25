from gpiozero import DistanceSensor
from signal import pause
import pygame
import pygame.camera
import os
from gtk import gdk
import sys
import RPi.GPIO


def launch_cam():
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

    sensor = DistanceSensor(echo = 17,trigger =4, max_distance=5)
    colour = GREEN
    image_loc = (screen_size[0]/2 - size[0]/2, 0) #top center
    
    
    while True:
        lcd.fill(BLACK)
        cam.get_image(surf)
        lcd.blit(surf, (image_loc[0],image_loc[1])) #top and center
        cm = int(sensor.distance * 100)
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
        
    return 0

