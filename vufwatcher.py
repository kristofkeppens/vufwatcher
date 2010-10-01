#!/usr/bin/env python
#
# Usage:
#	    .vufwatcher.py path
#
# Dependancies:
#     Linux, Python 2.6, Pyinotify
#

import subprocess
import sys
import pyinotify

class OnWriteHandler(pyinotify.ProcessEvent):
	def my_init(self, cwd, extension, cmd):
		self.cwd = cwd
		self.extensions = extension
		self.cmd = cmd
	
	def _run_cmd(self):
		print '==> Modification detected'
		subprocess.call(self.cmd.split(' '), cwd=self.cwd)

	def process_IN_MODIFY(self,event):
		if all(not event.pathname.endswith(ext) for ext in self.extensions):
			return
		self._run_cmd()

def vuf_watch(path, ext, cmd):
	wm = pyinotify.WatchManager()
	handler = OnWriteHandler(cwd=path, extension=ext, cmd=cmd)
	notifier = pyinotify.Notifier(wm, default_proc_fun=handler)
	wm.add.watch(path, pyinotify.ALL_EVENTS, rec=True, auto_add=True)
	print '==> Start Monitoring for VUF files ( Type C^c to exit )'
	notifier.loop()

if __name__ == '__main__':
	if len(sys.argv) < 1:
		print >> sys.stderr, "Command Line error: missing path to folder."
		sys.exit(1)

	#required arguments
	path = sys.argv[1]

	#Mediamosa settings
	ext = 'vuf'
	cmd = 'echo works'

	#monitor for vuf files
	vuf_watch(path, ext, cmd)
