# coding: utf-8
import redis
import json
import logger


class ProcessQueue(object):
    KEY_NAME = 'app:img:queue'
    WAIT_NAME = 'app:img:wait_ack'

    def __init__(self):
        self.pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True)
        self.r = redis.Redis(connection_pool=self.pool)
        self.log = logger.get_log(ProcessQueue)

    def r(self):
        return self.r

    def push(self, p_id, src_png, des_png, alg):
        raw_content = json.dumps({
            'src_png': src_png,
            'des_png': des_png,
            'alg': alg,
            'id': p_id
        })
        self.r.rpush(ProcessQueue.KEY_NAME, raw_content)
        self.log.info('rpush {} success, {}'.format(ProcessQueue.KEY_NAME, raw_content))

    def pop(self):
        raw_tuple = self.r.blpop(ProcessQueue.KEY_NAME, timeout=5)
        if not raw_tuple:
            self.log.info('blpop timeout, {} is empty'.format(ProcessQueue.KEY_NAME))
            return None
        self.log.info('blpop {} success, {}'.format(ProcessQueue.KEY_NAME, raw_tuple[1]))
        content = json.loads(raw_tuple[1])
        self.r.zadd(ProcessQueue.WAIT_NAME, {content['id']: 1}, incr=True)
        self.log.info('zadd {} success, {}'.format(ProcessQueue.WAIT_NAME, content['id']))
        return content

    def ack(self, p_id):
        self.r.zrem(ProcessQueue.WAIT_NAME, p_id)
        self.log.info('zrem {} success, {}'.format(ProcessQueue.WAIT_NAME, p_id))

    def scan(self):
        self.log.info('zscan {}'.format(self.r.zscan(ProcessQueue.WAIT_NAME)))


if __name__ == '__main__':
    p = ProcessQueue()
    # p.push(1234, '', '', '')
    p.scan()
    p.pop()
    p.scan()
    p.ack(1234)
    p.scan()
