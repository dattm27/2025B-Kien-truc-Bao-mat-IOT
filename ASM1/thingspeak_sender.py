import urllib.request
import urllib.parse
import urllib.error
import http.client
import json

API_KEY = "T7H40F0X82VGW7L5"
BASE_URL = "api.thingspeak.com"

FIELD1_VALUE = 20
FIELD2_VALUE = 33


# ============================================================
# Method a: GET request - data packed in URL (urlencoded)
# GET https://api.thingspeak.com/update?api_key=...&field1=20&field2=33
# ============================================================
def send_get_urlencoded(api_key: str, field1: int, field2: int) -> None:
    params = urllib.parse.urlencode({
        "api_key": api_key,
        "field1": field1,
        "field2": field2,
    })
    url = f"https://{BASE_URL}/update?{params}"

    print("=" * 60)
    print("Method a: GET request with URL parameters (urlencoded)")
    print(f"URL: {url}")

    try:
        with urllib.request.urlopen(url) as response:
            body = response.read().decode("utf-8")
            print(f"Status: {response.status} {response.reason}")
            print(f"Entry ID returned: {body}")
    except urllib.error.HTTPError as e:
        print(f"HTTP error {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        print(f"Connection error: {e.reason}")


# ============================================================
# Method b: POST request - data packed in request body (urlencoded)
# POST https://api.thingspeak.com/update
# Content-Type: application/x-www-form-urlencoded
# Body: api_key=...&field1=20&field2=33
# ============================================================
def send_post_urlencoded(api_key: str, field1: int, field2: int) -> None:
    payload = urllib.parse.urlencode({
        "api_key": api_key,
        "field1": field1,
        "field2": field2,
    }).encode("utf-8")

    url = f"https://{BASE_URL}/update"

    print("=" * 60)
    print("Method b: POST request with urlencoded body")
    print(f"URL: {url}")
    print(f"Body: {payload.decode()}")

    request = urllib.request.Request(
        url,
        data=payload,
        method="POST",
    )
    request.add_header("Content-Type", "application/x-www-form-urlencoded")

    try:
        with urllib.request.urlopen(request) as response:
            body = response.read().decode("utf-8")
            print(f"Status: {response.status} {response.reason}")
            print(f"Entry ID returned: {body}")
    except urllib.error.HTTPError as e:
        print(f"HTTP error {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        print(f"Connection error: {e.reason}")


if __name__ == "__main__":
    print("Sending data to ThingSpeak")
    print(f"field1={FIELD1_VALUE}, field2={FIELD2_VALUE}\n")

    # send_get_urlencoded("T7H40F0X82VGW7L5", 20, 33)
    print()
    send_post_urlencoded("T7H40F0X82VGW7L5", 20, 33)
    # print("=" * 60)
