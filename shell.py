# linux only: is needed to be able to use arrow keys
try:
    import gnureadline
except:
    pass

import sys
import basic_run
import basic.error


def main():
    while True:
        text = input("basic > ")
        if text.strip() == "":
            continue

        run(text)


def run(text, ctx="std::in", res=True):
    result, error = basic_run.run(ctx, text)

    if(error):
        print(error.as_string())
    elif result and res:
        if len(result.elements) == 1:
            print(repr(result.elements[0]))
        else:
            print(repr(result))


def run_file(argv):
    if argv[1] == "--file":
        fn = argv[2]
        script = ""
        try:
            with open(fn, "r") as f:
                script = f.read()
        except Exception as e:
            print("IO Error: " + str(e))
        run(script, fn, False)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        main()
    else:
        if len(sys.argv) == 3:
            run_file(sys.argv)
        if len(sys.argv) == 4:
            if sys.argv[3] == "--shell":
                run_file(sys.argv)
                main()
