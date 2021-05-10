import pygame 
import sys 
  

def doPopup():
  while True:
    opt = ["first", "second", "third"]
    make_popup(opt)
    for e in pygame.event.get():
      if e.type == pygame.QUIT:
        pygame.quit()
      elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
        OPTION = option_selected(opt)
        if OPTION != None:
          return OPTION
        else:
          return None


def option_selected(options):
  popupSurf = pygame.Surface((200, 200))
  #draw up the surf, but don't blit it to the screen
  for i in range(len(options)):
    textSurf = smallfont.render(options[i], 1, color_light)
    textRect = textSurf.get_rect()
    textRect.top = top
    textRect.left = left
    top += pygame.font.Font.get_linesize(smallfont)
    popupSurf.blit(textSurf, textRect)
    if pygame.Rect.collidepoint(textRect, mouse):
      print(options)
      return
  popupRect = popupSurf.get_rect()
  popupRect.centerx = width/2
  popupRect.centery = height/2


def make_popup(options):
  popupSurf = pygame.Surface((200, 200))
  popupRect = popupSurf.get_rect()
  popupRect.centerx = width/2
  popupRect.centery = height/2
  pygame.draw.rect(screen, color_light, popupRect)
  for i in range(len(options)):
    textSurf = smallfont.render(options[i], 1, color_light)
    textRect = textSurf.get_rect()
    textRect.top = top
    textRect.left = left
    top += pygame.font.Font.get_linesize(smallfont)
    pygame.draw.rect(popupSurf, color_light, textRect)
    # popupSurf.blit(textSurf, textRect)
  # self.WIN.blit(popupSurf, popupRect)
  pygame.display.update()


# initializing the constructor 
pygame.init() 
  
# screen resolution 
res = (720,720) 
top = 0
left = 0

# opens up a window 
screen = pygame.display.set_mode(res) 
  
# white color 
color = (255,255,255) 
  
# light shade of the button 
color_light = (170,170,170) 
  
# dark shade of the button 
color_dark = (100,100,100) 
  
# stores the width of the 
# screen into a variable 
width = screen.get_width() 
  
# stores the height of the 
# screen into a variable 
height = screen.get_height() 
  
# defining a font 
smallfont = pygame.font.SysFont('Corbel', 35) 
  
# rendering a text written in 
# this font 
text = smallfont.render('Quit' , True , color) 

while True: 
    
  for ev in pygame.event.get(): 
      
    if ev.type == pygame.QUIT: 
      pygame.quit() 
        
    if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 3:
      doPopup()
      # print(self.deckOptions())

    #checks if a mouse is clicked 
    if ev.type == pygame.MOUSEBUTTONDOWN: 
        
      #if the mouse is clicked on the 
      # button the game is terminated 
      if pygame.Rect.collidepoint(textBox, mouse):
        # print("I QUIT")
        pygame.quit()
      # if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40: 
      # 	pygame.quit() 
          
  # fills the screen with a color 
  screen.fill((60,25,60)) 
    
  # stores the (x,y) coordinates into 
  # the variable as a tuple 
  mouse = pygame.mouse.get_pos() 
  
  textBox = pygame.Rect(width/2,height/2,140,40)

  # if mouse is hovered on a button it 
  # changes to lighter shade 
  if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40: 
    pygame.draw.rect(screen,color_light,textBox)
    # pygame.draw.rect(screen,color_light,[width/2,height/2,140,40]) 
      
  else: 
    pygame.draw.rect(screen,color_dark,textBox)
    # pygame.draw.rect(screen,color_dark,[width/2,height/2,140,40]) 
    
  # superimposing the text onto our button 
  screen.blit(text, (width/2+50,height/2)) 
    
  # updates the frames of the game 
  pygame.display.update() 


