from sheets import SheetManager

#############################################################
# Declare all globals, and try to connect the google sheets #
# Also places the sheets in accessible global arrays        #
#############################################################


def init():
    global rfid, sheets, app
    sheets = SheetManager()


def setRFID(new_rfid):
    global rfid
    rfid = new_rfid


def setApp(new_app):
    global app
    app = new_app
