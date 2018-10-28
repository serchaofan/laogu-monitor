import redis

def redis_connect(settings):
  print(settings.REDIS_CONNECT)
  pool = redis.ConnectionPool(
    host=settings.REDIS_CONNECT['HOST'],
    port=settings.REDIS_CONNECT['PORT']
  )
  return redis.Redis(connection_pool=pool)