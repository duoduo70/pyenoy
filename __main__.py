from preprocess import preprocess
from screen import *

Screen.init()

mainwindow = Screen.get_main_window()

inputwindow = Window(
        0, 0,
        -1, 0
)
outputwindow = Window(
        0, -1,
        -1, 1
)

outputwindow.put("Pyeony 0.0.1\n")

LOCALS = {} # 它的项将在其它地方被添加

def process_content(content: str):
        import sys
        from io import StringIO
        stringio = StringIO()
        sys.stdout = stringio

        outputlines = []

        try:
                result = str(eval(preprocess(content), {}, LOCALS))
        except NameError as e:
                outputlines.append('! ' + str(e))
        else:
                redirected_output = stringio.getvalue()

                if redirected_output != '':
                        outputlines.extend(redirected_output.splitlines())

                outputlines.append(': ' + result)
        finally:
                outputlines = outputwindow.get_content().splitlines() + outputlines
                maxlines = outputwindow.get_height() + 1
                renderstarting = len(outputlines) // maxlines * maxlines
                outputwindow.put('\n'.join(outputlines[renderstarting::]))

# 光标指向下一个字符，而非当前字符
while ch := inputwindow.wait_char():
        if ch == SpecialKey.LEFT:
                inputwindow.add_real_point(-1)
        elif ch == SpecialKey.RIGHT:
                if inputwindow.get_real_point() <= len(inputwindow.get_content()):
                        inputwindow.add_real_point(1)
                else:
                        pass    # 之后的代码都假定光标在已写入的范围内
        elif ch == SpecialKey.BACKSPACE:
                content_list = inputwindow.get_content_list()
                if content_list != []:
                        real_point = inputwindow.get_real_point()
                        inputwindow.add_real_point(-1)
                        content_list.pop(real_point - 1)
                        inputwindow.put(content_list)
                else:
                        pass
        elif ch == SpecialKey.ENTER or ch == ord('\n'):
                content = inputwindow.get_content()
                if content != '':
                        process_content(content)
                        inputwindow.clear()
                else:
                        pass
        elif type(ch) == SpecialKey:    # 暂且忽略其它控制字符
                pass
        else:
                inputwindow.insert(inputwindow.get_real_point(), ch)
                inputwindow.add_real_point(1)