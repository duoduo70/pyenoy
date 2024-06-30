import ast
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

class TokenType(Enum):
        FUNCTION = 0
        STRING = 1

PrecoloredContent = list[tuple[TokenType, str] | str]

def highlight_from_precolored_content(
                window: Window,
                precolored_content: PrecoloredContent):

        for i, item in enumerate(precolored_content):
                if type(item) == tuple:
                        if item[0] == TokenType.STRING:
                                precolored_content[i-1:i+2] = [
                                        (item[0],
                                                  precolored_content[i-1] +
                                                  item[1] +
                                                  precolored_content[i+1])]
                                

        for item in precolored_content:
                if type(item) == tuple:
                        if item[0] == TokenType.FUNCTION:
                                window.add(
                                        item[1],
                                        color=Highlight.FUNCTION,
                                        refresh=False
                                )
                        if item[0] == TokenType.STRING:
                                window.add(
                                        item[1],
                                        color=Highlight.STRING,
                                        refresh=False
                                )
                else:
                        window.add(item, refresh=False)

def init_stringio():
        '''
        重定向 stdio 到 StringIO
        '''
        import sys
        from io import StringIO
        stringio = StringIO()
        sys.stdout = stringio
        return stringio

def get_redirected_std_output(stringio) -> str:
        redirected_std_output = stringio.getvalue()
        if redirected_std_output != '':
                return redirected_std_output + '\n'
        else:
                return ''

def crop_precolored_content(content: PrecoloredContent, maxwidth: int, nlines: int):
        '''
        这个算法在应对 tuple 中 field 第一个字符是 '\n' 的场景时可能会出问题，我没测试过
        '''
        import collections
        cropped_content = collections.deque()
        now_width = 0
        for field in reversed(content):
                if type(field) == tuple:
                        temp = ''
                        for ch in reversed(field[1]):
                                if ch == '\n':
                                        nlines -= 1
                                        if nlines == 0:
                                                cropped_content.appendleft((field[0], temp))
                                                return list(cropped_content)
                                        now_width = 0
                                        temp += ch
                                else:
                                        now_width += 1
                                        if now_width == maxwidth:
                                                nlines -= 1
                                        if now_width > maxwidth:
                                                now_width = now_width - maxwidth
                                                nlines -= 1
                                        if nlines == 0:
                                                cropped_content.appendleft((field[0], temp))
                                                return list(cropped_content)
                                        temp += ch
                        cropped_content.appendleft((field[0], temp[::-1]))
                else:
                        for ch in reversed(field):
                                if ch == '\n':
                                        nlines -= 1
                                        if nlines == 0:
                                                return list(cropped_content)
                                        now_width = 0
                                        cropped_content.appendleft(ch)
                                else:
                                        now_width += 1
                                        if now_width == maxwidth:
                                                nlines -= 1
                                        if now_width > maxwidth:
                                                now_width = now_width - maxwidth
                                                nlines -= 1
                                        if nlines == 0:
                                                return list(cropped_content)
                                        cropped_content.appendleft(ch)
        return list(cropped_content)

def process_content(
                content: str,
                last_time_content: PrecoloredContent) -> PrecoloredContent:
        redirected_stdio = init_stringio() # 把 eval 的 stdio 重定向到这里

        outputwindow.clear()

        precolored_output : PrecoloredContent = last_time_content
        try:
                preprocessed = preprocess(content, redirected_stdio)
                if preprocessed == None:
                        result = ''
                else:
                        result = str(eval(preprocessed, {}, LOCALS))
        except Exception as e:
                precolored_output.append((TokenType.FUNCTION, '! ' + str(e) + '\n'))
        else:
                precolored_output.append(get_redirected_std_output(redirected_stdio))
                if result != '':
                        precolored_output.append((TokenType.FUNCTION, result + '\n'))

        cropped_precolored_output = crop_precolored_content(
                precolored_output, outputwindow.get_width(), outputwindow.get_height())
        highlight_from_precolored_content(outputwindow, cropped_precolored_output)

        outputwindow.refresh()

        return precolored_output

class VariableVisitor(ast.NodeVisitor):
        def __init__(self):
                self.tokens : PrecoloredContent = []

        def visit_Name(self, node):
                import builtins
                # 将变量名添加到集合中
                if hasattr(builtins, node.id):
                        self.tokens.append(
                                (node.col_offset, TokenType.FUNCTION, node.id))
        
        def visit_Constant(self, node):
                if type(node.value) == str:
                        self.tokens.append(
                                (node.col_offset + 1, TokenType.STRING, node.value))
        

def parse_tokens(content: str) -> list[tuple[int, TokenType, str]]:
        try:
                tree = ast.parse(content)
        except SyntaxError as e:
                raise e
        visitor = VariableVisitor()
        visitor.visit(tree)
        return visitor.tokens

def precolor_input_content(
                content: str,
                tokens : list[tuple[int, TokenType, str]]
            ) -> PrecoloredContent:

        precolored_content = list(content)
        replacing_offset = 0
        for (col_offset, tokentype, nodeid) in tokens:
                col_offset -= replacing_offset
                precolored_content[
                                         col_offset:col_offset+len(nodeid)
                                  ] = [(tokentype, nodeid)]
                replacing_offset += len(nodeid) - 1
        return precolored_content

def highlight_from_content(content: str):
        try:
                tokens = parse_tokens(content)
        except:
                return

        precolored_content = precolor_input_content(content, tokens)

        inputwindow.clear()

        highlight_from_precolored_content(inputwindow, precolored_content)
        
        inputwindow.refresh()

def highlight():
        real_point = inputwindow.get_point()

        highlight_from_content(inputwindow.get_content())

        inputwindow.set_point(real_point)       # 清除输出字符时对鼠标指针的所有副作用

current_outputwindow_content: PrecoloredContent = []
last_contents = []
last_contents_point = 0
# 光标指向下一个字符，而非当前字符
while ch := inputwindow.wait_char():
        if ch == SpecialKey.LEFT:
                inputwindow.add_point(-1)
        elif ch == SpecialKey.RIGHT:
                if inputwindow.get_point() < len(inputwindow.get_content()):
                        inputwindow.add_point(1)
                else:
                        pass    # 之后的代码都假定光标在已写入的范围内
        elif ch == SpecialKey.BACKSPACE:
                content_list = inputwindow.get_content_chlist()
                if content_list != [] and inputwindow.get_point() != 0:
                        real_point = inputwindow.get_point()
                        inputwindow.add_point(-1)
                        content_list.pop(real_point - 1)
                        inputwindow.put(content_list, move_cur=False)
                        highlight()
                else:
                        pass
        elif ch == SpecialKey.UP and last_contents != [] and last_contents_point > 0:
                last_contents_point -= 1
                inputwindow.put(last_contents[last_contents_point])
        elif (ch == SpecialKey.DOWN
              and last_contents != []):
                if last_contents_point < len(last_contents) - 1:
                        last_contents_point += 1
                        inputwindow.put(last_contents[last_contents_point])
                elif last_contents_point == len(last_contents) - 1:
                        last_contents_point += 1
                        inputwindow.clear()
                else:
                        pass
        elif ch == SpecialKey.ENTER or ch == '\n':
                content = inputwindow.get_content()
                if content != '':
                        current_outputwindow_content = (
                                process_content(content, current_outputwindow_content))
                        inputwindow.clear()
                        last_contents.append(content)
                        last_contents_point += 1
                else:
                        pass
        elif ch == '(':
                inputwindow.insert(inputwindow.get_point(), "()")
                inputwindow.add_point(1)
                highlight()
        elif ch == '"':
                inputwindow.insert(inputwindow.get_point(), "\"\"")
                inputwindow.add_point(1)
                highlight()
        elif ch == '\'':
                inputwindow.insert(inputwindow.get_point(), "''")
                inputwindow.add_point(1)
                highlight()
        elif type(ch) == SpecialKey:    # 暂且忽略其它控制字符
                pass
        else:
                inputwindow.insert(inputwindow.get_point(), ch)
                inputwindow.add_point(1)
                highlight()