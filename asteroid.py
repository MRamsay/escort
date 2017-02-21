import pygame,random
class Asteroids(pygame.sprite.Sprite):
	direction=None
	rotation_degrees=0	
	
	image_reference=pygame.image.load("images/Asteroid.png")	
	
	def __init__(self,WINDOWHEIGHT,WINDOWWIDTH):
		self.rotation_change=random.uniform(-1,1)
		self.rotation_degrees		
		pygame.sprite.Sprite.__init__(self)		
		self.image=pygame.image.load("images/Asteroid.png")
		self.rect=self.image.get_rect()
		self.rect.y=random.randint(self.rect.height/2,(WINDOWHEIGHT-self.rect.height))
		self.direction = random.choice(["left","right"])
		if self.direction == "left":
			self.rect.x=WINDOWWIDTH+self.rect.x
		else:
			self.rect.x=(0-self.rect.x)
		self.hit_points = 5	
		self.rect_y_reference=self.rect.y
	def update_position(self,speed,WINDOWWIDTH,game,seconds):
		if self.direction=="left":
			self.rect.x-=(speed*seconds)
		else:
			self.rect.x+=(speed*seconds)
				
		self.image=pygame.transform.rotate(self.image_reference,self.rotation_degrees)
		self.rect=self.image.get_rect(center=self.rect.center)
		self.rotation_degrees+=self.rotation_change		
		
		
		if self.rect.x > (WINDOWWIDTH+self.rect.x):
			self.kill()
		elif self.rect.x < (0-self.rect.x):
			self.kill()
			
	def shot(self,game):
		if self.hit_points <= 0:
			self.kill()
		else:
			self.hit_points-=1

	
