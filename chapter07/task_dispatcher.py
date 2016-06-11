import logging

from celery import Celery

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(message)s')

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

app = Celery('tasks', broker='redis://192.168.25.21:6379/0')
app.conf.CELERY_RESULT_BACKEND = 'redis://192.168.25.21:6379/0'

#For fibo_tasks
input_list = [4, 3, 8, 6, 10]

#For crawl_tasks
url_list = ['http://www.google.com',
            'http://br.bing.com',
            'http://duckduckgo.com',
            'http://github.com',
            'http://br.search.yahoo.com']

def manage_sqrt_task(value):
    result = app.send_task('tasks.sqrt_task', args=(value,),
        queue='sqrt_queue', routing_key='sqrt_queue')
    logging.info(result.get())


def manage_fibo_task(value_list):
    async_result_dict = {x: app.send_task('tasks.fibo_task', 
        args=(x,), queue='fibo_queue', routing_key='fibo_queue')
            for x in value_list}
    
    for key, value in async_result_dict.items():
        if value.ready():
            logger.info("Value [%d] -> %s" % (key, value.get()[1]))
        else:
            logger.info("The task [%s] is not ready" % value.task_id)
    

def manage_crawl_task(url_list):
    async_result_dict = {url: app.send_task('tasks.crawl_task', 
        args=(url,), queue='webcrawler_queue', routing_key='webcrawler_queue')
            for url in url_list}

    for key, value in async_result_dict.items():
        logger.info("%s -> %s" % (key, value.get()))
    


if __name__ == '__main__':
    #manage_sqrt_task(4)
    #manage_fibo_task(input_list) 
    manage_crawl_task(url_list)
    
