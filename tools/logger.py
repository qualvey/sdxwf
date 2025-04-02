
import logging
import os

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.WARNING  # 设置日志级别
)

def get_logger(name: str, log_file: str = './log', level=logging.DEBUG):
    """
    获取或创建一个 logger。

    :param name: logger 的名称
    :param log_file: 日志文件路径
    :param level: logger 记录的最低日志级别，默认 DEBUG
    :return: 配置好的 logger 对象
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # 避免重复添加 Handler
    if not logger.handlers:
        # 创建日志文件目录（如果不存在）
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        # 控制台 Handler（INFO 及以上）
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # 文件 Handler（记录所有日志）
        file_handler = logging.FileHandler(log_file, mode="w")
        file_handler.setLevel(logging.DEBUG)

        # 设置日志格式
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        # 添加 Handlers
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger

if __name__ == "__main__":
    # 使用日志
    logger.debug("这是一条调试日志")
    logger.info("这是一条普通日志")
    logger.warning("这是一条警告日志")
    logger.error("这是一条错误日志")
    logger.critical("这是一条严重错误日志")
