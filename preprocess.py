from io import StringIO
import subprocess

# TODO: 可以返回一个 lambda 之类
def preprocess(content: str, stringio: StringIO):
        if content[0] == '@':
                result = subprocess.run(content[1:].split(' '), stdout=subprocess.PIPE)
                if result.stdout != None:
                        stringio.write(result.stdout.decode())
                return None
        else:
                return content