       
init python:
    
    def create_button_pattern(difficulty):
        pattern = []
        if difficulty == "easy":
            for i in range(4):
                pattern.append(renpy.random.randint(0, 3))
        elif difficulty == "medium":
            for i in range(6):
                pattern.append(renpy.random.randint(0, 3))
        elif difficulty == "hard":
            for i in range(8):
                pattern.append(renpy.random.randint(0, 3))
                
        return pattern

    def set_difficulty(button):
        global current_difficulty 
        current_difficulty = "easy"
        difficulties = ["easy", "medium", "hard"]
        current_index = difficulties.index(current_difficulty)
        if button == "right" and current_index < len(difficulties) - 1:
            current_difficulty = difficulties[current_index + 1]
        elif button == "left" and current_index > 0:
            current_difficulty = difficulties[current_index - 1]  
    renpy.restart_interaction()


    def light_buttons():
        global current_button_index, input_ready
        global red_button_lit, blue_button_lit, green_button_lit, yellow_button_lit

        if current_button_index < len(current_button_pattern):
            button_lit = current_button_pattern[current_button_index]
            if button_lit == "red":
                red_button_lit = True
            elif button_lit == "blue":
                blue_button_lit = True
            elif button_lit == "green":
                green_button_lit = True
            elif button_lit == "yellow":
                yellow_button_lit = True

            current_button_index += 1
            renpy.restart_interaction()
        else:
            input_ready = True
            renpy.restart_interaction()

    def off_buttons():
        global red_button_lit
        global blue_button_lit
        global green_button_lit
        global yellow_button_lit
    
        red_button_lit = False
        blue_button_lit = False
        green_button_lit = False
        yellow_button_lit = False

    def check_user_input(button):
        global selected_button_index, input_ready, correct_picks, user_picks
        if buttons.index(button) == current_button_pattern[selected_button_index]:
            correct_picks += 1
            user_picks += 1
            if current_button_index == user_picks:
                selected_button_index = user_picks = current_button_index = 0
                input_ready = False
        else:
            selected_button_index += 1
            renpy.restart_interaction()
            renpy.show_screen("game_over")
            renpy.hide_screen("simondice")
        if correct_picks == len(current_button_pattern):
            renpy.show_screen("simondice_menu")
            renpy.transitions(fade(1,0,1))
            renpy.hide_screen("simondice")


    def reset_simon_dice():
        global current_button_index
        global selected_button_index
        global input_ready
        global correct_picks
        global user_picks
        global current_button_pattern
        global red_button_lit, blue_button_lit, yellow_button_lit, green_button_lit

        current_button_index = 0
        selected_button_index = 0
        correct_picks = 0
        user_picks = 0
        input_ready = False

        red_button_lit = False
        blue_button_lit = False
        green_button_lit = False
        yellow_button_lit = False

        current_difficulty = "easy"  # Asignar un valor a current_difficulty
        current_button_pattern = create_button_pattern(current_difficulty)

    renpy.restart_interaction()

transform half_size:
    zoom 0.5

screen game_over:
    image "background.png" at half_size
    frame:
        background "black"
        xfill True
        yfill True
        frame:
            background None
            xysize (int(1548 / 2), int(941 / 2))
            align (0.5, 0.5)
            image "UI/menu-background-game-over.png" at half_size
            text "¡Mi niño, lo hiciste mal..." size 30 color "#FFFFFF" outlines [(absolute(2), "#000000", 0, 0)] align (0.5, 0.45)
            imagebutton idle "UI/try-again-button.png" action [Hide("game_over"), Show("simondice_menu")] align (0.3, 0.8) at half_size
            imagebutton idle "UI/quit-button.png" action [Hide("game_over"), Show("main_menu")] align (0.8, 0.8) at half_size
  
            
screen simondice:
    on "show" action Function(reset_simon_dice)
    image "background.png"
    if red_button_lit:
        imagebutton idle "red-button-lit.png" pos(0.15, 0.65) at half_size
    elif not (red_button_lit):
        imagebutton auto "red-button-%s.png" pos(0.15, 0.65) action [SetVariable("red_button_lit", True), Function(check_user_input, button = "red")] sensitive input_ready at half_size
    if blue_button_lit:
        imagebutton idle "blue-button-lit.png" pos(0.35, 0.52) at half_size
    elif not (blue_button_lit):
        imagebutton auto "blue-button-%s.png" pos(0.35, 0.52) action [SetVariable("blue_button_lit", True), Function(check_user_input, button = "blue")] sensitive input_ready at half_size
    if green_button_lit:
        imagebutton idle "green-button-lit.png" pos(0.65, 0.52) at half_size
    elif not (green_button_lit):
        imagebutton auto "green-button-%s.png" pos(0.65, 0.52) action [SetVariable("green_button_lit", True), Function(check_user_input, button = "green")] sensitive input_ready at half_size
    if yellow_button_lit:
        imagebutton idle "yellow-button-lit.png" pos(0.88, 0.65) at half_size
    elif not (yellow_button_lit):
        imagebutton auto "yellow-button-%s.png" pos(0.88, 0.65) action [SetVariable("yellow_button_lit", True), Function(check_user_input, button = "yellow")] sensitive input_ready at half_size

    if not input_ready:
        timer 1.0 action Function(light_buttons) repeat True
    else:
        #block of code to run:
        timer 0.5 action Function(off_buttons) repeat True

screen simondice_menu:
    modal True
    image "background.png"
    frame:
        background "#ff4f9857"
        xfill True
        yfill True
        frame:
            background Frame("UI/menu-background.png")
            xysize(int(1548 / 2),int(941 / 2))
            align(0.5, 0.5)
            text "Difficulty: [current_difficulty]" size 30 color "#FFFFFF" outlines[(absolute(2), "#000000", 0, 0 )] align(0.5, 0.45)
        imagebutton idle "UI/arrow-left.png" align(0.35, 0.46) action Function(set_difficulty, button = "left") at half_size
        imagebutton idle "UI/arrow-right.png" align(0.65, 0.46) action Function(set_difficulty, button = "right") at half_size
        imagebutton idle "UI/play-button.png" align(0.40, 0.60) action [Hide("simondice_menu"), Show("simondice")] at half_size
        imagebutton idle "UI/quit-button.png" align(0.60, 0.60) action NullAction at half_size
    timer 0.5 action Function(light_buttons) repeat True

label start:
    $ button_pattern_easy = create_button_pattern("easy")
    $ button_pattern_medium = create_button_pattern("medium")
    $ button_pattern_hard = create_button_pattern("hard")
    $ current_button_pattern = button_pattern_easy
    $ difficulties = ["easy", "medium", "hard"]
    $ current_difficulty = "easy"
    $ red_button_lit = False
    $ green_button_lit = False
    $ yellow_button_lit = False
    $ blue_button_lit = False
    $ buttons = ("red", "blue", "green", "yellow")
    $ current_button_index = 0
    $ input_ready = 0
    $ correct_picks = 0
    $ user_picks = 0
    $ selected_button_index = 0
    call screen simondice_menu
    return

