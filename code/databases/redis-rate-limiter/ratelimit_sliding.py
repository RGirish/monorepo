import pathlib
import sys
import time
import uuid

import redis

LIMIT = 3
WINDOW_MS = 10_000
SCRIPT_PATH = pathlib.Path(__file__).parent / "sliding_window.lua"


def is_allowed(client: redis.Redis, script, key: str) -> tuple[bool, int]:
    now_ms = int(time.time() * 1000)
    member = f"{now_ms}-{uuid.uuid4().hex[:6]}"
    count = script(keys=[key], args=[now_ms, WINDOW_MS, LIMIT, member])
    return count <= LIMIT, count


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: python ratelimit_sliding.py <user_id>")
        sys.exit(1)

    user_id = sys.argv[1]
    key = f"ratelimit:sliding:{user_id}"

    client = redis.Redis(host="localhost", port=6379, decode_responses=True)
    script = client.register_script(SCRIPT_PATH.read_text())

    allowed, count = is_allowed(client, script, key)

    status = "ALLOW" if allowed else "DENY"
    print(f"{status}  count={count}/{LIMIT}  key={key}")


if __name__ == "__main__":
    main()
