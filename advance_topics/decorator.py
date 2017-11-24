
""" 1. Baisc decorator example  """
""" Add logic without modifying original function """

# def decorator_func(ori_func):
	# def wrapper_func():
		# print("wrapper executed this b4 " + ori_func.__name__)
		# return ori_func()
	# return wrapper_func
	
# def display():
	# print("Display func ran")

# decorated_display = decorator_func(display)
# decorated_display()

"""
decorated_display = decorator_func(display)
   |||
@decorator_func <--- adding this means assignment like the above
"""

##### example using the @ symbol
# def decorator_func(ori_func):
	# def wrapper_func():
		# print("wrapper executed this b4 " + ori_func.__name__)
		# return ori_func()
	# return wrapper_func
	
# @decorator_func
# def display():
	# print("Display func ran")

# display()

""" 2. Two function with same decorator """
# def decorator_func(ori_func):
	# def wrapper_func(*args, **kwargs): ## in case function with differnt type or number of args
		# print("wrapper executed this b4 " + ori_func.__name__)
		# return ori_func(*args, **kwargs)
	# return wrapper_func

# @decorator_func
# def display_info(name, age):
	# print("Display info with arguments (" + name + ", " + str(age))
	
# @decorator_func
# def display():
	# print("Display func ran")

# display_info("what", 1)
# display()

""" 3. class decorator - will get the same result except using class """
""" using class decorator is less common """

# class decorator_class(object):
	# def __init__(self, ori_func):
		# self.ori_func = ori_func # tie function with instance of this class
		
	# def __call__(self, *args, **kwargs):
		# print("Call method from class executed this b4 " + self.ori_func.__name__)
		# return self.ori_func(*args, **kwargs)

# @decorator_class
# def display_info(name, age):
	# print("Display info with arguments (" + name + ", " + str(age))
	
# @decorator_class
# def display():
	# print("Display func ran")

# display_info("what", 1)
# display()


""" 4. prtaical example """
""" eg. logging or timing function """

def my_timer(ori_func):
	import time
	
	def wrapper(*args, **kwargs):
		t1 = time.time()
		result = ori_func(*args, **kwargs)
		t2 = time.time() - t1
		print("{} ran in: {} sec".format(ori_func.__name__, t2))
		return result
		
	return wrapper
	
@my_timer
def display_info(name, age):
	print("Display info with arguments (" + name + ", " + str(age) + ")")

print(display_info)
display_info("what", 1)


""" 5. decorator chain """
""" lower will be executed 1st """

@my_logger
@my_timer
def display_info(name, age):
	print("Display info with arguments (" + name + ", " + str(age) + ")")
|||
display_info = my_logger(my_timer(display_info))


## to avoid, do sth like

from functools import wraps
@wraps
def wrapper(*args, **kwargs):

### then you can use
@my_logger
@my_timer
def display_info(name, age):
	...
	
