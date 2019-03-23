class parser:
	
	def get_last_line(full_error):
		all_lines = full_error.splitlines()
		return all_lines[-1]

	def get_last_line_as_array(full_error):
		return ((full_error.splitlines())[-1]).split()
	
	def get_error_type(full_error):
		all_lines = full_error.splitlines()
		last_line = all_lines[-1]
		words = last_line.split()
		first_word = words[0]
		return first_word[:-1]
