from configparser import ConfigParser
from configparser import MissingSectionHeaderError
from os.path import join
from os.path import dirname
from os import getenv
from os import makedirs

CONFIG_DIR     = ".config"
APP_CONFIG_DIR = "redmine-assistant"
CONFIG_FILE    = "redmine.conf"

class RedmineConfig:


	def __init__(self):
		self.config = ConfigParser()
		home_dir = getenv("HOME")
		config_file = join(home_dir, CONFIG_DIR, APP_CONFIG_DIR, CONFIG_FILE)
		try:
			self._load_config_file(config_file)
		except FileNotFoundError:
			self.url, self.api_key = self._get_user_info_from_input()
			answer = input(f'Do you want to save your config in \"{config_file}\"? [y/N]: ')
			if answer.lower() in ["", "y", "ye", "yep", "yes"]:
				self._write_config_file(config_file, self.url, self.api_key)
		except MissingSectionHeaderError:
			pass
		

	def set_user_info(self, url: str, api_key: str):
		self.url = url
		self.api_key = api_key


	def get_user_info(self):
		return self.url, self.api_key


	def _load_config_file(self, config_file: str):
		with open(config_file, "rt") as fd:
			self.config.read_file(fd, config_file)
			self.set_user_info(url=self.config["user_info"]["url"],
					  		   api_key=self.config["user_info"]["api_key"])
	

	@staticmethod
	def _get_user_info_from_input():
		print("Your config file is missing!")
		url = input("Please enter Redmine URL: ")
		api_key = input("Please enter your API key: ")
		return url, api_key

		
	@staticmethod
	def _write_config_file(config_file: str, url: str, api_key: str):
		makedirs(dirname(config_file))
		with open(config_file, "wt") as file:
			file.write("[user_info]\r\n")
			file.write(f'url={url}\r\n')
			file.write(f'api_key={api_key}\r\n')
