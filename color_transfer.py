# coding:utf-8
import logger
from src.reinhard.main import work as reinhard
from src.welsh.main import work as welsh
import message_queue
import time
import random
import uuid
import db
import redis_db
import os


class ColorTransfer(object):
    """
    调用cpp接口
    """

    def __init__(self):
        self.log = logger.get_log(ColorTransfer)

    def run(self, src_img, ref_img, alg, out_img):
        """
        src_img: 源文件路径
        ref_img: 参考文件路径
        alg: 算法
        out_img: 输出文件路径
        """
        if alg == 'reinhard':
            cpp_alg = reinhard
        elif alg == 'welsh':
            cpp_alg = welsh
        else:
            raise Exception('unknown alg :' + alg)
        self.log.info('start color transfer out_img:{}'.format(out_img))
        exitcode = cpp_alg(src_img, ref_img, out_img)
        if exitcode == 0:
            self.log.info('color transfer success out_img:{}'.format(out_img))
            return True
        else:
            self.log.error('cpp alg exitcode:{}'.format(exitcode))
            return False


class IdGenerator(object):

    def __init__(self):
        pass

    def gen_id(self):
        rand_low = random.randint(0, (1 << 12) - 1)
        machine_id = 0
        idc_id = 0
        timestamp = int(time.time() * 1000)
        ret = timestamp  # 41 bits
        ret = (ret << 5) + machine_id  # 5 bits
        ret = (ret << 5) + idc_id  # 5bits
        ret = (ret << 12) + rand_low  # 12bits
        return ret

    def gen_name(self):
        return uuid.uuid1()


class FileStore(object):
    """
    文件缓存池
    """

    CACHE_KEY = 'app:img_file:'

    def __init__(self):
        self.log = logger.get_log(FileStore)
        self.base = 'uploads'
        self.r = redis_db.get_connect()
        self.id_gen = IdGenerator()

    def upload(self, file, file_name):
        """
        保存完成后，返回文件名
        存放文件名到文件绝对路径
        """
        file_name, file_path = self.get_save_path(file_name)
        if file:
            file.save(file_path)
        self.save_to_redis(file_name, file_path)
        self.log.info('save file success, file_name:{}'.format(file_name))
        return file_name

    def save_to_redis(self, file_name, file_path):
        """
        保存文件名、文件绝对路径到redis
        """
        redis_file_name = FileStore.CACHE_KEY + file_name
        self.r.set(redis_file_name, file_path)

    def get_save_path(self, file_name):
        """
        生成唯一文件名、存储路径
        """
        file_name = file_name.split('_')[0] + '_' \
                    + str(self.id_gen.gen_id()) + '.' \
                    + file_name.split('.')[-1]
        file_path = os.path.join(self.base, file_name)
        return file_name, file_path

    def list(self, prefix):
        """
        存放的所有前缀相符的文件名列表
        """
        file_name_list = self.r.keys(FileStore.CACHE_KEY + prefix + '*')
        return [name[len(FileStore.CACHE_KEY):] for name in file_name_list]

    def download(self, file_name):
        """
        获取文件名对应的绝对路径
        """
        return self.r.get(FileStore.CACHE_KEY + file_name)


class Executor(object):

    def __init__(self):
        self.log = logger.get_log(Executor)
        self.mq = message_queue.ProcessQueue()
        self.fs = FileStore()
        self.cf = ColorTransfer()
        self.db = db.SqliteDB()

    def run_loop(self):
        while True:
            content = self.mq.pop()
            if not content:
                self.log.info('message queue is empty')
                continue
            # 调用算法需要文件的绝对路径
            src_img = self.fs.download(content['src_img'])
            ref_img = self.fs.download(content['ref_img'])
            out_img = 'res_.jpg'  # 等待生成文件名
            out_img, out_img_path = self.fs.get_save_path(out_img)
            try:
                success = self.cf.run(src_img,
                                      ref_img,
                                      content['alg'],
                                      out_img_path)
                if success:
                    self.log.info(
                        'alg run success, src_img: {}, ref_img: {}, out_img: {}'.format(src_img, ref_img, out_img))
                    self.mq.ack(content['id'])
                    self.fs.save_to_redis(out_img, out_img_path)
                    self.db.ack_file(content['id'], out_img)
                else:
                    raise Exception('run failed')
            except:
                # TODO 运行失败，需要重试
                self.log.exception('processes failed')

    def add_task(self, r_id, src_img, ref_img, alg):
        """
        web添加task
        """
        self.mq.push({
            'id': r_id,
            'src_img': src_img,
            'ref_img': ref_img,
            'alg': alg
        })


if __name__ == '__main__':
    executor = Executor()
    executor.run_loop()
