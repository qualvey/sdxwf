import logging
import os
from colorama import init, Fore, Style
import coloredlogs

# 初始化 colorama，确保在 Windows 上颜色输出也能正常
init(autoreset=True)

# 屏蔽 urllib3 的烦人日志（比如 requests 请求的 debug 信息）
logging.getLogger("urllib3").setLevel(logging.WARNING)

def get_logger(name: str, log_file: str = './log/debug.log') -> logging.Logger:
    """
    创建一个带有彩色控制台输出和文件记录功能的 logger。

    :param name: logger 的名称，通常传 __name__
    :param log_file: 日志文件保存路径
    :return: 配置好的 logger 对象
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # 如果 logger 已经添加过 Handler，就直接返回（防止重复日志）
    if logger.hasHandlers():
        return logger

    # ---------- 文件日志部分 ----------
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    file_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
    )
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)

    # ---------- 控制台日志（带颜色） ----------
    console_format = "%(asctime)s %(name)s %(levelname)s %(message)s"
    coloredlogs.install(
        level='DEBUG',
        logger=logger,
        fmt="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
        level_styles={
            'debug': {'color': 'cyan'},
            'info': {'color': 'green'},
            'warning': {'color': 'yellow'},
            'error': {'color': 'red'},
            'critical': {'color': 'red', 'bold': True},
        }
    )

    return logger

# 测试代码
if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.debug("调试信息")
    logger.info("普通信息")
    logger.warning("警告信息")
    logger.error("错误信息")
    logger.critical("严重错误")
