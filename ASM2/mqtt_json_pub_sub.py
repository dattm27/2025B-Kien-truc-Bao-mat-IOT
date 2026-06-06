#!/usr/bin/env python3
import argparse
import json
import threading
import uuid
from datetime import datetime
from pathlib import Path

import paho.mqtt.client as mqtt


DEFAULT_BROKER = "broker.hivemq.com"
DEFAULT_PORT = 1883
DEFAULT_TOPIC = f"asm2/mqtt-json-demo/{uuid.uuid4().hex}"
DEFAULT_DATA_FILE = Path(__file__).with_name("data.json")


def load_json_payload(data_file):
    with open(data_file, "r", encoding="utf-8") as file:
        return json.load(file)


def local_timestamp():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def display_fields(payload):
    print("Retrieved data:")
    print(f"DeviceName  : {payload.get('DeviceName')}")
    print(f"temperature : {payload.get('temperature')}")
    print(f"humidity    : {payload.get('humidity')}")
    if "timestamp" in payload:
        print(f"timestamp   : {payload.get('timestamp')}")


def publish_payload(client, args, payload, message_received):
    message_payload = payload.copy()
    message_payload["timestamp"] = local_timestamp()
    json_payload = json.dumps(message_payload)
    result = client.publish(args.topic, json_payload, qos=1)
    if result.rc != mqtt.MQTT_ERR_SUCCESS:
        print(f"Publish request failed with result code: {result.rc}")
        message_received.set()
        return

    print(f"Publish time (local): {message_payload['timestamp']}")
    print(f"Publish request sent to topic {args.topic}: {json_payload}")


def build_client(args, payload, message_received):
    client_id = f"python-mqtt-json-{uuid.uuid4().hex[:8]}"
    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id=client_id,
    )

    def on_connect(client, userdata, flags, reason_code, properties):
        if reason_code != 0:
            print(f"Connection failed with reason code: {reason_code}")
            message_received.set()
            return

        print(f"Connected to {args.broker}:{args.port}")
        if args.mode == "publish":
            publish_payload(client, args, payload, message_received)
            return

        result, message_id = client.subscribe(args.topic)
        if result != mqtt.MQTT_ERR_SUCCESS:
            print(f"Subscribe request failed with result code: {result}")
            message_received.set()
            return

        print(f"Subscribe request sent for topic: {args.topic}")

    def on_subscribe(client, userdata, message_id, reason_codes, properties):
        print(f"Subscribed to topic: {args.topic}")

        if args.mode == "both":
            publish_payload(client, args, payload, message_received)

    def on_publish(client, userdata, message_id, reason_code, properties):
        print(f"Publish confirmed by broker. Message id: {message_id}")
        if args.mode == "publish":
            message_received.set()

    def on_message(client, userdata, message):
        print(f"\nMessage received from topic: {message.topic}")
        print(f"Receive time (local): {local_timestamp()}")
        try:
            decoded_message = message.payload.decode("utf-8")
            received_payload = json.loads(decoded_message)
        except UnicodeDecodeError:
            print("Could not decode MQTT payload as UTF-8 text.")
        except json.JSONDecodeError:
            print("Could not parse MQTT payload as JSON.")
            print(f"Raw payload: {message.payload!r}")
        else:
            display_fields(received_payload)
        finally:
            if args.mode != "subscribe" or args.timeout > 0:
                message_received.set()

    def on_disconnect(client, userdata, disconnect_flags, reason_code, properties):
        if reason_code != 0 and not message_received.is_set():
            print(f"Disconnected before receiving data. Reason code: {reason_code}")
            message_received.set()

    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_publish = on_publish
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    return client


def parse_args():
    parser = argparse.ArgumentParser(
        description="Publish JSON data to an MQTT broker, subscribe, parse it, and display fields."
    )
    parser.add_argument(
        "--mode",
        choices=["publish", "subscribe", "both"],
        default="both",
        help="Run as publisher only, subscriber only, or both in one process",
    )
    parser.add_argument("--broker", default=DEFAULT_BROKER, help="MQTT broker hostname")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="MQTT broker port")
    parser.add_argument("--topic", default=DEFAULT_TOPIC, help="MQTT topic to publish and subscribe")
    parser.add_argument(
        "--data-file",
        default=str(DEFAULT_DATA_FILE),
        help="Path to JSON file containing DeviceName, temperature, and humidity",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=60.0,
        help="Seconds to wait; use 0 to wait forever",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    payload = None
    if args.mode in ("publish", "both"):
        payload = load_json_payload(args.data_file)

    message_received = threading.Event()
    client = build_client(args, payload, message_received)

    client.connect(args.broker, args.port, keepalive=60)
    client.loop_start()

    try:
        if args.timeout <= 0:
            print("Waiting for MQTT messages. Press Ctrl+C to stop.")
            message_received.wait()
        elif not message_received.wait(args.timeout):
            waiting_for = "publish confirmation" if args.mode == "publish" else "MQTT message"
            print(f"No {waiting_for} received within {args.timeout} seconds.")
    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
