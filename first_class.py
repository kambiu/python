"""
Many programming lanuage can have first class function like Javascrit
"""

# def logger(msg):
	
	# def log_message():
		# print("Logs: ", msg)
	
	# return log_message ## main concept , return a cutom function

# func_hi = logger("Hello")
# func_hi()

## real applciation

def html_tag(tag):

	def wrap_text(msg):
		print("<{0}>{1}</{0}>".format(tag, msg))
		
	return wrap_text
	
tag_h1 = html_tag("h1")
tag_h1("This will be a Heading 1")

tag_p = html_tag("p")
tag_p("Paragraph 1")

tag_h1("This will be another Heading 1")
tag_p("Paragraph 2")