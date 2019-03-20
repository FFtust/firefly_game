class data_structure():
	def __init__(self):
		self.type = None  # 输入； 输出
		self.name = ""    
		self.key = None   
		self.current_value = None
		self.last_value = None

        self.return_value = None
		self.value_new_flag = False
		self.sync_type = None  # 变化同步；实时同步

	def value_update(self, new_value):
		pass

	def return_value_update(self, new_return):
		pass

class input_module_control():
	def __init__(self):
		pass

	def read_value(self, module):
		pass

	def read_value_until_new(self, module):
		pass

	def set_value(self, module, value):
		pass

	def is_value_new(self):
		pass
    

class output_module_control():
	def __init__(self):
		pass

	def read_value(self, module):
		pass

	def read_value_until_new(self, module):
		pass

	def set_value(self, module, value):
		pass

	def is_value_new(self):
		pass
    
