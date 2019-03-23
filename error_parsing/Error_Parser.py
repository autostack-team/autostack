class parser:
	
	def get_last_line(full_error):
		all_lines = full_error.splitlines()
		return all_lines[-1]
