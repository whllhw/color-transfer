# coding:utf-8
import ctypes

def work(src_img,ref_img,out_img):
    so = ctypes.cdll.LoadLibrary
    lib = so('src/welsh/libWelsh.so')
    lib.test()
    lib.welsh(ctypes.c_char_p(src_img.encode('utf-8')), ctypes.c_char_p(ref_img.encode('utf-8')),ctypes.c_char_p(out_img.encode('utf-8')))

if __name__ == '__main__':
    work('../../images/1g.jpg','../../images/1c.jpg','result.jpg')