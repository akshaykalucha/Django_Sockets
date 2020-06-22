import redis

r = redis.Redis()

# r.hset("channel", "ids", 253262787)
# r.hset("channel", 6665577889)
# r.hset("channel", 345567)
# r.hset("channel", 76554)

# print(r.hgetall("channel"))

# r.lpush("ips", "51.218.112.236")
# r.lpush("ips", "90.213.45.98")
# r.lpush("ips", "115.215.230.176")
# r.lpush("ips", "51.218.112.236")

# channelInfo = {
#     "channel:4889546": "hdgdteytuhF456",
# }

channelInfo = {
    "channel:6452989": "peuwfdjJhsyweF6&="
}

# r.hmset("channels", channelInfo)
r.hdel("channels", "channel:4889546")

# print(r.hget("channels", "channel:453628"))