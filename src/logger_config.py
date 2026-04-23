import logging
import sys
import os

def setup_logger(name: str):
    """
    Configura um logger estruturado para a aplicação.
    """
    # Cria a pasta de logs se não existir
    if not os.path.exists("logs"):
        os.makedirs("logs")

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Evita duplicidade de handlers se o logger já estiver configurado
    if not logger.handlers:
        # Formato profissional: Data - Nome - Nível - Mensagem
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Handler para saída no console (stdout) - Mostra tudo (INFO+)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Handler para arquivo - Salva avisos e erros (WARNING+)
        file_handler = logging.FileHandler("logs/erros.log", encoding="utf-8")
        file_handler.setLevel(logging.WARNING)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
