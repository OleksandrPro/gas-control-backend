from .lookups import lookups_router
from .cards import cards_router
from .equipment import equipment_router

# Если в будущем появятся другие роутеры, добавляйте их сюда так же:
# from .cards import router as cards_router

__all__ = ["lookups_router", "cards_router", "equipment_router"]