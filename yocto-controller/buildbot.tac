import os

from twisted.application import service
from buildbot.master import BuildMaster

basedir = r'.'
rotateLength = 10000000
maxRotatedFiles = 99

# if this is a relocatable tac file, get the directory containing the TAC
if basedir == '.':
    import os.path
    basedir = os.path.abspath(os.path.dirname(__file__))

application = service.Application('buildmaster')
try:
  from twisted.python.logfile import LogFile
  from twisted.python.log import ILogObserver, FileLogObserver
  logfile = LogFile.fromFullPath(os.path.join(basedir, "twistd.log"), rotateLength=rotateLength,
                                 maxRotatedFiles=maxRotatedFiles)
  application.setComponent(ILogObserver, FileLogObserver(logfile).emit)
except ImportError:
  # probably not yet twisted 8.2.0 and beyond, can't set log yet
  pass

configfile = r'controller.cfg'

m = BuildMaster(basedir, configfile)
m.setServiceParent(application)
m.log_rotation.rotateLength = rotateLength
m.log_rotation.maxRotatedFiles = maxRotatedFiles

