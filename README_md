file base url:
http://git.yoctoproject.org/cgit/cgit.cgi/yocto-autobuilder/tree

basis:
http://www.yoctoproject.org/docs/current/yocto-project-qs/yocto-project-qs.html

# Yocto AutoBuilder Documentation

## Introduction

Prior versions of the yocto-autobuilder required an extensive knowledge of buildbot as well as basic python. Over the years, as more targets were added the main configuation file had become hard to maintain, harder to read and, frankly, was not utilizing the power of buildbot. This document will explain some of the rational behind the refactor, introduce end users to the new configuration language, introduce the concept of customized buildsteps and give some basic instruction on how to modify an autobuilder setup.

### What is it

Yocto Autobuilder is essentially some extension to the vanilla build bot. This extension mainly addresses configuration file handling and Yocto specific build steps. For better maintainability, the Autobuilder ([see Autobuilder.py located at lib/python2.7/site-packages/autobuilder/](http://git.yoctoproject.org/cgit/cgit.cgi/yocto-autobuilder/tree/lib/python2.7/site-packages/autobuilder/Autobuilder.py)), handles configuration from multiple files. Additional build steps such as CheckOutLayers.py or CreateBBLayersConf are Yocto specific and simplify the bulders configuration.

### Setup

    $ git clone git://git.yoctoproject.org/yocto-autobuilder
    $ cd yocto-autobuilder
    $ . ./yocto-autobuilder-setup
    $ yocto-start-autobuilder both

### TODO

- buildhistory is not functional
- still missing some needed build targets
    - oe-core
    - fsl
    - p1022ds
    - bunch of meta-intel
- minor UI cleanup for toggling of triggered layers
- bbpriority needs to work
- verify buildappsrcrev
- deploy stuff
- killing triggers. this has been a long standing issue. look into

## Setting up a Yocto Autobuilder Build Cluster

Most autobuilder setups are individual to the circumstances of the user. This document outlines some of the configuration options/files, autobuilder setup gotchas and general autobuilder best practices.

### Setup to run headless sanity tests

If you plan on using the yocto autobuilder to run sanity testing, you will need to:

1. Install tight-vnc client and server.
2. Set up tap devs by running poky/scripts/runqemu-setup-tapdev
3. Add "xterm*vt100*geometry: 80x50+10+10" to .Xdefaults
4. Setup and start vnc session as the autobuilder user.
5. You MUST manually connect to the vnc session at least once prior to running a qemu sanity test (Something is getting set during the initial connection that I haven't figured out yet. Manually connecting seems to set up the session correctly.)

### Adding additional build workers

The production yocto autobuilder uses a cluster of build workers, all sharing the same SSTATE_DIR and DL_DIR via an NFS4 mounted NAS. The main nightly trigger prepopulates the DL_DIR, allowing the workers to not have to deal with a lot of downloading. In theory you could also run your build workers with NO_NETWORK to enforce a single point of populating DL_DIR.

Running multiple build workers is fairly simple, but does require some setup:

1. Ensure the settings in autobuilder.conf are valid for each buildworker, As certain variables are set within this file that are work with the local configuruation on each builder.
2. Within yocto-controller/controller.cfg add your worker to the c['workers'] list inside of the BUILDWORKERS section
3. For each build worker change the WORKER SETTINGS section of yocto-worker/buildbot.tac to match the settings in controller.cfg.

### Setting up build history

Build History is used to track changes to packages and images. By default
the autobuilder does not collect build history. The production autobuilder
does have this functionality enabled.

Setting up build history requires the following steps:

1. Create an empty git repo. Make a single commit to it and the create and push branches for each of the nightly core architectures (ie. mips, ppc, x86...)
2. Find a central location to create a clone for this. This works best if you have a set up similar to the production autobuilder (NAS with many builders)
3. Run the following:

        # This is an example of how to set up a local build history checkout. Paths
        # obviously are situation dependant.
        mkdir /nas/buildhistory
        cd /nas/buildhistory
        git clone ssh://git@git.myproject.org/buildhistory
        git clone ssh://git@git.myproject.org/buildhistory nightly-arm
        git clone ssh://git@git.myproject.org/buildhistory nightly-x86
        git clone ssh://git@git.myproject.org/buildhistory nightly-x86-64
        git clone ssh://git@git.myproject.org/buildhistory nightly-ppc
        git clone ssh://git@git.myproject.org/buildhistory nightly-mips
        for x in `ls|grep nightly` do cd $x; git checkout $x; cd /nas/buildhistory; done

4. Within the autobuilder.conf of EACH slave change the following:

        BUILD_HISTORY_COLLECT = True
        BUILD_HISTORY_DIR = "/nas/buildhistory"
        BUILD_HISTORY_REPO = "ssh://git@git.myproject.org/buildhistory"

## Configuration

In the bad old days, the yocto-autobuilder configuration was stored in a single file. This file contained both build target definitions as well as helper code / custom buildsteps. This was obviously a "bad thing". We've now removed all build target configuration out into the config/* directory

### Files used for Yocto-Autobuilder Configuration

There are two needed files in this directory. One file, autobuilder.conf, is a global definition file which sets various globals that slaves and master need to know about. This hasn't really changed from prior versions.

One new file is yoctoAB.conf. This is the only required file needed for build target definitions. However, as it would be a bad practice to have all build targets within a single file, you may define build targets in other *.conf files.

As long as those conf files live within the config directory, the yocto-autobuilder will automatically load them. This allows us to keep things nice and neat.

### config/autobuilder.conf

Used to set autobuilder wide parameters, like where various build artifacts are published to, DL_DIR, SSTATE_DIR or if build artifacts should be published (needed for production autobuilders, not needed for desktop builders)

### buildset-config.*/yoctoAB.conf

This is the main yocto autobuilder config. Documentation for this and associated. Format is in README_CONFIG (THIS IS A LIE!)

The main BuildSets section required for the configuration contains a single property:

[BuildSets]
order: ['nightly', 'nightly-x86']

The order property tells buildbot what order you wish to display build targets in on the waterfall page. This can not be used with vanilla buildbot as there is a small patch required to utilize this functionality.

### buildset configuration

Each buildset must start with a section name followed by at three to four
properties:

builders: A string or list of builders used to build the buildset

repos: A list of dicts. Each item will contain a dict entry:

        'name_of_repo':
                    {'repourl':'git://path.to/git_repo',
                     'bbpriority':'1',
                     'branch':'master'}}

NOTE: bbpriority is currently not used

props: A list of dicts. This is used when you need to add properties to a
       builder. An example of this would be build-appliance which needs to have
       a buildappsrcrev property passed so it knows which version from the poky
       repo to pull. prop_type is basically buildbot scheduler properties with
       the args sent as dict pairs. See:
       http://buildbot.net/buildbot/docs/0.8.6/manual/cfg-schedulers.html#forcesched-parameters

steps: A list of dicts. These steps can be either custom buildsteps or basic
       buildbot buildsteps with args passed as dict pairs. Custom buildsteps
       that we utilize are in lib/python2.7/site-packages/autobuilder/buildsteps.

       CreateBBLayersConf: This build step creates the bblayers.conf used by the
       build system to determine which layers to use and where to find them.

          {'CreateBBLayersConf': {'buildprovider' : 'yocto',
            'bsplayer':'True',
            'bspprovider':'intel',
            'bbtextprepend':'text_to_prepend',
            'bbtextappend':'text_to_append',
            'layerdirs': ['layerdir1', 'layerdir2', ...]}}

          buildprovider: Optional and defaults to 'yocto'.  If this is set to
          'yocto', then it adds the layers' 'meta', 'meta-yocto' and
          'meta-yocto-bsp' to BBLAYERS. If set to 'oe', then only 'meta' is
          added to BBLAYERS.

          bsplayer: Optional and defaults to False.  Set this to 'True' if you
          want to use an established BSP layer and include its default layers.

          bspprovider: Required if bsplayer is set to True.  Defines the BSP
          provider so the default layers can be included.  At this time only
          'intel', 'fsl-ppc' and 'fsl-arm' are recognized.

          bbtextprepend: Prepends the given text to bblayers.conf.  Use \n in
          the text to start a new line and always end the text with a \n.  For
          example:
              'bbtextprepend': '#Adding one comment line\n#Adding a second comment line\n'

          bbtextappend: Appends the given text to bblayers.conf.  Same format
          as bbtextprepend.

          layerdirs: Used to add layers to BBLAYERS.  Layers are added in the
          order specified and are added after the layers created by the
          buildprovider.  For example:
              'layerdirs': ['meta-openembedded/meta-oe',
                  'meta-openembedded/meta-networking',
                  'meta-openembedded/meta-gnome']
          will append the layers meta-openembedded/meta-oe,
          meta-openembedded/meta-networking, and meta-openembedded/meta-gnome
          to BBLAYERS.  Note that this will override any default layers from a
          bspprovider.

scheduler: A list of dicts. Each item defines a scheduler associated with this
       buildset:

       'name_of_scheduler':
                 {'type': 'Nightly'}

       The scheduler type is specified by the 'type' property, where supported
       values are 'Nightly' or 'SingleBranchScheduler', with 'Nightly' as the
       default. Additional properties are used to configure the scheduler and
       are type-specific:

          Nightly scheduler properties:
               month: The month in which to start the build, with January = 1.
                    This defaults to '*', meaning every month.
               dayOfWeek: The day of the week in which to start the build, with
                    Monday = 1.  This defaults to '*', meaning every day.
           hour: The hour of the day in which to start the build, with
                    12:00 AM = 0.  This must be set by the user.
           minute: The minute of the hour in which to start the build, with
                    0 to 59 as valid values.  This must be set by the user.

      SingleBranchScheduler properties:
           repository: the repository to attach the scheduler to; this
                is the repo name from the 'repos' section; the branch which
                the scheduler is attached to matches that in the repo
                definition.

           stable-timer: how long (in seconds) to wait after change before
                triggering build to allow for changes to settle.

           change-user: the user name which the remote hook will use; the
                    default value is the repository name as per the 'repository' property.

           change-password: password which the remote hook will use; the
                default is the buildbot default 'changepw' -- if your
                autobuilder is publically accessible, you want to keep this
                secret to avoid injection of arbitrary changes into your
                autobuilder.

### Extra Notes on SingleBranchScheduler setup

There is one SBS scheduler for each repository in the buildset, i.e.,
if your buildset contains more repositories, and you want build
triggered by changes to any of them, you need to define a scheduler
for each. This also means that you can mix and match, e.g., only
do nightly rebuilds for some repos and immediate for others.

The scheduler change filter is set up to watch changes only in the
single repository specified, so you have to set up your repository
hook to sent the repository url in the change set with the
--repository argument to git_buildbot.py, e.g., your git post-receive
hook could look something like:

    #!/bin/sh
    echo "$1 $2 $3" | \
        git_buildbot.py --repository="git://some_repo..."

For local testing, you can use a post-merge hook instead, along these lines:

    #!/bin/sh
    PRE=$(git rev-parse 'HEAD@{1}')
    POST=$(git rev-parse HEAD)
    SYMNAME=$(git rev-parse --symbolic-full-name HEAD)
    echo "$PRE $POST $SYMNAME" | \
        git_buildbot.py --repository="file:///where_your_repo_is"

Because of the way builbot change sources work, your change user names must not colide with the user names used by your workers.

Example:

    [nightly-x86]
    builders: 'builder1'
    repos: [{'poky':
            {'repourl':'git://git.yoctoproject.org/poky',
                 'bbpriority':'1',
                 'branch':'master'}},
            {'meta-qt3':
                {'repourl':'git://git.yoctoproject.org/meta-qt3',
                 'bbpriority':'2',
                 'branch':'master'}}]
    steps: [{'SetDest':{}},
            {'CheckOutLayers': {}},
            {'RunPreamble': {}},
            {'CreateAutoConf': {'machine': 'qemux86', 'SDKMACHINE' : 'i686',
                                'distro': 'poky'}},
            {'CreateBBLayersConf': {'buildprovider' : 'yocto'}},
            {'BuildImages': {'images': 'core-image-sato core-image-sato-dev'}},
            {'RunSanityTests': {'images': 'core-image-minimal core-image-sato'}},
            {'PublishArtifacts': {'artifacts': ['qemux86', 'atom-pc']}}]
    scheduler: [{'dev-branch-scheduler' :
                    {'type':'SingleBranchScheduler',
             'repository':'poky',
             'stable-timer':30,
                     'change-password':'secret_change_password'}}]

### Adding Buildsteps

I've included the basic buildsteps required to do general building as well as an example buildstep called HelloWorld.py.

    from buildbot.steps.shell import ShellCommand

    class HelloWorld(ShellCommand):
        haltOnFailure = True
        flunkOnFailure = True
        name = "Hello World"
        def __init__(self, factory, argdict=None, **kwargs):
            self.firstname=""
            self.lastname=""
            self.factory = factory
            for k, v in argdict.iteritems():
                if k=="name":
                    self.firstname=v
                elif k=="lastname":
                    self.lastname=v
                else:
                    setattr(self, k, v)
            self.description = "Hello World"
            self.command = "echo 'Hello World " + self.firstname + " " + self.lastname + "'"
            ShellCommand.__init__(self, **kwargs)

        def describe(self, done=False):
            description = ShellCommand.describe(self,done)
            return description

We see that this is an inherited class (from ShellCommand) that overrides the \_\_init\_\_ and describe methods of ShellCommand. All custom buildsteps MUST override \_\_init\_\_ of the inherited class, adding the argdict and kwargs properties to the class. This allows us to pass arguments specific to the custom buildstep in via an argument dictionary while allowing us to pass arguments in that will get passed up to the inherited class as a keyworded, variable length argument list.

We do this so that adding buildsteps is essentially drag and drop. By adding a custom buildstep to [lib/python2.7/site-packages/autobuilder/buildsteps](http://git.yoctoproject.org/cgit/cgit.cgi/yocto-autobuilder/tree/lib/python2.7/site-packages/autobuilder/buildsteps) you can just reference it within your config file without making any changes to the core Autobuilder codebase.
