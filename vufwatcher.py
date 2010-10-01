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
		if (not event.pathname.endswith(ext)):
			return
		self._run_cmd(event.pathname)

def vuf_watch(path, extension, cmd):
	wm = pyinotify.WatchManager()
	handler = OnWriteHandler(cwd=path, extension=extension, cmd=cmd)
	notifier = pyinotify.Notifier(wm, default_proc_fun=handler)
	wm.add_watch(path, pyinotify.ALL_EVENTS, rec=True, auto_add=True)
	print '==> Start Monitoring for %s files in %s ( Type C^c to exit )' % (extension, path)
	notifier.loop(daemonize=True)

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print >> sys.stderr, "Command Line error: missing path to folder."
		sys.exit(1)

	#required arguments
	path = sys.argv[1]
	#Mediamosa settings
	ext = 'vuf'
	cmd = 'notify-send'

	#monitor for vuf files
	vuf_watch(path, ext, cmd)
