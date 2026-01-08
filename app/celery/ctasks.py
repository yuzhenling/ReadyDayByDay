from celery import Celery

app = Celery('ctasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/1')

@app.task
def add(x, y):
    """加法任务"""
    print(f'[任务执行] add({x}, {y})')
    result = x + y
    print(f'[任务完成] 结果: {result}')
    return result

@app.task
def multiply(x, y):
    """乘法任务"""
    print(f'[任务执行] multiply({x}, {y})')
    result = x * y
    print(f'[任务完成] 结果: {result}')
    return result

if __name__ == '__main__':
    # 本地测试时可以这样运行
    print("Celery 应用已创建")
    print(" celery -A app.ctasks worker --loglevel=info")
