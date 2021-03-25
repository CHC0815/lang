# linux only: is needed to be able to use arrow keys
try:
    import gnureadline
except:
    pass

import basic_run

while True:
    text = input("basic > ")
    if text.strip() == "": continue
    
    result, error = basic_run.run('std::in', text)

    if(error):
        print(error.as_string())
    elif result:
        if len(result.elements) == 1:
            print(repr(result.elements[0]))
        else:
            print(repr(result)) 
    