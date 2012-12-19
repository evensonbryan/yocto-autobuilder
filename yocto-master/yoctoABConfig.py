'''
Created on Dec 4, 2012

@author: pidge
'''

if __name__ == '__main__':
    from Autobuilder import Autobuilder 


    yocto_buildsets = Autobuilder()
    yocto_buildsets.parseConfig()
    yocto_buildsets.createBuildsets()
    
    