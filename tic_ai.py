import pygame
import random
import os
import time
import solver as ttt
pygame.font.init()

MARGIN = 10
CUBE_SIZE = 170
MARGIN_SIZE = 2
WIDTH,HEIGHT = CUBE_SIZE*3+MARGIN_SIZE*2,CUBE_SIZE*3+CUBE_SIZE//2+MARGIN_SIZE*2
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Tic Tac Toe @Advait")
WIN.fill((255,255,255))

EMPTY = None

# Loading Images
TICK = pygame.image.load(os.path.join("assets","tick.png"))
CROSS = pygame.image.load(os.path.join("assets","cross.png"))

BG = pygame.transform.scale(pygame.image.load(os.path.join("assets","background-black.png")),(WIDTH,HEIGHT))

ICON = pygame.image.load(os.path.join("assets","icon.png"))
pygame.display.set_icon(ICON)


mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)
black = (0,0,0)
white = (255,255,255)
user = None
ai = None
user_img = None
al_img = None



class FILL:
  def __init__(self,img,x,y):
    self.img = img
    self.x = x
    self.y = y

  def draw(self,window):
    window.blit(self.img,(self.x,self.y))
   
    

def main():
  global user
  global ai
  global user_img
  global ai_img

  grid = ttt.initial_state()

  run = True
  game_is_still_going = True
  winner = None
  statement_panel = ""
  fill_boxes = []
  lost_count = 0
  clock = pygame.time.Clock()


  def redraw_window():
    WIN.fill((255,255,255))
    for i in range(3):
      for j in range(3):
         pygame.draw.rect(WIN,(0,0,0),(j*CUBE_SIZE+j*MARGIN_SIZE,i*CUBE_SIZE+i*MARGIN_SIZE,CUBE_SIZE,CUBE_SIZE))

    pygame.draw.rect(WIN,(0,0,0),(0,3*(CUBE_SIZE+MARGIN_SIZE),WIDTH,CUBE_SIZE//2))     

    for box in fill_boxes:
      box.draw(WIN)


    statement = largeFont.render(f"{statement_panel}",1,(255,255,255))
    WIN.blit(statement,(WIDTH//2 - statement.get_width()//2,(CUBE_SIZE + MARGIN_SIZE)* 3 + 15))

    pygame.display.update()


  while run:
      redraw_window()
      clock.tick(60)
      game_over = ttt.terminal(grid)
      player = ttt.player(grid) 

      if game_is_still_going == False:
          if lost_count > 60*3:
              run = False
          else:
              lost_count+=1
              continue
 
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              run = False

          if user != player and not game_over:
            time.sleep(0.5)
            move = ttt.minimax(grid)
            grid = ttt.result(grid, move)

            for row in range(3):
              for column in range(3):
                if grid[row][column] == ai:
                  box = FILL(ai_img,ai_img.get_width()//2 + CUBE_SIZE*column ,ai_img.get_width()//2 + CUBE_SIZE*row)
                  fill_boxes.append(box)


          click, _, _ = pygame.mouse.get_pressed()
          if click == 1 and user == player and not game_over:
            pos = pygame.mouse.get_pos()
            column = pos[0] // (CUBE_SIZE + MARGIN_SIZE//2)     # x coordinate og grid
            row = pos[1] // (CUBE_SIZE + MARGIN_SIZE//2)        # y coordinate of grid

            if column<3 and row <3:
              if grid[row][column] == EMPTY :
                grid[row][column] = user
                box = FILL(user_img,user_img.get_width()//2 + CUBE_SIZE*column ,user_img.get_width()//2 + CUBE_SIZE*row)
                fill_boxes.append(box)
      
  
      if game_over:
          winner = ttt.winner(grid)
          game_is_still_going = False
          if winner is None:
              statement_panel = "Game Over: Tie."
          else:
              statement_panel = f"Game Over: {winner} wins."
      elif user == player:
          statement_panel = f"Play as {user}"
      else:
          statement_panel = f"BOT thinking..."

  if winner =="X" or winner == "O":
      print(winner + " won.")  

  elif winner == None :
      print("Tie")


def main_menu():

    run = True
    global user
    global ai
    global user_img
    global ai_img
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run == False
                quit()

        pygame.display.update()
        WIN.fill(black)
        title = largeFont.render("Play Tic-Tac-Toe", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((WIDTH // 2), 100)
        WIN.blit(title, titleRect)

        # Draw buttons
        playXButton = pygame.Rect((WIDTH // 8), (HEIGHT // 2), WIDTH // 4, 50)
        playX = mediumFont.render("Play as X", True, black)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(WIN, white, playXButton)
        WIN.blit(playX, playXRect)

        playOButton = pygame.Rect(5 * (WIDTH // 8), (HEIGHT // 2), WIDTH // 4, 50)
        playO = mediumFont.render("Play as O", True, black)
        playORect = playO.get_rect()
        playORect.center = playOButton.center
        pygame.draw.rect(WIN, white, playOButton)
        WIN.blit(playO, playORect)


        my_name = mediumFont.render("- Advait Shrivastava",1,(255,255,255))
        WIN.blit(my_name,(WIDTH - my_name.get_width() - 20,HEIGHT - HEIGHT//4))

        # Check if button is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            user = None
            if playXButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.X
                ai = ttt.O
                user_img = CROSS
                ai_img = TICK
                main()
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.O
                ai = ttt.X
                user_img = TICK
                ai_img = CROSS
                main()
    pygame.quit()


main_menu()    
        