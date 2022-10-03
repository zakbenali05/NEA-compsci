import pygame
from tiles import Tile
from settings import tile_size, screen_width
from player import Player

class Level:
    def __init__(self,level_data,surface):
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_scroll = 0
    
    def setup_level(self,layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        for row_index,row in enumerate(layout):
            for column_index, column in enumerate(row):
                x = column_index * tile_size
                y = row_index * tile_size

                if column == 'X':
                    tile = Tile((x,y),tile_size)
                    self.tiles.add(tile)
                if column == 'P':
                    player_sprite = Player((x,y))
                    self.player.add(player_sprite)
    
    def scroll_x(self):
        player = self.player.sprite
        #Where the player is
        player_x = player.rect.centerx
        #What direction they are moving in
        direction_x = player.direction.x
          
        #Scrolls the screen left or right when the player reaches a certain number of pixels out to the right or left
        if player_x < screen_width/4 and direction_x < 0:
            self.world_scroll = 5
            player.speed = 0
        elif player_x > screen_width - (screen_width/4) and direction_x > 0:
            self.world_scroll = -5
            player.speed = 0
        else:
            self.world_scroll = 0
            player.speed = 5
    
    #we have to split the horizontal and vertical movement, and calculate the resulting collisions seperately, to avoid errors
    def horizontal_mov_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        
        #looks through all of the sprites
        for sprite in self.tiles.sprites():
            #checks if any of the rectangles collide
            if sprite.rect.colliderect(player.rect):
                #Figure out whether the collision is on the left or the right side
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def vertical_mov_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                #Figure out whether the collision is on the tob or the bottom of the player
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0


    def run(self):
        #level tiles
        self.tiles.update(self.world_scroll)
        self.tiles.draw(self.display_surface)
        #player
        self.player.draw(self.display_surface)
        self.player.update()
        self.horizontal_mov_collision()
        self.vertical_mov_collision()
        self.scroll_x()

    