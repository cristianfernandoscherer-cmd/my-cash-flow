import logging
import sys
from .config import settings

def setup_logger(name: str = __name__) -> logging.Logger:
    """Configura logger padronizado"""
    
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        # Formato do log
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        # Handler para console
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        
        # Handler para arquivo
        file_handler = logging.FileHandler("logs/transactions.log", encoding="utf-8")
        file_handler.setFormatter(formatter)
        
        # Aplicar handlers
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        
        # Nível de log
        logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))
    
    return logger

# Logger global
logger = setup_logger("transactions_ms")