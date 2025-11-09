import pygame, random, time

pygame.font.init()
pygame.mixer.init()
WIDTH,HEIGHT = 1300,900
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("space war")

enemy_ship = pygame.transform.scale(pygame.image.load("./enemy_ship.png"),(20,30))
space_ship = pygame.transform.scale(pygame.image.load("./space_ship.png"),(40,60))
BG = pygame.transform.scale(pygame.image.load("./bg_2.png"),(WIDTH,HEIGHT))
Bullet = pygame.transform.scale(pygame.image.load("./Bullet.png"),(10,15))
battle_sound = pygame.mixer.Sound("./battle_sound.mp3")
kill_sound = pygame.mixer.Sound("./last.mp3")
FONT = pygame.font.SysFont("comicsans",30)
STAR_WIDTH,STAR_HEIGHT = 20,30
PLAYER_VEL = 5
STAR_VEL = 3
FPS = 60


def draw(player,elapsed_time,full_power_enemy_ship_list,Fired_Bullet_list,score):
    WINDOW.blit(BG,(0,0))

    time_text = FONT.render(f"Time:{round(elapsed_time)}s",1,"WHITE")
    score_text = FONT.render(f"Score:{score}",1,"WHITE")
    WINDOW.blit(time_text,(10,10))
    WINDOW.blit(score_text,(10,40))
    WINDOW.blit(space_ship,(player[0],player[1]))

    for star in full_power_enemy_ship_list:
        WINDOW.blit(enemy_ship,(star[0],star[1]))
    for Bullet_fired in Fired_Bullet_list:
        WINDOW.blit(Bullet,(Bullet_fired[0],Bullet_fired[1]))
    pygame.display.update()

def main():
    player = [random.randint(1, WIDTH-40 ),HEIGHT-60]
    full_power_enemy_ship_list = []
    player_add_increament = False
    clock = pygame.time.Clock()
    star_add_increament = 1000
    start_time = time.time()
    Fired_Bullet_list = []
    elapsed_time = 0 
    star_count = 0
    Fire_Bullet=0
    play_sound=1
    hit = False
    run = True
    score = 0

    while run:
        star_count+= clock.tick(FPS)
        elapsed_time= time.time() - start_time
#######################  ADD OBJECT  ##################################
        if star_count > star_add_increament:
            for _ in range(random.randint(3,5)):
                star_x = random.randint(0,WIDTH-STAR_WIDTH)
                star = pygame.Rect(star_x,-STAR_HEIGHT,STAR_WIDTH,STAR_HEIGHT)
                full_power_enemy_ship_list.append(star)
            star_add_increament = max(500,star_add_increament-10)
            Fired_Bullet_list.append([player[0]+20,player[1]])
            star_count =  0
##################### EVENT HANDELING  ######################################
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player_add_increament=True
                    l=-1
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    l=1
                    player_add_increament=True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player_add_increament=False
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player_add_increament=False
##################  TIME #################################
        if round(elapsed_time)%round(battle_sound.get_length()) == 0 and play_sound!=round(elapsed_time):
            battle_sound.play()
            play_sound=round(elapsed_time)
            battle_sound.set_volume(0.5)

####################  INCREMENT / DECREMENT  ############################
        if player_add_increament:  # space ship
            if l==-1 and player[0]>PLAYER_VEL:
                player[0] += PLAYER_VEL*l
            elif l==1 and WIDTH-PLAYER_VEL-40 >player[0]:
                player[0] += PLAYER_VEL*l

        for star in full_power_enemy_ship_list[:]:  # enemy ship
            star.y+= STAR_VEL
            if star.y + STAR_HEIGHT > HEIGHT :
                full_power_enemy_ship_list.remove(star)
            elif player[0]<star.x+STAR_WIDTH and star.x <player[0]+40 and star.y>850 :
                full_power_enemy_ship_list.remove(star)
                hit = True
                break
                
        for Bullet_fired in Fired_Bullet_list:  #BULLET
            for star in full_power_enemy_ship_list[:]:
                try:
                    if -5<((star.y+STAR_HEIGHT)-Bullet_fired[1])<5 and -15<(star.x+(STAR_WIDTH/2)-5-Bullet_fired[0])<15 :
                        full_power_enemy_ship_list.remove(star)
                        Fired_Bullet_list.remove(Bullet_fired)
                        score+=1
                        kill_sound.play()
                except:
                    pass
            Bullet_fired[1]-=STAR_VEL

        draw(player,elapsed_time,full_power_enemy_ship_list,Fired_Bullet_list,score)  #FUNCTION CALL
#########################  HIT  ############################################
        if hit:
            lost_text = FONT.render("OOPS!! You Lost!",1,"BLACK")
            score = FONT.render(f"your score was {score}",1,"BLACK")
            WINDOW.blit(lost_text,(WIDTH/2-lost_text.get_width()/2,HEIGHT/2-lost_text.get_height()/2))
            WINDOW.blit(score,(WIDTH/2-score.get_width()/2,HEIGHT/2-score.get_height()/2+lost_text.get_height()))
            pygame.display.update()
            pygame.time.delay(3000)
            break

main()
pygame.quit()
