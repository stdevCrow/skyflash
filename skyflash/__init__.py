# part of skyflash

import os
import sys
import shutil
import time
from glob import glob

module_dir = os.path.dirname(sys.modules["skyflash"].__file__)
__all__ = []
for i in sorted(glob(os.path.join(module_dir, "*.py"))):
    name = os.path.basename(i)[:-3]
    if not name.startswith("__"):
        __all__.append(name)

# Version
name = "skyflash"

# GUI imports
from PyQt5.QtGui import QGuiApplication, QIcon
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QFileInfo

# local imports
from skyflash.skyflash import Skyflash
from skyflash.utils import *

def app():
    '''Run the app'''

    try:
        # app instance
        skyflash = Skyflash()

        # GUI app
        app = QGuiApplication(sys.argv)
        if getattr( sys, 'frozen', False ) :
            # running in a pyinstaller bundle
            appFolder = sys._MEIPASS
            print("NOTICE! running from a pyinstaller bundle")
        else :
            # running live
            appFolder = QFileInfo(__file__).path()

        print("App run folder is: {}".format(appFolder))

        # app icon
        iconPath = os.path.join(appFolder, 'skyflash.png')
        iconPathData = os.path.join(appFolder, "data" + os.sep + "skyflash.png")
        if os.path.exists(iconPath):
            # default path
            print("Found Icon file in: {}".format(iconPath))
            app.setWindowIcon(QIcon(iconPath))
        elif os.path.exists(iconPathData):
            # data folder for source runs
            print("Found Icon file in: {}".format(iconPathData))
            app.setWindowIcon(QIcon(iconPathData))
        else:
            print("Can not find the icon of the app.")

        # main workspace, skyflash object
        path, download, checked = setPath("Skyflash")
        skyflash.localPath = path
        skyflash.localPathDownloads = download
        skyflash.checked = checked

        # init the logging.
        skyflash.logStart()

        # startting the UI engine
        engine = QQmlApplicationEngine()
        engine.rootContext().setContextProperty("skf", skyflash)

        # Conditional QML file loading
        localQMLdata = os.path.join(appFolder, "data" + os.sep + "skyflash.qml")
        localQMLfile = os.path.join(appFolder, "skyflash.qml")
        installedQML = "/usr/share/skyflash/skyflash.qml"
        if os.path.exists(localQMLdata):
            # local qml file in data folder
            print("Found QML file in: {}".format(localQMLdata))
            engine.load(localQMLdata)
        elif os.path.exists(localQMLfile):
            # qml file in app path folder
            print("Found QML file in: {}".format(localQMLfile))
            engine.load(localQMLfile)
        else:
            # other locations by OS
            if sys.platform.startswith('linux'):
                # first locally, then on deb install path
                if os.path.exists(installedQML):
                    # the one installed by the .deb package
                    print("Found QML file in: {}".format(installedQML))
                    engine.load(installedQML)
                else:
                    # cant find the QML file
                    print("Crap! I'm unable to find a file I need to render the user interface, exiting")
                    sys.exit(-1)
            else:
                    # cant find the QML file
                    print("Crap! I'm unable to find a file I need to render the user interface, exiting")
                    sys.exit(-1)

        # connect the engine
        engine.quit.connect(app.quit)

        # check to see if we can load a previous downloaded & tested image
        skyflash.loadPrevious()

        # main GUI call
        sys.exit(app.exec_())
    except SystemExit:
        skyflash.timerStop()
        sys.exit("By, see you soon.")
    except:
        skyflash.timerStop()
        print("Unexpected error:", sys.exc_info()[0])
        raise
        sys.exit(-1)
