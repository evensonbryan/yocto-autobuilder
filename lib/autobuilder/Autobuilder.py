'''
Created on Dec 4, 2012

@author: pidge
'''
#!/usr/bin/python

class Autobuilder:
    '''
    classdocs
    '''



    def __init__(self, cfile=None):
        from config import *
        yocto_sources = YOCTO_SOURCES
        yocto_sched = YOCTO_SCHED
        yocto_builders = YOCTO_BUILDERS
        yocto_projname = YOCTO_PROJNAME
        yocto_projurl = YOCTO_PROJURL
        import os, config
        if cfile is None:
            try:
                self.cfile = os.environ.get("YOCTO_AB_CONFIG")
            except:
                self.cfile = "./config/yoctoAB.conf"

    def parseConfig(self):
        import ConfigParser
        print "LOADING CONFIG FILE"
        config = ConfigParser.ConfigParser()
        try:
            config.read(self.cfile)
        except:
            print "Can't seem to find the Config file. Is YOCTO_AB_CONFIG set?"
        buildsets=config.sections()
        self.configdict = {}
        for section in buildsets:
            self.configdict[section]= dict(config.items(section))
        return self.configdict

    def createBuildsets(self):
        import BuildSet
        import ast
        from buildbot.schedulers.forcesched import ForceScheduler
        from config import *

        for key in self.configdict.iterkeys():
            if str(key) != "BuildSets":
                locals()['buildset_%s' % key]=BuildSet.BuildSet(name=key,
                                                                steps=ast.literal_eval(self.configdict[key]['steps']), 
                                                                builders=ast.literal_eval(self.configdict[key]['builders']), 
                                                                layers=ast.literal_eval(self.configdict[key]['layers']))
                yocto_sched=YOCTO_SCHED
                yocto_sched.append(ForceScheduler(
                                    name=str(key),
                                    builderNames=['%s' % key]))