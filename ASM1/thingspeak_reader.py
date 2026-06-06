import urllib.request
import urllib.error
import json

CHANNEL_ID = 1529099
RESULTS = 2
URL = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?results={RESULTS}"


def fetch_feeds(url: str) -> dict | None:
    try:
        with urllib.request.urlopen(url) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw)
    except urllib.error.HTTPError as e:
        print(f"HTTP error {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        print(f"Connection error: {e.reason}")
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
    return None


def parse_and_display(data: dict) -> None:
    channel = data.get("channel", {})
    feeds = data.get("feeds", [])

    print(f"Channel : {channel.get('name', 'N/A')}")
    print(f"Results : {len(feeds)} entry(ies)")
    print("-" * 45)
    print(f"{'#':<4} {'Created At':<25} {'Temp (°C)':<12} {'Humidity (%)'}")
    print("-" * 45)

    for i, feed in enumerate(feeds, start=1):
        created_at  = feed.get("created_at", "N/A")
        temperature = feed.get("field1", "N/A")
        humidity    = feed.get("field2", "N/A")
        print(f"{i:<4} {created_at:<25} {temperature:<12} {humidity}")

    print("-" * 45)


if __name__ == "__main__":
    data = fetch_feeds(URL)
    if data:
        parse_and_display(data)
