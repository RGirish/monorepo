import sys

import redis

LIMIT = 3
WINDOW_SECONDS = 10


def is_allowed(client: redis.Redis, key: str) -> tuple[bool, int, int]:
    count = client.incr(key)
    if count == 1:
        client.expire(key, WINDOW_SECONDS)
    ttl = client.ttl(key)
    return count <= LIMIT, count, ttl


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: python ratelimit_naive.py <user_id>")
        sys.exit(1)

    user_id = sys.argv[1]
    key = f"ratelimit:{user_id}"

    client = redis.Redis(host="localhost", port=6379, decode_responses=True)
    allowed, count, ttl = is_allowed(client, key)

    status = "ALLOW" if allowed else "DENY"
    print(f"{status}  count={count}/{LIMIT}  ttl={ttl}s  key={key}")


if __name__ == "__main__":
    main()
