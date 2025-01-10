import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    
    # Добавляем обработчик для консоли, если необходимо
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    console_handler.setFormatter(formatter)
    
    # Получаем корневой логгер и добавляем к нему обработчик
    logger = logging.getLogger()
    logger.addHandler(console_handler)