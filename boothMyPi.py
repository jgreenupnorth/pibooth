  # selfie.py
import tweepy
from picamera import PiCamera
from gpiozero import MotionSensor
from time import sleep
from sense_hat import SenseHat
from gpiozero import LED
from gpiozero import Button

#importing ability to play sounds
import pygame

#Initialise pygame and the mixer
pygame.init()
pygame.mixer.init()

#initialise sensehat
sense =SenseHat()
camera = PiCamera()
pir = MotionSensor(4)

#buttons and leds
greenLED = LED(14)
red1LED = LED(18)
yellowLED = LED(27)
red2LED = LED(10)

greenButton = Button(15)
red1Button = Button(17)
yellowButton = Button(22)
red2Button = Button(9)

#Jim & Jonathan
def get_api(cfg):
  auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
  auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
  return tweepy.API(auth)

def tweet(status):
  # Fill in the values noted in previous step here
  cfg = { 
    "consumer_key"        : "",
    "consumer_secret"     : "",
    "access_token"        : "",
    "access_token_secret" : "" 
    }

  api = get_api(cfg)
  #status = api.update_status(status=tweet)
  file="/home/pi/motion.jpg"
  api.update_with_media(file,status)
  # Yes, tweet is called 'status' rather confusing

def motion():
    pir.wait_for_motion()
    
    motion_detected = True
    return motion_detected

def capture():
        camera.rotation = 180
        camera.start_preview(alpha=192)
        sleep(1)
        camera.capture("/home/pi/motion.jpg")
        camera.stop_preview()
        
def countdown():
    #load the sound file
    mysound = pygame.mixer.Sound("cd_beep.wav")
    mysound2 = pygame.mixer.Sound("Shutter.wav")
    sense.show_message("Pick your tweet", scroll_speed=0.05)
    tweet_msg= tweet_selection()
    sense.show_message(tweet_msg, scroll_speed=0.05)
    
    #play the sound file for 10 seconds and then stop it
    mysound.play()
    sense.show_message("3")
    sleep(1)
    mysound.play()
    sense.show_message("2")
    sleep(1)
    mysound.play()
    sense.show_message("1")
    sleep(1)
    mysound2.play()

    r=(255,0,0)
    w=(255,255,255)
    g=(0,255,0)
    
    grin=[w,w,w,w,w,w,w,w,
          w,r,r,w,w,r,r,w,
          w,r,r,w,w,r,r,w,
          w,w,w,r,r,w,w,w,
          w,r,w,r,r,w,r,w,
          w,r,w,w,w,w,r,w,
          w,r,r,r,r,r,r,w,
          w,w,w,w,w,w,w,w,]
    sense.set_pixels(grin)
    capture()
    sleep(2)

    sense.show_message("Tweeting!")

    tick=[w,w,w,w,w,w,w,w,
          w,w,w,w,w,w,g,w,
          w,w,w,w,w,g,w,w,
          w,w,w,w,g,w,w,w,
          w,g,w,g,g,w,w,w,
          w,g,g,g,w,w,w,w,
          w,g,g,w,w,w,w,w,
          w,w,w,w,w,w,w,w,]
    sense.set_pixels(tick)
    tweet(tweet_msg)
    sleep(2)
    sense.clear()


def all_off():
    greenLED.off()
    red1LED.off()
    yellowLED.off()
    red2LED.off()

def tweet_selection():
    while True:
        
        if greenButton.is_pressed:
            all_off()
            greenLED.on()
            status = 'I like pie. RaspberryPi #picademy'
            break
        
        elif red1Button.is_pressed:
            all_off()
            red1LED.on()
            status = 'I met a rocket scientist! #picademy'
            break
        elif yellowButton.is_pressed:
            all_off()
            yellowLED.on()
            status = "Jimmy Green's Dream Team #picademy"
            break
        elif red2Button.is_pressed:
            all_off()
            red2LED.on()
            status = "And i need one more. Wave your arm in the air like you just don't care #picademy @littlemisssauce"
            break
    sleep(2)
    all_off()
    return status

while True:

    m_dect = motion()
    if m_dect == True:
        countdown()
        sense.clear()
    sleep(60)
    
