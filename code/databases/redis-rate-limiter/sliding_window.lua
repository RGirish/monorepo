-- KEYS[1] = sorted set key
-- ARGV[1] = current timestamp in milliseconds
-- ARGV[2] = window length in milliseconds
-- ARGV[3] = limit
-- ARGV[4] = unique member id for this request

local key = KEYS[1]
local now = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local limit = tonumber(ARGV[3])
local member = ARGV[4]

redis.call("ZREMRANGEBYSCORE", key, "-inf", now - window)
local count = redis.call("ZCARD", key)

if count < limit then
    redis.call("ZADD", key, now, member)
    redis.call("PEXPIRE", key, window)
    return count + 1
end

redis.call("PEXPIRE", key, window)
return count
