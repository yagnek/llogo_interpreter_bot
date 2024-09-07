from PIL import ImageDraw
from copy import copy
import re

from scene import Field, Turtle

class Interpreter():

    def __init__(self, field, turtle):
        self.field = field
        self.turtle = turtle

        self.text_output = ""
        self.error_output = ""
        self.img_out = False


        self.operands = ('+', '-', '*', '/', '>', '<', '=')
        
        self.keywords = {
            'no_args' : {
                'penup'         : self.turtle.penup,
                'pu'            : self.turtle.penup,
                'pendown'       : self.turtle.pendown,
                'pd'            : self.turtle.pendown,
                'hideturtle'    : self.turtle.hideturtle,
                'ht'            : self.turtle.hideturtle,
                'showturtle'    : self.turtle.showturtle,
                'st'            : self.turtle.showturtle,
                'home'          : self.turtle.home,
                'clean'         : self.field.clean,
                'clearscreen'   : self.turtle.clearscreen,
                'cs'            : self.turtle.clearscreen,
            },
            'one_arg' : {
                'forward'       : self.turtle.forward,
                'fd'            : self.turtle.forward,
                'backward'      : self.turtle.backward,
                'back'          : self.turtle.backward,
                'bk'            : self.turtle.backward,
                'left'          : self.turtle.left,
                'lt'            : self.turtle.left,
                'right'         : self.turtle.right,
                'rt'            : self.turtle.right,
                'setheading'    : self.turtle.setheading,
                'seth'          : self.turtle.setheading,

             }
        }

        self.special_cases = {
            "repeat", "rp", "if", "make", "mk", "to", "end", "print", "pr"
        }

        self.mem = {}
        self.local_mem = {}

    def parse(self, line):
        line = line.replace('+', ' + ').replace('-', ' - ').replace('*', ' * ').replace('/', ' / ')
        line = line.replace('>', ' > ').replace('<', ' < ')
        return line        

    def tokenize(self, line):
        line = line.replace("[", "[ ").replace("]", " ]").split()
        string = str(line).replace("'[',", "[").replace("', ']'", "' ]").replace(", ']'", ", ]")
        tokens = eval(string)
        return tokens
    
    def matches(self, pattern, string):
        match = re.match(pattern, string)
        if match != None:
            return True
        else:
            return False

    def is_num(self, token):
        pattern = r"^[+-]?\d+\.?\d*$"
        return self.matches(pattern, token)

    
    def calculate(self, tokens):
        ls = []
        for i in range(len(tokens)):
            if type(tokens[i]) == str:
                if self.is_num(tokens[i]):
                    ls.append(tokens[i])
                elif tokens[i] in self.operands:
                    ls.append(tokens[i])
                elif tokens[i][0] == ':':
                        var_name = tokens[i][1:]
                        if var_name in self.mem:
                            ls.append(self.mem[var_name])
                else:
                    break
            
        string = str(ls).replace('=', ' == ').replace("'", "").replace(",", "").replace("[", "").replace("]", "")
        result = eval(string)
        jump = len(ls)
        return result, jump


    def interpret(self, tokens):

        argument = None
        procedure = None

        if type(tokens) == list:
            jump = 0
            for i in range(len(tokens)):
                if jump == 0:
                    if type(tokens[i]) == list:
                        try:
                            self.interpret(tokens[i])
                        except:
                            self.raise_error("An error accured because of: " + str((tokens[i])))
                    elif tokens[i] in self.keywords['no_args']:
                        procedure = self.keywords['no_args'][tokens[i]]
                        procedure()
                        setattr(self, 'img_out', True)
                    elif tokens[i] in self.keywords['one_arg']:
                        try:
                            procedure = self.keywords['one_arg'][tokens[i]]
                            argument, jump = self.calculate(tokens[i+1:])
                            procedure(argument)
                            setattr(self, 'img_out', True)
                        except:
                            self.raise_error("An argument is required for the function: " + tokens[i])
                    elif tokens[i] == "print" or tokens[i] == "pr":
                        try:
                            procedure = self.print_output
                            argument, jump = self.calculate(tokens[i+1:])
                            procedure(argument)
                        except:
                            self.raise_error("An argument is required for the function: " + tokens[i])
                    elif tokens[i] == "repeat" or tokens[i] == "rp":
                        try:
                            times, jump = self.calculate(tokens[i+1:])
                            if times > 0:
                                procedure = tokens[i+jump+1]
                                self.repeat(times, procedure)
                            elif times == 0:
                                jump += 2
                            else:
                                self.raise_error("The argument for REPEAT cannot be negative")
                        except:
                            self.raise_error("Incorrect format for REPEAT command")
                    elif tokens[i] == "make" or tokens[i] == "mk":
                        if tokens[i+1][0] == '"':
                            name = tokens[i+1]
                            value, jump = self.calculate(tokens[i+2:])
                            jump += 1
                            self.make(name, str(value))
                    elif tokens[i] == "if":
                        test, jump = self.calculate(tokens[i+1:])
                        if test == False:
                            jump += 1
                        elif test == True:
                            self.interpret(tokens[i+jump+1])
                            if len(tokens[i+jump:]) > 2:
                                if type(tokens[i+jump+2]) == list: 
                                    jump += 2
                            else:
                                jump += 1
                    elif tokens[i] == "to":
                        procedure_name = tokens[i+1]
                        if procedure_name not in self.keywords['no_args']\
                            and procedure_name not in self.keywords['one_arg']\
                            and procedure_name not in self.operands\
                            and procedure_name not in self.special_cases\
                            and self.is_num(procedure_name) == False:
                            definition = [] 
                            for n in range(i+1, i+1+len(tokens[i+1:])):
                                if tokens[n] != "end":
                                    definition.append(tokens[n])
                                    jump = len(definition)+1
                                else:
                                    break
                            self.new_function(definition)
                        else:
                            self.raise_error("Error: The word", procedure_name, "is reserved")
                    elif tokens[i] in self.mem:
                        procedure_name = tokens[i]
                        args, args_count = self.parse_arguments(procedure_name, tokens[i+1:])
                        self.assign_arguments(procedure_name, args)
                        procedure = self.parse(self.mem[procedure_name])
                        procedure_tokens = self.tokenize(procedure)
                        procedure_tokens = self.set_args(procedure_tokens)
                        self.interpret(procedure_tokens)
                        jump = args_count
                    else:
                        self.raise_error("Exception: " + str(tokens[i]))
                else:  
                    jump -= 1


    def repeat(self, times, procedure):
        for i in range(times-1):
            self.interpret(procedure)


    def make(self, name, value):
        name = name.replace('"', '')
        self.mem[name] = value

  
    def new_function(self, definition):
        string = str(definition[1:]).replace("'", "").replace(",", "")
        if string[0] == '[' and string[-1] == ']':
            try:
                self.mem[definition[0]] = string[1:-1]
            except:
                self.raise_error("Bad function definition: " + definition)
        else:
            self.mem[definition[0]] = string
    
    def parse_arguments(self, procedure, tokens):
        args_count = 0
        args = []
        procedure = self.mem[procedure].split()
        for i in range(len(procedure)):
            if procedure[i][0] == ':':
                args.append(tokens[i])
                args_count += 1
            else:
                break
        return args, args_count
    
    def assign_arguments(self, procedure_name, args):
        procedure = self.mem[procedure_name].split()
        for i in range(len(args)):
            self.local_mem[procedure[i][1:]] = args[i]

    def set_args(self, tokens):
        args = set()
        for i in range(len(tokens)):
            if tokens[i][0] == ':':
                if tokens[i][1:] in self.local_mem:
                    args.add(tokens[i])
                    tokens[i] = self.local_mem[tokens[i][1:]]
            elif type(tokens[i]) == list:
                self.set_args(tokens[i])
        args_count = len(args)
        return tokens[args_count:]
    
    def print_output(self, output):
        self.text_output += str(output) + "\n"

    def raise_error(self, error):
        self.error_output += str(error) + "\n"

    def render_field(self):
        out = copy(self.field.picture)
        if self.turtle.visible:
            ImageDraw.Draw(out).circle(self.turtle.pos, 7, self.turtle.color)
        #out.save("output.png")
        return(out)
        

    def interpreting_pipeline(self, line):
        setattr(self, "img_out", False)
        line = self.parse(line)
        try:
            rb = line.count('[')
            lb = line.count(']')
            image_output = None
            if '(' in line or ')' in line:
                self.raise_error("Error: Parenthesis are not supported in this implementation")
            elif rb != lb:
                self.raise_error("Error: Square brackets were not closed")
            else:
                tokens = self.tokenize(line)
                self.interpret(tokens)
                if self.img_out == True:
                    image_output = self.render_field()
            error_output = copy(self.error_output)
            text_output = copy(self.text_output)
            return image_output, error_output, text_output
        except:
            self.raise_error("Something went wrong. Please check your program.")

def new_interpreter():
    field = Field()
    turtle = Turtle(field=field, pos = [225, 200])
    interpreter = Interpreter(field=field, turtle=turtle)
    return interpreter