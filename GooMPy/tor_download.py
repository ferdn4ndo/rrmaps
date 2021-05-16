#!/usr/bin/python
# -*- coding: utf-8 -*-
import io
import pycurl

import stem.process

from stem.util import term

# SOCKS_PORT = 7000


class TorDownload(object):

	def __init__(self, socks_port = 7000, requests_refresh = 20, tls = '{br}'):
		'''
		@brief      Constructs the object.
		
		@param      self              The object
		@param      socks_port        The socks port
		@param      requests_refresh  The number of requests before refreshing the tor connection
		'''

		self.socks_port = socks_port
		self.requests_refresh = requests_refresh
		self.tls = tls

		self.tor_process = None
		self.requests_counter = 0

		self.startTor()

	def startTor(self):

		self.tor_process = stem.process.launch_tor_with_config(
			config = {
				'SocksPort': str(self.socks_port),
				'ExitNodes': self.tls,
			},
			init_msg_handler = self.print_bootstrap_lines,
		)

	def print_bootstrap_lines(self, line=""):
		self.printMsg(line,"Bootstrapped",term.Color.GREEN)
	
	def printMsg(self, line = "DUMMY MESSAGE LINE", filter_string = "", color = term.Color.BLUE):
		if filter_string != "":
			if filter_string in line:
				print(term.format(line, color))
		else:
			print(term.format(line, color))

	def query(self,url=""):
		if self.tor_process is not None:
			self.requests_counter += 1

			if(self.requests_counter >= self.requests_refresh):
				self.printMsg("Requests limit exceeded. Generating new Tor connection [30 sec sleep]","",tem.Color.RED)
				self.killTor()
				sleep(30)
				self.startTor()
				if self.tor_process is not None:
					self.printMsg("New Tor connection generated!","",tem.Color.GREEN)
				else:
					self.printMsg("New Tor connection FAILED!","",tem.Color.RED)
					return -1

			output = io.BytesIO()
			query = pycurl.Curl()
			query.setopt(pycurl.URL, url)
			query.setopt(pycurl.PROXY, 'localhost')
			query.setopt(pycurl.PROXYPORT, self.socks_port)
			query.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5_HOSTNAME)
			query.setopt(pycurl.WRITEFUNCTION, output.write)

			try:
				query.perform()
				return output.getvalue()
			except pycurl.error as exc:
				return "Unable to reach %s (%s)" % (url, exc)
		else:
			self.startTor(self)
			self.query(url)

	def downloadContent(self,url="",tofilename="output.dat"):
		file = open(tofilename, 'wb')
		result = self.query(url)
		f.write(result)
		f.close
		return 0


	def checkEndpoint(self):
		print(term.format("\nChecking our endpoint:\n", term.Attr.BOLD))
		print(term.format(query("https://www.atagar.com/echo.php"), term.Color.BLUE))

	
  	def killTor(self):
  		self.tor_process.kill()  # stops tor




# def query(url):
#   """
#   Uses pycurl to fetch a site using the proxy on the SOCKS_PORT.
#   """

#   output = io.BytesIO()

#   query = pycurl.Curl()
#   query.setopt(pycurl.URL, url)
#   query.setopt(pycurl.PROXY, 'localhost')
#   query.setopt(pycurl.PROXYPORT, SOCKS_PORT)
#   query.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5_HOSTNAME)
#   query.setopt(pycurl.WRITEFUNCTION, output.write)

#   try:
#     query.perform()
#     return output.getvalue()
#   except pycurl.error as exc:
#     return "Unable to reach %s (%s)" % (url, exc)


# # Start an instance of Tor configured to only exit through Russia. This prints
# # Tor's bootstrap information as it starts. Note that this likely will not
# # work if you have another Tor instance running.

# def print_bootstrap_lines(line):
#   if "Bootstrapped " in line:
#     print(term.format(line, term.Color.BLUE))


# print(term.format("Starting Tor:\n", term.Attr.BOLD))

# tor_process = stem.process.launch_tor_with_config(
#   config = {
#     'SocksPort': str(SOCKS_PORT),
#     'ExitNodes': '{br}',
#   },
#   init_msg_handler = print_bootstrap_lines,
# )



# print(query("https://media.readthedocs.org/css/sphinx_rtd_theme.css"))

