from Datos.Platillos import Arroz

class Sushi(Arroz.Arroz):
	def configurationFileName(self):
		return "sushi.json"