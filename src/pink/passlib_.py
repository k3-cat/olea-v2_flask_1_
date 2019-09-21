from passlib.context import LazyCryptContext

olea_context = LazyCryptContext(schemes=['argon2'],
                                argon2__time_cost=20,
                                argon2__memory_cost=4096,
                                argon2__parallelism=4)
