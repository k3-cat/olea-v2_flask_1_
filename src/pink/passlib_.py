from passlib.context import LazyCryptContext

olea_context = LazyCryptContext(schemes=['argon2'],
                                argon2__time_cost=2,
                                argon2__memory_cost=256 * 1024,
                                argon2__parallelism=4)
