from functools import wraps

from shopAPI.core.database import session


class Transactional:
    def __call__(self, function):
        @wraps(function)
        async def decorator(*args, **kwargs):
            try:
                result = await function(*args, **kwargs)
                await session.commit()
                return result
            except Exception as exception:
                await session.rollback()
                raise exception

        return decorator
