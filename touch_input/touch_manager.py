from .touch_pointer import *


class TouchManager:
    def __init__(self, touch_nums=1, auto_update=False, visuals_enable=False):
        self.__touch_nums = touch_nums
        self.auto_update = auto_update
        self.__visuals_enable = visuals_enable

        self.touch_inited = False
        self.__pointers: list[TouchPointer] = []
        self.pointers_status: list = [None] * touch_nums

        self.__initialize_touch_injection()
        self.__init_touch_settings()
        self.__filtered = [x.touch_info for x in self.__pointers]

    @property
    def touch_nums(self):
        return self.__touch_nums

    def __initialize_touch_injection(self):
        if not self.touch_inited:
            visuals = 1 if self.__visuals_enable else 3
            inited = windll.user32.InitializeTouchInjection(self.__touch_nums, visuals)
            if inited != 0:
                #print("Initialized Touch Injection")
                self.touch_inited = True

    def __init_touch_settings(self):
        for ind in range(self.__touch_nums):
            pointer = TouchPointer(ind, self)
            self.__pointers.append(pointer)
        self._update_all_pointers(ignore_errors=True)

    def __set_pointers_to_update(self):
        for _, x in self.get_pressed_pointers():
            x.touch_info.pointerInfo.pointerFlags = (POINTER_FLAG_INRANGE |
                                                     POINTER_FLAG_INCONTACT |
                                                     POINTER_FLAG_UPDATE)

    def __getitem__(self, item) -> TouchPointer:
        return self.__pointers[item]

    def __iter__(self):
        return self.__pointers

    def __compare_status(self, pointer_id: int):
        status = self.__pointers[pointer_id].get_status()
        comparison = self.pointers_status[pointer_id] == status
        if not comparison:
            self.pointers_status[pointer_id] = status
        return comparison

    def __get_filtered_list(self):
        filtered = []
        for ind, pointer in enumerate(self.__pointers):
            status = self.__compare_status(ind)
            if pointer.need_update or not status:
                filtered.append(pointer.touch_info)
        return filtered

    def get_pressed_pointers(self):
        return [(x.id, x) for x in self.__pointers if x.status in [PointerStatus.PRESSED, PointerStatus.SWIPE]]

    def get_upped_pointers(self):
        return [(x.id, x) for x in self.__pointers if x.status == PointerStatus.UP]

    def _update_all_pointers(self, ignore_errors=False):
        """Updating all touch pointers on screen"""

        filtered = self.__get_filtered_list()

        arr = (PointerTouchInfo * len(filtered))(*filtered)
        if arr:
            press = windll.user32.InjectTouchInput(len(arr), byref(arr))

            if press == 0 and not ignore_errors:
                print("Failed update with Error: " + FormatError())

            self.__set_pointers_to_update()

    def update(self, ignore_errors=False):
        """Calling update, if auto update is off"""
        if not self.auto_update:
            self._update_all_pointers(ignore_errors)

