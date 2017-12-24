#currently implementing
import utilities

class SaveSystem:
	def __init__(self, filename = None):
		self.defaultName = self.generate_filename()
		#Note: in the future, currentName should be in the IMAGE and not in the SaveSystem
		if(filename == None):
			self.currentName = self.defaultName
		else:
			self.currentName = filename
		self.recent_files=[""]*15
	def get_current_filename(self):
		return self.currentName
	def set_current_filename(self, name):
		self.currentName = name
	
	def generate_filename(self):
		return "newfile_"+utilities.gen_time()+".ansi"
		
	def pushName(self,filename=None):
		if(filename==None or filename == ""):
			filename = self.currentName
		if(filename in self.recent_files):
			self.recent_files.remove(filename)
			self.recent_files.append("")
		self.recent_files = [filename]+self.recent_files[:-1]
		
	def get_recent_filename(self, index = None):
		if(index==None):
			return self.recent_files
		else:
			return self.recent_files[index]