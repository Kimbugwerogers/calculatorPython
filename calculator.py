import tkinter

button_values = [
    ['C', 'CE', '%', '√'],
    ['7', '8', '9', '/'],
    ['4', '5', '6', '*'],
    ['1', '2', '3', '-'],
    ['0', '.', '=', '+']
    ]

right_align = [ '/', '*', '-', '+', '=']
top_align = [ 'C', 'CE', '%', '√' ]

row_count = len(button_values) #5
column_count = len(button_values[0]) #4

color_light_gray = '#F0F0F0'
color_black = '#000000'
color_dark_gray = '#A9A9A9'
color_blue = '#0000FF'
color_white = '#FFFFFF'
color_orange = '#FFA500'

# Create the main window
window = tkinter.Tk() #create a window object
window.title("Calculator")
window.resizable(False, False) #make the window not resizable
window.geometry("300x400")

frame = tkinter.Frame(window) #create a frame to hold the buttons
label = tkinter.Label(frame, text="0", anchor='e', bg=color_black, 
                      fg=color_white, font=('Arial', 24), padx=10, pady=10, width=column_count) #create a label to display the result
label.grid(row=0, column=0, columnspan=column_count, sticky='ew') #make the label span all columns and align to the right

history_label = tkinter.Label(window, text="",bg=color_orange,  pady=6, font=("Arial", 12), anchor="e")
history_label.pack(expand=True, fill='both') 

for row in range(row_count):
    for column in range(column_count):
        value = button_values[row][column]
        button = tkinter.Button(frame, text=value, bg=color_light_gray, fg=color_black, font=('Arial', 18), 
                                padx=13, pady=9, width=column_count-1, height=1,
                                command=lambda value=value: button_clicked(value)) #create a button for each value
        
        if value in top_align:
            button.config(foreground=color_black, background=color_light_gray) #set the background color for top symbols
        elif value in right_align:
            button.config(foreground=color_blue, background=color_orange) #set the background color for right symbols
        else:
            button.config(foreground=color_white, background=color_dark_gray) #set the background color for numbers and dot
       
        button.grid(row=row+1, column=column)

frame.pack(expand=True, fill='both') #make the frame expand to fill the window

# define operands and operator
A = 0
operator = None
B = None

def clear_all():
    global A, operator, B
    A = 0
    operator = None
    B = None
    label['text'] = '0'

def remove_trailing_zeros(num):
    if num % 1 == 0: #check if the number is an integer
        num = int(num) #convert the number to an integer to remove trailing zeros
    return str(num) #return the number as a string

    
def button_clicked(value):
    global  right_align, top_align, label, A, B, operator 
    
    if value in right_align:
        if value == '=':
            if A is not None and operator is not None:
                B = label['text']
                numA = float(A) #convert A to a float for calculation
                numB = float(B) #convert B to a float for calculation
                
                if operator == '+':
                    label['text'] = remove_trailing_zeros(numA + numB)
                elif operator == '-':
                    label['text'] = remove_trailing_zeros(numA - numB)
                elif operator == '*':
                    label['text'] = remove_trailing_zeros(numA * numB)
                elif operator == '/':
                    if numB != 0:
                        label['text'] = remove_trailing_zeros(numA / numB)
                    else:
                        label['text'] = 'Error' #display error for division by zero
                        return
                    
                history_label['text'] = f"{A} {operator} {B} = {label['text']}"
                
                # keep result visible, reset operator for next input
                A = label['text']
                operator = None
                B = None
                
        elif value in '/*-+':
            if operator is  None:
                A = label['text']
                label['text'] = '0' #reset the label for the next operand
                B = '0' #reset B for the next operand
            operator = value #update the operator with the clicked value
            history_label['text'] = f"{A} {value}" #update history with the current operator
    elif value in top_align:
        if value == 'C':
            clear_all()
            label['text'] = '0'
        elif value == 'CE':
            label['text'] = '0'
        elif value == '%':
            result = float(label['text']) / 100
            label['text'] = remove_trailing_zeros(result)
        elif value == '√':
            A = float(label['text'])
            result = A ** 0.5
            label['text'] = remove_trailing_zeros(result)
    else:
        if value == '.':
            if '.' not in label['text']:
                label['text'] += value
        elif value in '0123456789':
            if label['text'] == '0':
                label['text'] = value #replace the initial '0' with the clicked value
            else:
                label['text'] += value


#center the window on the screen
window.update() #update the window to get the correct size
window_width = window.winfo_width() #get the width of the window
window_height = window.winfo_height() #get the height of the window
screen_width = window.winfo_screenwidth() #get the width of the screen
screen_height = window.winfo_screenheight() #get the height of the screen
x = (screen_width - window_width) // 2 #calculate the x coordinate to center the window
y = (screen_height - window_height) // 2 #calculate the y coordinate to center
#format the geometry string to set the size and position of the window
window.geometry(f"{window_width}x{window_height}+{x}+{y}") #set the geometry of the window to center it

window.mainloop() #start the main loop of the window

