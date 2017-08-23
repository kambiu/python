import logging
import staff

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s %(funcName)s %(message)s | %(module)s")

file_hanlder = logging.FileHandler(__name__ + ".log")
file_hanlder.setFormatter(formatter)
logger.addHandler(file_hanlder)


def main():
	a = staff.Staff()
	logger.info("test")
	a.run()


if __name__ == "__main__":
	main()