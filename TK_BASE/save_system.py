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
		self.load_recent()
		
	def save_recent(self):
		f = open("recent.ini","w")
		for filename in self.recent_files:
			f.write(filename+"\n")
		
	def load_recent(self):
		self.recent_files = []
		try:
			f = open("recent.ini","r")
			for filename in f.readlines():
				filename = filename.strip()
				if(filename!=""):
					self.recent_files.append(filename)
		except:
			self.recent_files=[""]*15
			self.save_recent()
		self.recent_files.extend([""]*(15-len(self.recent_files)))
		
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
		self.save_recent()
	def get_recent_filename(self, index = None):
		if(index==None):
			return self.recent_files
		else:
			return self.recent_files[index]