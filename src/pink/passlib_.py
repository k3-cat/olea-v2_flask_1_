from passlib.context import LazyCryptContext

olea_context = LazyCryptContext(schemes=['argon2'],
                                argon2__time_cost=30,
                                argon2__memory_cost=1024,
                                argon2__parallelism=4)
