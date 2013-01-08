'''
Created on Dec 29, 2012

__author__ = "Elizabeth 'pidge' Flanagan"
__copyright__ = "Copyright 2012-2013, Intel Corp."
__credits__ = ["Elizabeth Flanagan"]
__license__ = "GPL"
__version__ = "2.0"
__maintainer__ = "Elizabeth Flanagan"
__email__ = "elizabeth.flanagan@intel.com"
'''

if __name__ == '__main__':
    from Autobuilder import Autobuilder 


    yocto_buildsets = Autobuilder()
    yocto_buildsets.parseConfig()
    yocto_buildsets.createBuildsets()

