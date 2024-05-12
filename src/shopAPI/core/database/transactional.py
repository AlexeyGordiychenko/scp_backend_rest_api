from functools import wraps

from shopAPI.core.database import session


class Transactional:
    def __init__(self, refresh: bool = False):
        self.refresh = refresh

    def __call__(self, function):
        @wraps(function)
        async def decorator(*args, **kwargs):
            try:
                result = await function(*args, **kwargs)
                await session.commit()
                if self.refresh:
                    await session.refresh(result)
                return result
            except Exception as exception:
                await session.rollback()
                raise exception

        return decorator
