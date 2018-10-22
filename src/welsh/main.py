# coding:utf-8
import ctypes

if __name__ == '__main__':
    so = ctypes.cdll.LoadLibrary
    lib = so('./libWelsh.so')
    lib.test()
    lib.welsh(ctypes.c_char_p(b'../../images/1c.jpg'), ctypes.c_char_p(b'../../images/1g.jpg'))
