# coding:utf-8
import ctypes
def work(src_img,ref_img,out_img):
    so = ctypes.cdll.LoadLibrary
    lib = so('src/reinhard/libReinhard.so')
    lib.test()
    lib.reinhard(ctypes.c_char_p(src_img.encode('utf-8')), ctypes.c_char_p(ref_img.encode('utf-8')),ctypes.c_char_p(out_img.encode('utf-8')))

if __name__ == '__main__':
    work('src.jpg','ref.jpg','out.jpg')
