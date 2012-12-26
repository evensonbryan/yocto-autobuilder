

from buildbot.process.buildstep import LoggingBuildStep
from buildbot.status.results import SUCCESS, FAILURE
import os, datetime 
import cPickle as pickle

class SetDest(LoggingBuildStep):
    renderables = [ 'abbase', 'btarget']
    haltOnFailure = True 
    flunkOnFailure = True 
    name = "Set Destination" 

    def __init__(self, factory, argdict=None):
        LoggingBuildStep.__init__(self)
        self.btarget=""
        self.abbase=os.environ.get("PWD")
        self.workdir=os.path.join(os.path.join(self.abbase, "yocto-slave"), self.btarget)
        self.description = ["Setting", "Destination"]
        self.addFactoryArguments(abbase=self.abbase, workdir=self.workdir)

    def describe(self, done=False):
        return self.description

    def setStepStatus(self, step_status):
        LoggingBuildStep.setStepStatus(self, step_status)

    def setDefaultWorkdir(self, workdir):
        self.workdir = self.workdir or workdir

    def start(self):

        try:
            self.getProperty('DEST')
        except:
            DEST = os.path.join(os.environ('BUILD_PUBLISH_DIR').strip('"').strip("'"), self.btarget)
            DEST_DATE=datetime.datetime.now().strftime("%Y%m%d")
            DATA_FILE = os.path.join(self.abbase, self.btarget + "_dest.dat")
            print DATA_FILE
            try:
                pfile = open(DATA_FILE, 'rb')
                data = pickle.load(pfile)
            except:
                pfile = open(DATA_FILE, 'wb')
                data = {}
                pickle.dump(data, pfile)
                pfile.close()
            # we can't os.path.exists here as we don't neccessarily have
            # access to the slave dest from master. So we keep a cpickle of 
            # the dests.
            
            try:
                # if the dictionary entry exists, we increment value by one, then repickle
                REV=data[os.path.join(DEST, DEST_DATE)]
                REV=int(REV) + 1
                #data[os.path.join(DEST, DEST_DATE)]=int(REV)
            except:
                REV=1
            data[os.path.join(DEST, DEST_DATE)] = REV
            pfile = open(DATA_FILE, 'wb')
            pickle.dump(data, pfile)
            pfile.close()
            DEST = os.path.join(DEST, DEST_DATE + "-" + str(REV))
            self.setProperty('DEST', DEST)
        return self.finished(SUCCESS)
