"""Фильтр алертов: из events.json оставляем только critical."""
import json
import sys


def critical(events):
    return [e for e in events if e.get("level") == "critical"]


def demo():
    assert [e["id"] for e in critical(json.load(open("events.json", encoding="utf-8")))] == [1, 4, 6]
    assert critical([{"level": "warn"}, {}]) == []
    print("self-check ok")


if __name__ == "__main__":
    if "--test" in sys.argv:
        demo()
    else:
        path = sys.argv[1] if len(sys.argv) > 1 else "events.json"
        with open(path, encoding="utf-8") as f:
            events = json.load(f)
        alerts = critical(events)
        for e in alerts:
            print(f"[{e['level']}] #{e['id']} {e['message']}")
        print(f"критичных {len(alerts)}")
