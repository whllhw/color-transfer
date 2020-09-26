# coding:utf-8
import logger
from src.reinhard.main import work as reinhard
from src.welsh.main import work as welsh
import message_queue


class ColorTransfer(object):
    """
    调用cpp接口
    """

    def __init__(self):
        self.log = logger.get_log(ColorTransfer)

    def run(self, src_img, ref_img, alg, out_img):
        if alg == 'reinhard':
            cpp_alg = reinhard
        elif alg == 'welsh':
            cpp_alg = welsh
        else:
            raise Exception('unknown alg :' + alg)
        cpp_alg(src_img, ref_img, out_img)
        self.log.info('color transfer success out_img:{}'.format(out_img))


class FileStore(object):
    """
    分布式文件上传与下载
    """

    def __init__(self):
        self.log = logger.get_log(FileStore)

    def upload(self):
        pass

    def download(self):
        pass


class Executor(object):

    def __init__(self):
        self.log = logger.get_log(Executor)
        self.mq = message_queue.ProcessQueue()
        self.fs = FileStore()

    def run_loop(self):
        while True:
            content = self.mq.pop()
            if not content:
                self.log.info('message queue is empty')
                continue

    def add_task(self):
        pass


if __name__ == '__main__':
    pass
