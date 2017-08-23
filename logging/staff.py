import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s %(funcName)s %(message)s | %(module)s")

file_hanlder = logging.FileHandler(__name__ + ".log")
file_hanlder.setFormatter(formatter)
logger.addHandler(file_hanlder)


class Staff:

	def __init__(self):
		self.id = "me"
		logger.info("staff inti")

	def run(self):
		logger.info("staff run()")


