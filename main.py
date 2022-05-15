import pygame
from pygame.locals import *
import pygame.camera
import pygame.image
import numpy as np
import cv2

pygame.init()
pygame.camera.init()
pygame.display.set_caption("Game")

cameras = pygame.camera.list_cameras()

print("Using camera %s ..." % cameras[0])

cam1 = pygame.camera.Camera(cameras[0])
cam1.start()

img1 = cam1.get_image()

flags = DOUBLEBUF
screen = pygame.display.set_mode((500,500), flags, 4)
frame = 0

def take_screen_shot():
    global frame
    save_file = 'screenshots\\'+str(frame)+'.png'
    pygame.image.save(img1, save_file)

def image_proccesing():
    global frame
    global counter
    if frame >= 1:
        img1 = cv2.imread('screenshots\\'+str(frame - 1)+'.png', 0)
        img2 = cv2.imread('screenshots\\'+str(frame)+'.png', 0)
        sub = cv2.subtract(img1, img2)

        coords = np.argwhere(sub > 100)
        coords_list = coords.tolist()
        
        if coords_list:
            x = list(list(zip(*coords_list))[0])
            y = list(list(zip(*coords_list))[1])

            for i in range(len(x)):
                pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(y[i], x[i], 1, 1))
            x.clear()
            y.clear()

clock = pygame.time.Clock()
while 1:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        pygame.event.set_allowed(KEYDOWN)
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            pygame.camera.quit()

    img1 = cam1.get_image().convert()
    take_screen_shot()
    image_proccesing()
    clock.tick(15)
    pygame.display.update()
    frame += 1
