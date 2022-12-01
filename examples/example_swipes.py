import time

from touch_input import TouchManager

# https://naqtn.github.io/WBBMTT/touch-tester.html?markSizeScale=1.0&backGroundColor=black
touch_nums = 3
touch_interface = TouchManager(touch_nums, visuals_enable=True, auto_update=False)

for x in range(touch_nums):
    touch_interface[x].press_down((300, 450 + 50 * x))
touch_interface.update()

time.sleep(.2)
for x in range(touch_nums):
    touch_interface[x].pull_up()
touch_interface.update()
time.sleep(.2)
for x in range(touch_nums):
    touch_interface[x].press_down((300, 450 + 50 * x))
touch_interface.update()
time.sleep(.2)

touch_interface.update()
time.sleep(.2)
touch_interface[0].pull_up()
touch_interface.update()
time.sleep(.2)

for tick in range(20):
    for x in range(1, touch_nums):
        touch_interface[x].swipe((300 + tick * 10, 450 + 50*x), shake_y=3)
    touch_interface.update()
    time.sleep(0.02)

touch_interface[0].press_down((300, 450))
touch_interface.update()
time.sleep(.2)
for tick in range(20):
    touch_interface[0].swipe((300, 450 + tick * 10))
    touch_interface.update()
    time.sleep(0.02)

touch_interface[1].pull_up()
touch_interface[2].pull_up()
touch_interface.update()
