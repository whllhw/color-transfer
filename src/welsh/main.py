# coding:utf-8
from multiprocessing import Process
import ctypes
import _ctypes


def do_work(src_img, ref_img, out_img):
    welsh_lib = ctypes.cdll.LoadLibrary('src/welsh/libWelsh.so')
    welsh_lib.welsh(ctypes.c_char_p(src_img.encode('utf-8')), ctypes.c_char_p(ref_img.encode('utf-8')),
                    ctypes.c_char_p(out_img.encode('utf-8')))
    _ctypes.dlclose(welsh_lib._handle)


def work(src_img, ref_img, out_img):
    p = Process(target=do_work, args=(src_img, ref_img, out_img))
    p.start()
    p.join()


if __name__ == '__main__':
    # while True:
    work('uploads/src_1g.jpg', 'uploads/ref_1c.jpg', 'result.jpg')
