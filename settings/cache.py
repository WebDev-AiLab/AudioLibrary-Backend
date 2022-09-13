from .base import DEBUG

REDIS_LOCATION = "redis"
if DEBUG:
    REDIS_LOCATION = "localhost"

# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": f"redis://{REDIS_LOCATION}:6379/1",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient"
#         }
#     }
# }

CACHE_TTL = 60 * 15  # 15 minutes
