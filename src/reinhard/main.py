# coding:utf-8
import ctypes

if __name__ == '__main__':
    so = ctypes.cdll.LoadLibrary
    lib = so('./libReinhard.so')
    lib.test()
    lib.reinhard(ctypes.c_char_p(b'src.jpg'), ctypes.c_char_p(b'ref.jpg'))
