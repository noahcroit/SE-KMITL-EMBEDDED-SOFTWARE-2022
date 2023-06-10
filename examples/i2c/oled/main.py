from oled import *




OLED = OLED_1inch5()
OLED.fill(0x0) 
OLED.text("128 x 128 Pixels",1,5,OLED.white)
OLED.text("OLED-1.5-Demo",1,20,OLED.white)
OLED.text("SSD1327",1,35,OLED.white)  
OLED.line(0,0,127,0,OLED.white)
OLED.fill_rect(0, 50,127,60,  2)
OLED.fill_rect(0, 60,127,70,  4)
OLED.fill_rect(0, 70,127,80,  6)
OLED.fill_rect(0, 80,127,90,  8)
OLED.fill_rect(0, 90,127,100, 10)
OLED.fill_rect(0,100,127,110, 12)
OLED.fill_rect(0,110,127,120, 14)
OLED.fill_rect(0,120,127,128, 16)
OLED.show()
time.sleep(1)

while True:
    pass
