'''
Created on Dec 26, 2012

@author: pidge
'''

from buildbot.steps.shell import ShellCommand

class RunSanityTests(ShellCommand):

    def __init__(self, **kwargs):
        ShellCommand.__init__(self, **kwargs)

    def describe(self, done=False):
        description = ShellCommand.describe(self,done)
        if done:
            failed = self.step_status.getStatistic('failed', 0)
            if failed > 0:
                description.append('Failed: %d' % failed)
        self.command = "run_sanity"           
        return description

    def createSummary(self,log):
        _re_result = re.compile(r'(\d*) failed')
       
        failed = 0
        lines = self.getLog('stdio').readlines()
        
        for l in lines:
            m = _re_result.search(l)
            if m:                
                failed = int(m.group(1))
             
        self.step_status.setStatistic('failed', failed)
