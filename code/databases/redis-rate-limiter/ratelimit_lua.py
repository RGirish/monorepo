import pathlib
import sys

import redis

LIMIT = 3
WINDOW_SECONDS = 10
SCRIPT_PATH = pathlib.Path(__file__).parent / "rate_limit.lua"


def is_allowed(client: redis.Redis, script, key: str) -> tuple[bool, int, int]:
    count = script(keys=[key], args=[WINDOW_SECONDS])
    ttl = client.ttl(key)
    return count <= LIMIT, count, ttl


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: python ratelimit_lua.py <user_id>")
        sys.exit(1)

    user_id = sys.argv[1]
    key = f"ratelimit:{user_id}"

    client = redis.Redis(host="localhost", port=6379, decode_responses=True)
    script = client.register_script(SCRIPT_PATH.read_text())

    allowed, count, ttl = is_allowed(client, script, key)

    status = "ALLOW" if allowed else "DENY"
    print(f"{status}  count={count}/{LIMIT}  ttl={ttl}s  key={key}")


if __name__ == "__main__":
    main()
