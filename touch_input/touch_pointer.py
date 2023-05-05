import random
from enum import Enum
from time import sleep
from typing import TYPE_CHECKING

from .touch_ctypes_constants import *

if TYPE_CHECKING:
    from .touch_manager import TouchManager


class PointerStatus(Enum):
    UP = 1
    PRESSED = 2
    SWIPE = 3


class TouchPointer:
    def __init__(self, id, interface: 'TouchManager'):
        self.id = id
        self.touch_info = PointerTouchInfo()
        self.set_pointer_settings(self.id, self.touch_info)
        self.need_update = False
        self.interface = interface
        self.status = PointerStatus.UP
        self.shake = False

    def get_status(self):
        """Get status of current pointer"""
        x, y = self.get_position()
        return self.id, self.status, x, y

    def get_position(self):
        return (self.touch_info.pointerInfo.ptPixelLocation.x,
                self.touch_info.pointerInfo.ptPixelLocation.y)

    def _auto_update(self):
        if self.interface.auto_update:
            self.interface._update_all_pointers()

    @staticmethod
    def set_pointer_settings(id, tifno):
        tifno.pointerInfo.pointerType = PT_TOUCH
        tifno.pointerInfo.pointerId = id
        tifno.pointerInfo.ptPixelLocation.y = 1000
        tifno.pointerInfo.ptPixelLocation.x = 500

        tifno.touchFlags = TOUCH_FLAG_NONE
        tifno.touchMask = TOUCH_MASK_ALL
        tifno.orientation = 90
        tifno.pressure = 32000
        tifno.rcContact.top = tifno.pointerInfo.ptPixelLocation.y - 2
        tifno.rcContact.bottom = tifno.pointerInfo.ptPixelLocation.y + 2
        tifno.rcContact.left = tifno.pointerInfo.ptPixelLocation.x - 2
        tifno.rcContact.right = tifno.pointerInfo.ptPixelLocation.x + 2

        tifno.pointerInfo.pointerFlags = POINTER_FLAG_NONE

    def _set_position(self, pos: (int, int), finger_radius=5, random_offset=0):
        x, y = int(pos[0]), int(pos[1])
        if random_offset:
            x = x + random.randint(-random_offset, random_offset)
            y = y + random.randint(-random_offset, random_offset)

        self.touch_info.pointerInfo.ptPixelLocation.x = x
        self.touch_info.pointerInfo.ptPixelLocation.y = y

        self.touch_info.rcContact.left = x - finger_radius
        self.touch_info.rcContact.right = x + finger_radius
        self.touch_info.rcContact.top = y - finger_radius
        self.touch_info.rcContact.bottom = y + finger_radius

    def press_down(self, pos: (int, int), finger_radius=5, random_offset=0):
        if self.status in [self.status.PRESSED, self.status.SWIPE]:
            print('pointer already Pressed')
            return

        # print('pressed down', self.id, 'pressed down')
        self._set_position(pos, finger_radius, random_offset)

        self.touch_info.pointerInfo.pointerFlags = (POINTER_FLAG_DOWN |
                                                    POINTER_FLAG_INRANGE |
                                                    POINTER_FLAG_INCONTACT)

        self.status = PointerStatus.PRESSED
        self.need_update = True
        self._auto_update()

    def swipe(self, pos: (int, int), finger_radius=5, random_offset=0, shake_x=0, shake_y=0):
        if self.status in [self.status.PRESSED, self.status.SWIPE]:
            self.touch_info.pointerInfo.pointerFlags = (POINTER_FLAG_INRANGE |
                                                        POINTER_FLAG_INCONTACT |
                                                        POINTER_FLAG_UPDATE)
        else:
            self.touch_info.pointerInfo.pointerFlags = (POINTER_FLAG_DOWN |
                                                        POINTER_FLAG_INRANGE |
                                                        POINTER_FLAG_INCONTACT)
        x, y = pos
        if shake_x or shake_y:
            self._set_position((x + (-shake_x if self.shake else shake_x),
                                y + (-shake_y if self.shake else shake_y)),
                               finger_radius,
                               random_offset)
            self.shake = not self.shake
        else:
            self._set_position((x, y), finger_radius, random_offset)

        self.status = PointerStatus.SWIPE
        self.need_update = True
        self._auto_update()

    def pull_up(self):
        if self.status == self.status.UP:
            print('pointer already Up')
            return

        self.touch_info.pointerInfo.pointerFlags = POINTER_FLAG_UP
        self.status = PointerStatus.UP
        self.need_update = False
        self._auto_update()

    @staticmethod
    def _lerp(a: float, b: float, t: float) -> float:
        return (1 - t) * a + t * b

    def _lerp2D(self, point1: (int, int), point2: (int, int), t: float):
        return self._lerp(point1[0], point2[0], t), self._lerp(point1[1], point2[1], t)

    def action_swipe(self, start: (int, int), finish: (int, int), duration=1, tick=60,
                     random_offset=0, shake_x=0, shake_y=0):
        """
        Animated swipe action
        """
        steps = tick * duration
        wait = duration / steps
        for x in range(1, steps + 1):
            t = x / steps
            point = self._lerp2D(start, finish, t)
            x, y = int(point[0]), int(point[1])
            self.swipe((x, y), random_offset=random_offset,
                       shake_x=shake_x, shake_y=shake_y)
            self.interface._update_all_pointers()
            sleep(wait)
        self.pull_up()
        self.interface._update_all_pointers()

    def action_press(self, point: (int, int), hold_time: float = 0.5, random_offset=0):
        """
        Simple touch press
        hold_time > 0.5 may cause errors
        """
        hold_time = min(hold_time, 0.5)
        self.press_down(point, random_offset=random_offset)
        self.interface._update_all_pointers()
        sleep(hold_time)
        self.pull_up()
        self.interface._update_all_pointers()
