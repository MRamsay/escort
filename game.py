import pygame
class Game():
	def __init__(self):
		self._score=0
		self._Ships_saved=0
		self._lives=3		
		
		self.lives_updated=False
		self.score_updated=False
		self.Ships_saved_updated=False
		
	def update_lives(self,amount):
		self._lives+=amount
		self.lives_updated=True
	def get_lives(self):
		return self._lives
	def update_score(self,amount):
		self._score+=amount
		self.score_updated=True
	def get_score(self):
		return self._score
		
	def update_Ships_saved(self):
		self._Ships_saved+=1
		self.Ships_saved_updated=True
	def get_Ships_saved(self):
		return self._Ships_saved
	

	def get_updated_variables(self):
		return[self.lives_updated,self.score_updated,self.Ships_saved_updated]
