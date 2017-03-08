import datetime
import os
import json
import logging, logging.config

if __name__ == "__main__":
	logDirectory = "C:/temp/log"
file_log_conf = "./logging.json"
if os.path.exists(file_log_conf):
	with open(file_log_conf, 'rt') as f:
		config = json.load(f)
		# only if the log file name depends on date
		log_fname = os.path.join(logDirectory, datetime.datetime.now().strftime("indexing_%Y%m%d.log"))
		config["handlers"]["info"]["filename"] = log_fname
	logging.config.dictConfig(config)
else:
	logging.basicConfig(level=logging.DEBUG)

logging.info("Program End")

