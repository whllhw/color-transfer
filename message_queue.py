# coding: utf-8
import redis_db
import json
import logger


class ProcessQueue(object):
    """
    利用redis实现消息队列
    """
    # 待消费队列
    KEY_NAME = 'app:img:queue'
    # 待确认消息有序集合
    WAIT_NAME = 'app:img:wait_ack'

    def __init__(self):
        self.r = redis_db.get_connect()
        self.log = logger.get_log(ProcessQueue)

    def r(self):
        return self.r

    def push(self, raw_content):
        """
        将消息放入队列末尾
        """
        content = json.dumps(raw_content)
        self.r.rpush(ProcessQueue.KEY_NAME, content)
        self.log.info('rpush {} success, {}'.format(ProcessQueue.KEY_NAME, content))

    def pop(self, timeout=5):
        """
        弹出队首的消息，并将消息id放入待确认队列中
        """
        raw_tuple = self.r.blpop(ProcessQueue.KEY_NAME, timeout=timeout)
        if not raw_tuple:
            self.log.info('blpop timeout, {} is empty'.format(ProcessQueue.KEY_NAME))
            return None
        self.log.info('blpop {} success, {}'.format(ProcessQueue.KEY_NAME, raw_tuple[1]))
        content = json.loads(raw_tuple[1])
        self.r.zadd(ProcessQueue.WAIT_NAME, {content['id']: 1}, incr=True)
        self.log.info('zadd {} success, {}'.format(ProcessQueue.WAIT_NAME, content['id']))
        return content

    def ack(self, p_id):
        """
        消息消费完毕，将消息id移出待确认队列
        """
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
