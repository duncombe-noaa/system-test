
#system-test

A place to discuss, raise issues, and capture progress for the IOOS DMAC System Integration Test project.

* Discuss by commenting on or creating new [System-Test Issues](https://github.com/ioos/system-test/issues?direction=desc&page=1&sort=created&state=open)
* Capture plans, progress by using the [System-Test Wiki](https://github.com/ioos/system-test/wiki)
* To contribute to this repository consult [Contributing to the Project](https://github.com/ioos/system-test/wiki/Contributing-to-the-Project) in the project wiki. 


##Intended Use

The documentation developed here is intended to guide and inform on the use of Python code to access data described by the meta-data provided by  IOOS. Several test-cases are developed that demonstrate accessing and using data provided by the IOOS and Regional Associations servers. The test-cases are presented as iPython notebooks providing Python code examples and commentary guiding the use of the databases and servers. 

For a full discussion of the purpose of the system-test notebooks, see the web-pages at [System Test Wiki](https://github.com/ioos/system-test/wiki).

##How-To

The pages used to create the iPython notebooks are available on the [IOOS
github site](https://github.com/ioos/system-test). They can be `git clone`d
onto your desktop, served using `ipython notebook` and thereby browsed and
edited on your chrome or firefox browser locally. They will also be served
as iPython notebooks somewhere at the [IOOS
Website](https://IOOS.github.io) (*or another site*) from a Wakari, or
similar, server (maybe). 

##Getting Started

###Reading an IPython notebook

IPython does not need to be running to read a notebook. View the .ipynb
file in online [nbviewer](http://nbviewer.ipython.org/) or install a
browser app (search your bowser's webstore for "nbviewer"). For full
functionality and to change parameters and experiment, run `ipython
notebook`.

###Running an IPython notebook

Use your preferred python installation. We use
[Anaconda](http://docs.continuum.io/anaconda/install.html) mostly.    
- activate an appropriate environment    
    `activate glider_test`    
    Find environments available by checking in ``<anaconda install
dir>/envs``  or run ``conda info --envs``
- start the notebook server    
    `ipython notebook`    
    A browser window should open, or you can access it at the default
location ``localhost:8890``


