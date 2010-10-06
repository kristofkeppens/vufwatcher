#!/usr/bin/env python
#
# Usage:
#	    .vufwatcher.py path
#
# Dependancies:
#     Linux ( with inotify ), Python > 2.6, Pyinotify > 2.8
#

import subprocess
import sys
import pyinotify
from optparse import OptionParser

class OnWriteHandler(pyinotify.ProcessEvent):
	def my_init(self, cwd, extension, cmd):
		self.cwd = cwd
		self.extensions = extension
		self.cmd = cmd
	
	def _run_cmd(self, pathname ):
		print '==> Modification detected: %s' % pathname
		cmd = self.cmd.split(' ')
		cmd.append(pathname)
		subprocess.call(cmd, cwd=self.cwd)

	def process_IN_CREATE(self,event):
		if (not event.pathname.endswith(self.extension)):
			return
		self._run_cmd(event.pathname)

	def process_IN_MODIFY(self,event):
		if (not event.pathname.endswith(self.extension)):
			return
		self._run_cmd(event.pathname)

def vuf_watch(path, extension, cmd, daemon):	
	wm = pyinotify.WatchManager()
	handler = OnWriteHandler(cwd=path, extension=extension, cmd=cmd)
	notifier = pyinotify.Notifier(wm, default_proc_fun=handler)
	wm.add_watch(path, pyinotify.ALL_EVENTS, rec=True, auto_add=True)
	print '==> Start Monitoring for %s files in %s ( Type C^c to exit )' % (extension, path)
	if(daemon):
		notifier.loop(daemonize=True)
	else:
		notifier.loop()

def main():	
	usage = "usage: %prog [options] arg"
	parser = OptionParser(usage, conflict_handler='resolve')
	parser.add_option("-p", "--path", nargs=1, help="Path to the directory to monitor.", dest="path")
	parser.add_option("-d", "--daemon", action="store_true", dest="daemon", help="Run this script as daemon.")

	(options, args) = parser.parse_args()
	daemon = 0
	if len(sys.argv) <=2:
		parser.error("Path is a required argument.")
		sys.exit(2)
	if options.daemon:
		daemon = 1
	if options.path == '':
		parser.error("Path is a required argument.")
		sys.exit(2)

	#Mediamosa settings
	ext = 'vuf'
	cmd = 'php /path/' #path to process.php

	#monitor for vuf files
	vuf_watch(options.path, ext, cmd, daemon)

if __name__ == '__main__':
	main()
