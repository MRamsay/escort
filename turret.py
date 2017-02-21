import pygame

class Turret(pygame.sprite.Sprite):
	
	def __init__(self,WINDOWWIDTH,WINDOWHEIGHT):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.image.load("images/Ship.png")
		self.rect = self.image.get_rect()
		self.rect.x = (WINDOWWIDTH-self.rect.width)/2
		self.rect.y = WINDOWHEIGHT-(self.rect.height)*1.5
		self.can_shoot = True
	def update_position(self,direction,WINDOWWIDTH,SPEED,seconds,background_x):
		if direction == "left" and self.rect.x>15:
			self.rect.x-=(SPEED*seconds)*3	
			background_x+=(SPEED*seconds)*.15			
		elif direction == "right" and self.rect.x<(WINDOWWIDTH-(self.rect.width)):
			self.rect.x+=(SPEED*seconds)*3
			background_x-=(SPEED*seconds)*.15
		return background_x	
	def get_gun_position(self):
		position={}
		position["x"]=self.rect.x+(self.rect.width/2)
		position["y"]=self.rect.y-(self.rect.height/2)
		return position
	
	def update_can_shoot(self,can_shoot_update):	
		self.can_shoot=can_shoot_update
	def get_can_shoot(self):
		return self.can_shoot
