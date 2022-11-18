## Touch input library

Simple Python touch input package with multitouch support

### Usage:

```python
from time import sleep
from touch_input import TouchManager


# Open this link in browser. This is good for multitouch testing  
# https://naqtn.github.io/WBBMTT/touch-tester.html?markSizeScale=1.0&backGroundColor=black

# Create TouchManager object
tm = TouchManager(touch_nums=2, visuals_enable=True, auto_update=True)

# Access pointers by index
p1 = tm[0]
p2 = tm[1]

# Do something

# Press 2 pointers
p1.press_down((500, 500))
p2.press_down((600, 600))

# Holding pointers for more than 0.5 seconds without update may cause errors
sleep(0.5)

# Pull up pointers
p1.pull_up()
p2.pull_up()

# Try some simple actions
p1.action_swipe((200, 200), (400, 400), 1)
p2.action_press((300, 400))

```

For more examples check examples folder