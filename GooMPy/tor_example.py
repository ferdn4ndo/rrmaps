#!/usr/bin/python
# -*- coding: utf-8 -*-

from tor_download import TorDownload

def main():
	tor = TorDownload()

	tor.downloadContent("https://www.tutorialspoint.com/python/time_sleep.htm","out.html")

if __name__ == "__main__":
	main()