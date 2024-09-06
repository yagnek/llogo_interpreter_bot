start_msg = (
    "Hi! I'm a chat bot that can interpret a Turing-complete Logo-like "
    "programming language. Logo is a programming language designed in 1967 "
    "to help kids learn programming. It is famous for the turtle graphics. "
    "I can interpret the most essential commands of this language. Note "
    "that I only work with numeric types, and each message you send me is "
    "a separate program. To see the list of available procedures, run /help"
)

help_msg = (
    "Currently, these procedures are implemented. To learn more about a "
    "procedure, run its name as a chat bot command:\n"
    "/forward\n"
    "/backward\n"
    "/right\n"
    "/left\n"
    "/penup\n"
    "/pendown\n"
    "/repeat\n"
    "/make\n"
    "/to\n"
    "/clean\n"
    "/home\n"
    "/clearscreen\n"
    "/hideturtle\n"
    "/showturtle\n"
    "/setheading\n"
    "/print"
)

forward_msg = (
    "forward *distance* \n\n"
    "Moves the turtle forward *distance* steps. The *distance* argument "
    "can be a number, a variable, or a simple arithmetic expression. \n\n"
    "Aliases: fd \n\n"
    "Example: forward 360 / 5"
)

backward_msg = (
    "backward *distance* \n\n"
    "Moves the turtle backward *distance* steps. The *distance* argument "
    "can be a number, a variable, or a simple arithmetic expression. \n\n"
    "Aliases: back, bk \n\n"
    "Example: backward 50"
)

right_msg = (
    "right *angle* \n\n"
    "Turns the turtle right *angle* degrees. The *angle* argument can be "
    "a number, a variable, or a simple arithmetic expression. \n\n"
    "Aliases: rt \n\n"
    "Example: right 90"
)

left_msg = (
    "left *angle* \n\n"
    "Turns the turtle left *angle* degrees. The *angle* argument can be "
    "a number, a variable, or a simple arithmetic expression. \n\n"
    "Aliases: lt \n\n"
    "Example: left 120"
)

penup_msg = (
    "penup \n\n"
    "Lifts the pen up, so the turtle does not draw a line when it moves. \n\n"
    "Aliases: pu"
)

pendown_msg = (
    "pendown \n\n"
    "Puts the pen down, so the turtle draws a line when it moves. \n\n"
    "Aliases: pd"
)

repeat_msg = (
    "repeat *times* [*procedures*] \n\n"
    "Repeats the specified procedures the specified number of times. "
    "Nested repeats are also allowed. \n\n"
    "Aliases: rp \n\n"
    "Example: repeat 20 [repeat 360 [forward 1.6 right 1] right 18]"
)

make_msg = (
    'make "*name* *value* \n\n'
    "Creates a variable and assigns a value to it. The value can be a "
    "number, a variable, or a simple arithmetic expression."
    'Note that when creating a variable, its name must be prefixed with ", '
    "and when the variable is used, its name must be prefixed with :. \n\n"
    "Aliases: mk \n\n"
    'Example: \nmake "x 360 / 7 \nright :x'
)

to_msg = (
    "to *name* *:argument_names* *procedures* end \n\n"
    "Creates a custom function. A custom function can take any specified "
    "number of arguments. Argument names must be prefixed by : when "
    "defining the function. When calling a custom function, the argument " 
    "values may be a number or a variable, but not an expression. " 
    "Also, after the function is called, the passed argument values "
    "cannot be modified. However, they can be assigned to a variable "
    "that can be modified inside the function."
    "Nested function definitions are NOT allowed, but a function can call "
    "other functions. Note that the function definition must end with the "
    "'end' keyword.\n\n"
    "Example:\n to square :side repeat 4 [forward :side right 90] end\n "
    "square 42"
)

clean_msg = "clean \n\n Cleans the screen."

home_msg = "home \n\n Moves the turtle to the center of the field."

clearscreen_msg = "clearscreen \n\n Moves the turtle to the center of the field and cleans the screen."

hideturtle_msg = (
    "hideturtle \n\n"
    "Makes the turtle invisible. \n\n Aliases: ht"
)

showturtle_msg = (
    "showturtle \n\n"
    "Makes the turtle visible. \n\n Aliases: st"
)

setheading_msg = (
    "setheading *angle* \n\n"
    "Makes the turtle face the direction specified by the *angle* "
    "argument. The argument can be a number, a variable, or a simple "
    "arithmetic expression. \n\n"
    "Aliases: seth \n\n"
    "Example: seth 260"
)

print_msg = (
    "print *argument*\n\n"
    "Prints the argument, which can be a number, a variable, or a simple "
    "arithmetic expression. \n\n"
    "Aliases: pr \n\n"
    "Example: print 99 * 77 + 123"
)
