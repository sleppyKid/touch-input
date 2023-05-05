from touch_input import TouchManager

# https://naqtn.github.io/WBBMTT/touch-tester.html?markSizeScale=1.0&backGroundColor=black
ti = TouchManager(touch_nums=2, visuals_enable=True)

ti[1].press_down((250, 250))
ti[0].action_swipe(start=(500, 500), finish=(300, 200), duration=1, tick=30)
ti[0].action_press(point=(600, 700), hold_time=0.5)
ti[0].action_swipe((400, 400), (900, 900))
ti[1].pull_up()
