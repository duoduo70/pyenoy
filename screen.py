r"""
这是和创建 Curses-like Screen 相关的代码的封装
我们会在应用程序实现的地方灵活的随时调用这些“底层”的UI相关的代码
至于每个应用程序要使用怎样的控件，可以在应用程序的内部进行定义
应用程序随时可以通过这套接口与其它应用程序交互
        亦可以与 Shell 本身提供的控件进行交互
我们对 Curses 代码进行隐藏，以获得更优雅的 API 与更强的跨平台可移植性，屏蔽平台之间的差异
这是平台相关的部分，尽可能小，但我们可以将其封装成更高级的库
这应该是应用程序可以使用的最底层 API
Usage:
        import screen
        screen.screen_init() # Internal status machine initialization
        myscreen = screen.get_screen()
DONT:
        你不应该直接调用 curses
"""

from enum       import Enum
from typing     import Any
import os
import curses
import unicodedata  # Some Unix-like OS only


class TextAttribute(Enum):
        ALTCHARSET = curses.A_ALTCHARSET
        ATTRIBUTES = curses.A_ATTRIBUTES
        BLINK      = curses.A_BLINK
        BOLD       = curses.A_BOLD
        CHARTEXT   = curses.A_CHARTEXT
        COLOR      = curses.A_COLOR
        DIM        = curses.A_DIM
        HORIZONTAL = curses.A_HORIZONTAL
        INVIS      = curses.A_INVIS
        ITALIC     = curses.A_ITALIC
        LEFT       = curses.A_LEFT
        LOW        = curses.A_LOW
        NORMAL     = curses.A_NORMAL
        PROTECT    = curses.A_PROTECT
        REVERSE    = curses.A_REVERSE
        RIGHT      = curses.A_RIGHT
        STANDOUT   = curses.A_STANDOUT
        TOP        = curses.A_TOP
        UNDERLINE  = curses.A_UNDERLINE
        VERTICAL   = curses.A_VERTICAL

class Color(Enum):
        BLACK   = curses.COLOR_BLACK
        BLUE    = curses.COLOR_BLUE
        CYAN    = curses.COLOR_CYAN
        GREEN   = curses.COLOR_GREEN
        MAGENTA = curses.COLOR_MAGENTA
        RED     = curses.COLOR_RED
        WHITE   = curses.COLOR_WHITE
        YELLOW  = curses.COLOR_YELLOW

class SpecialKey(Enum):
        A1        = curses.KEY_A1
        A3        = curses.KEY_A3
        B2        = curses.KEY_B2
        BACKSPACE = curses.KEY_BACKSPACE
        BEG       = curses.KEY_BEG
        BREAK     = curses.KEY_BREAK
        BTAB      = curses.KEY_BTAB
        C1        = curses.KEY_C1
        C3        = curses.KEY_C3
        CANCEL    = curses.KEY_CANCEL
        CATAB     = curses.KEY_CATAB
        CLEAR     = curses.KEY_CLEAR
        CLOSE     = curses.KEY_CLOSE
        COMMAND   = curses.KEY_COMMAND
        COPY      = curses.KEY_COPY
        CREATE    = curses.KEY_CREATE
        CTAB      = curses.KEY_CTAB
        DC        = curses.KEY_DC
        DL        = curses.KEY_DL
        DOWN      = curses.KEY_DOWN
        EIC       = curses.KEY_EIC
        END       = curses.KEY_END
        ENTER     = curses.KEY_ENTER
        EOL       = curses.KEY_EOL
        EOS       = curses.KEY_EOS
        EXIT      = curses.KEY_EXIT
        F0        = curses.KEY_F0
        F1        = curses.KEY_F1
        F10       = curses.KEY_F10
        F11       = curses.KEY_F11
        F12       = curses.KEY_F12
        F13       = curses.KEY_F13
        F14       = curses.KEY_F14
        F15       = curses.KEY_F15
        F16       = curses.KEY_F16
        F17       = curses.KEY_F17
        F18       = curses.KEY_F18
        F19       = curses.KEY_F19
        F2        = curses.KEY_F2
        F20       = curses.KEY_F20
        F21       = curses.KEY_F21
        F22       = curses.KEY_F22
        F23       = curses.KEY_F23
        F24       = curses.KEY_F24
        F25       = curses.KEY_F25
        F26       = curses.KEY_F26
        F27       = curses.KEY_F27
        F28       = curses.KEY_F28
        F29       = curses.KEY_F29
        F3        = curses.KEY_F3
        F30       = curses.KEY_F30
        F31       = curses.KEY_F31
        F32       = curses.KEY_F32
        F33       = curses.KEY_F33
        F34       = curses.KEY_F34
        F35       = curses.KEY_F35
        F36       = curses.KEY_F36
        F37       = curses.KEY_F37
        F38       = curses.KEY_F38
        F39       = curses.KEY_F39
        F4        = curses.KEY_F4
        F40       = curses.KEY_F40
        F41       = curses.KEY_F41
        F42       = curses.KEY_F42
        F43       = curses.KEY_F43
        F44       = curses.KEY_F44
        F45       = curses.KEY_F45
        F46       = curses.KEY_F46
        F47       = curses.KEY_F47
        F48       = curses.KEY_F48
        F49       = curses.KEY_F49
        F5        = curses.KEY_F5
        F50       = curses.KEY_F50
        F51       = curses.KEY_F51
        F52       = curses.KEY_F52
        F53       = curses.KEY_F53
        F54       = curses.KEY_F54
        F55       = curses.KEY_F55
        F56       = curses.KEY_F56
        F57       = curses.KEY_F57
        F58       = curses.KEY_F58
        F59       = curses.KEY_F59
        F6        = curses.KEY_F6
        F60       = curses.KEY_F60
        F61       = curses.KEY_F61
        F62       = curses.KEY_F62
        F63       = curses.KEY_F63
        F7        = curses.KEY_F7
        F8        = curses.KEY_F8
        F9        = curses.KEY_F9
        FIND      = curses.KEY_FIND
        HELP      = curses.KEY_HELP
        HOME      = curses.KEY_HOME
        IC        = curses.KEY_IC
        IL        = curses.KEY_IL
        LEFT      = curses.KEY_LEFT
        LL        = curses.KEY_LL
        MARK      = curses.KEY_MARK
        MAX       = curses.KEY_MAX
        MESSAGE   = curses.KEY_MESSAGE
        MIN       = curses.KEY_MIN
        MOUSE     = curses.KEY_MOUSE
        MOVE      = curses.KEY_MOVE
        NEXT      = curses.KEY_NEXT
        NPAGE     = curses.KEY_NPAGE
        OPEN      = curses.KEY_OPEN
        OPTIONS   = curses.KEY_OPTIONS
        PPAGE     = curses.KEY_PPAGE
        PREVIOUS  = curses.KEY_PREVIOUS
        PRINT     = curses.KEY_PRINT
        REDO      = curses.KEY_REDO
        REFERENCE = curses.KEY_REFERENCE
        REFRESH   = curses.KEY_REFRESH
        REPLACE   = curses.KEY_REPLACE
        RESET     = curses.KEY_RESET
        RESIZE    = curses.KEY_RESIZE
        RESTART   = curses.KEY_RESTART
        RESUME    = curses.KEY_RESUME
        RIGHT     = curses.KEY_RIGHT
        SAVE      = curses.KEY_SAVE
        SBEG      = curses.KEY_SBEG
        SCANCEL   = curses.KEY_SCANCEL
        SCOMMAND  = curses.KEY_SCOMMAND
        SCOPY     = curses.KEY_SCOPY
        SCREATE   = curses.KEY_SCREATE
        SDC       = curses.KEY_SDC
        SDL       = curses.KEY_SDL
        SELECT    = curses.KEY_SELECT
        SEND      = curses.KEY_SEND
        SEOL      = curses.KEY_SEOL
        SEXIT     = curses.KEY_SEXIT
        SF        = curses.KEY_SF
        SFIND     = curses.KEY_SFIND
        SHELP     = curses.KEY_SHELP
        SHOME     = curses.KEY_SHOME
        SIC       = curses.KEY_SIC
        SLEFT     = curses.KEY_SLEFT
        SMESSAGE  = curses.KEY_SMESSAGE
        SMOVE     = curses.KEY_SMOVE
        SNEXT     = curses.KEY_SNEXT
        SOPTIONS  = curses.KEY_SOPTIONS
        SPREVIOUS = curses.KEY_SPREVIOUS
        SPRINT    = curses.KEY_SPRINT
        SR        = curses.KEY_SR
        SREDO     = curses.KEY_SREDO
        SREPLACE  = curses.KEY_SREPLACE
        SRESET    = curses.KEY_SRESET
        SRIGHT    = curses.KEY_SRIGHT
        SRSUME    = curses.KEY_SRSUME
        SSAVE     = curses.KEY_SSAVE
        SSUSPEND  = curses.KEY_SSUSPEND
        STAB      = curses.KEY_STAB
        SUNDO     = curses.KEY_SUNDO
        SUSPEND   = curses.KEY_SUSPEND
        UNDO      = curses.KEY_UNDO
        UP        = curses.KEY_UP

        def is_special_key(ch):
                '''
                这个函数不限制参数类型
                输出其类型是否是 SpecialKey
                因为 Window.wait_char() 的返回类型可能是 int、str、SpecialKey
                '''
                if type(ch) == SpecialKey:
                        return True
                else:
                        return False

def get_key_name(key):
        return curses.keyname(key)

def can_change_color() -> bool:
        return curses.can_change_color()


def char_display_wide(ch) -> int:
        '''
        对于一些字符，例如汉字，它们会在终端中占用两格宽度
        这个函数可以获取字符的显示宽度，以正确在终端中排版这些字符
        '''
        if unicodedata.east_asian_width(ch) in ("W", "F"):
                return 2
        else:
                return 1


def str_display_len(str_) -> int:
        len_ = 0
        for ch in str_:
                len_ += char_display_wide(ch)
        return len_


class Window:
        """
        坐标定位和 Curses 不同
        先 X 再 Y ，(0, 0) 为屏幕左下角
        编辑指针是从 0 开始的，指向下一个字符
        """

        __begin_x: int  # 左上角 x
        __begin_y: int  # 左上角 y
        __end_x  : int  # 右下角 x
        __end_y  : int  # 右下角 y

        __content       = ""  # 现在 Window 内的内容
        __display_point = 0  # 显示的编辑指针
        __real_point    = 0  # 可作用于 Content 的编辑指针
        # 有两个指针是为了解决 CJK 字符在终端中显示为两字符宽度的问题

        def __reverse_pos(field_len, pos_weight: int):
                '''
                Example:
                        __reverse_pos(self.get_height(), 0)
                        将 Screen 形式的 y 坐标转化为 Curses 形式

                        __reverse_pos(self.get_height(), -1)
                        类似 list_[-1] 的形式使用坐标
                '''
                if pos_weight >= 0:
                        return field_len - 1 - pos_weight
                else:
                        return field_len + pos_weight
        def __init__(
                self,
                begin_x = 0,
                begin_y = os.get_terminal_size().lines - 1,
                end_x   = os.get_terminal_size().columns - 1,
                end_y   = 0,
        ):
                
                # 支持使用反转坐标模式，例如 y = -1 是从上往下算第 0 列
                if begin_x < 0:
                        begin_x = Window.__reverse_pos(Screen.get_width(), begin_x)
                if begin_y < 0:
                        begin_y = Window.__reverse_pos(Screen.get_height(), begin_y)
                if end_x < 0:
                        end_x = Window.__reverse_pos(Screen.get_width(), end_x)
                if end_y < 0:
                        end_y = Window.__reverse_pos(Screen.get_height(), end_y)

                self.__curses_window = curses.newwin(
                        begin_y - end_y + 1,
                        end_x - begin_x + 1,
                        Window.__reverse_pos(
                                Screen.get_height(),
                                begin_y
                        ),
                        begin_x
                )
                self.__curses_window.keypad(True)
                self.__begin_x = begin_x
                self.__begin_y = begin_y
                self.__end_x   = end_x
                self.__end_y   = end_y

        def _from_curses_window(
                curses_window,
                nlines: int, ncols: int, begin_y: int, begin_x: int
        ):
                window = Window()

                this_class_begin_y = Window.__reverse_pos(
                        Screen.get_height(),
                        begin_y
                )

                this_class_end_y = Window.__reverse_pos(
                        Screen.get_height(),
                        begin_y + nlines - 1
                )

                window.__begin_x       = begin_x
                window.__begin_y       = this_class_begin_y
                window.__end_x         = begin_x + ncols - 1
                window.__end_y         = this_class_end_y
                window.__curses_window = curses_window
                return window

        def put(self, text, x = 0, y = 0, refresh=True):
                if type(text) == list:
                        text = "".join(text)

                self.__curses_window.clear()
                self.__curses_window.addstr(y, x, text)
                self.__content = text

                if refresh == True:
                        self.__curses_window.refresh()
                else:
                        pass

                return self
        
        def clear(self):
                self.__curses_window.clear()
                self.__content = ''
                self.__curses_window.refresh()
                self.__real_point = 0
                self.__display_point = 0

        def add(self, str_or_can_be_str: str | Any):
                str_ = str(str_or_can_be_str)
                self.__content       += str_
                self.__display_point += str_display_len(str_)
                self.__real_point    += len(str_)
                self.__curses_window.addstr(str_)
                self.refresh()

        def set_real_point(self, real_point):
                """
                该函数假定光标永远在已写入的范围内
                """
                if real_point < 0:
                        self.__real_point = 0
                else:
                        self.__real_point = real_point

                self.__display_point = str_display_len(self.__content)

                x, y = self.len_to_xy(self.__display_point)
                self.__curses_window.move(y, x)

        def __just_add_display_point(self, len_):
                if len_ >= 0:
                        self.__display_point += str_display_len(
                                self.__content[self.__real_point : self.__real_point + len_]
                        )
                else:
                        self.__display_point -= str_display_len(
                                self.__content[self.__real_point + len_ : self.__real_point]
                        )

        def add_real_point(self, len_):
                """
                该函数假定光标永远在已写入的范围内
                """

                if self.__real_point + len_ < 0:
                        len_ = self.__real_point

                self.__just_add_display_point(len_)

                self.__real_point += len_

                x, y = self.len_to_xy(self.__display_point)
                self.__curses_window.move(y, x)

        def get_display_point(self):
                return self.__display_point

        def get_real_point(self):
                return self.__real_point

        def refresh(self):
                self.__curses_window.refresh()
                return self

        def get_width(self):
                return self.__end_x - self.__begin_x

        def get_height(self):
                return self.__begin_y - self.__end_y + 1

        def get_content(self):
                return self.__content

        def get_content_list(self):
                return list(self.get_content())

        def len_to_xy(self, len_):
                if len_ <= 0:
                        return 0, 0
                else:
                        y = len_ // self.get_width()
                        x = len_ % self.get_width()
                        return x, y

        def xy_to_len(self, x, y):
                if x == 0:
                        len_ = y * self.get_width()
                else:
                        len_ = (y - 1) * self.get_width() + x

                if len_ < 0:
                        return 0
                else:
                        return len_

        def __get_utf8char(self, startch):
                if startch & 0b10000000 == 0:  # ASCII char
                        return chr(startch)
                elif startch & 0b11100000 == 0b11000000:  # UTF-8 2bytes char
                        byte2 = self.__curses_window.getch()
                        utf8ch = (startch << 8) | byte2
                        return str(int.to_bytes(utf8ch, length=2), encoding="utf8")
                elif startch & 0b11110000 == 0b11100000:  # UTF-8 3bytes char
                        byte2 = self.__curses_window.getch()
                        byte3 = self.__curses_window.getch()
                        utf8ch = (((startch << 8) | byte2)
                                                        << 8) | byte3
                        return str(int.to_bytes(utf8ch, length=3), encoding="utf8")
                elif startch & 0b11111000 == 0b11110000:  # UTF-8 4bytes char
                        byte2 = self.__curses_window.getch()
                        byte3 = self.__curses_window.getch()
                        byte4 = self.__curses_window.getch()
                        utf8ch = (((((startch << 8) | byte2)
                                                        << 8) | byte3) 
                                                                << 8) | byte4
                        return str(int.to_bytes(utf8ch, length=4), encoding="utf8")

        def wait_char(self) -> str | int | SpecialKey:
                """
                这会输出一个 UTF-8 编码的字符或一个控制字符
                如果输入不合法，则输出 \ufffd (�)
                """
                ch = self.__curses_window.getch()

                if 32 <= ch <= 126 or (ch > 127 and ch < 256):  # ASCII 或 UTF-8 字符
                        return self.__get_utf8char(ch)
                else:
                        # 如果 ch 是 SpecialKey ，返回对应的 SpecialKey 名称
                        # 如果不是，则返回对应的值
                        try:
                                sk = SpecialKey(ch)
                        except ValueError:
                                return ch
                        else:
                                return sk

        def insert(self, index, str_or_can_be_str: str | Any):
                contentlist = list(self.__content)
                contentlist.insert(index, str(str_or_can_be_str))
                self.put("".join(contentlist), 0, 0)

        def move_to(self, x, y):
                self.__curses_window.move(y, x)
                self.refresh()


__STDSCR = None


class Screen:
        """控制 Pyeony 视口本身"""

        def init():
                global __STDSCR
                __STDSCR = curses.initscr()
                curses.noecho()         # 底层开启无回显模式，我们会再套一层
                curses.cbreak()         # 同理，我们不需要默认按回车
                __STDSCR.keypad(True)    # 让 curses 处理特殊按键
                __STDSCR.clear()

        def exit():
                curses.echo()
                curses.nocbreak()
                __STDSCR.keypad(False)
                curses.endwin()

        def get_width() -> int:
                return curses.COLS
        
        def get_height() -> int:
                return curses.LINES

        def get_main_window() -> Window:
                return Window._from_curses_window(
                        __STDSCR, os.get_terminal_size().lines,
                        os.get_terminal_size().columns,
                        0,
                        0
                )
