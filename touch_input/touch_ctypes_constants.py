from ctypes import *
from ctypes.wintypes import *

# Constants

# For touchMask
TOUCH_MASK_NONE = 0x00000000  # Default
TOUCH_MASK_CONTACTAREA = 0x00000001
TOUCH_MASK_ORIENTATION = 0x00000002
TOUCH_MASK_PRESSURE = 0x00000004
TOUCH_MASK_ALL = 0x00000007

# For touchFlag
TOUCH_FLAG_NONE = 0x00000000

# For pointerType
PT_POINTER = 0x00000001  # All
PT_TOUCH = 0x00000002
PT_PEN = 0x00000003
PT_MOUSE = 0x00000004

# For pointerFlags
POINTER_FLAG_NONE = 0x00000000  # Default
POINTER_FLAG_NEW = 0x00000001
POINTER_FLAG_INRANGE = 0x00000002
POINTER_FLAG_INCONTACT = 0x00000004
POINTER_FLAG_FIRSTBUTTON = 0x00000010
POINTER_FLAG_SECONDBUTTON = 0x00000020
POINTER_FLAG_THIRDBUTTON = 0x00000040
POINTER_FLAG_FOURTHBUTTON = 0x00000080
POINTER_FLAG_FIFTHBUTTON = 0x00000100
POINTER_FLAG_PRIMARY = 0x00002000
POINTER_FLAG_CONFIDENCE = 0x00004000
POINTER_FLAG_CANCELED = 0x00008000
POINTER_FLAG_DOWN = 0x00010000
POINTER_FLAG_UPDATE = 0x00020000
POINTER_FLAG_UP = 0x00040000
POINTER_FLAG_WHEEL = 0x00080000
POINTER_FLAG_HWHEEL = 0x00100000
POINTER_FLAG_CAPTURECHANGED = 0x00200000


# Structs Needed

class PointerInfo(Structure):
    _fields_ = [("pointerType", c_uint32),
                ("pointerId", c_uint32),
                ("frameId", c_uint32),
                ("pointerFlags", c_int),
                ("sourceDevice", HANDLE),
                ("hwndTarget", HWND),
                ("ptPixelLocation", POINT),
                ("ptHimetricLocation", POINT),
                ("ptPixelLocationRaw", POINT),
                ("ptHimetricLocationRaw", POINT),
                ("dwTime", DWORD),
                ("historyCount", c_uint32),
                ("inputData", c_int32),
                ("dwKeyStates", DWORD),
                ("PerformanceCount", c_uint64),
                ("ButtonChangeType", c_int)
                ]


class PointerTouchInfo(Structure):
    _fields_ = [("pointerInfo", PointerInfo),
                ("touchFlags", c_int),
                ("touchMask", c_int),
                ("rcContact", RECT),
                ("rcContactRaw", RECT),
                ("orientation", c_uint32),
                ("pressure", c_uint32)]