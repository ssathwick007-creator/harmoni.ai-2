import json
import threading
import time
import unittest
from http import HTTPStatus
from urllib.error import HTTPError
from urllib.request import urlopen

from harmoni_ai.app import HarmoniRequestHandler, ThreadingHTTPServer


class ServerThread(threading.Thread):
    def __init__(self, host: str = "127.0.0.1", port: int = 0):
        super().__init__(daemon=True)
        self.server = ThreadingHTTPServer((host, port), HarmoniRequestHandler)

    @property
    def url(self) -> str:
        host, port = self.server.server_address
        return f"http://{host}:{port}"

    def run(self) -> None:
        self.server.serve_forever()

    def stop(self) -> None:
        self.server.shutdown()
        self.server.server_close()


class TestHarmoniServer(unittest.TestCase):
    def setUp(self) -> None:
        self.server = ServerThread()
        self.server.start()
        time.sleep(0.05)

    def tearDown(self) -> None:
        self.server.stop()

    def test_health_endpoint(self) -> None:
        with urlopen(f"{self.server.url}/health") as response:
            self.assertEqual(response.status, HTTPStatus.OK)
            payload = json.loads(response.read())
            self.assertEqual(payload["status"], "ok")

    def test_root_endpoint(self) -> None:
        with urlopen(f"{self.server.url}/") as response:
            self.assertEqual(response.status, HTTPStatus.OK)
            payload = json.loads(response.read())
            self.assertIn("endpoints", payload)
            self.assertIn("/health", payload["endpoints"])

    def test_missing_endpoint(self) -> None:
        with self.assertRaises(HTTPError) as err:
            urlopen(f"{self.server.url}/missing")
        self.assertEqual(err.exception.code, HTTPStatus.NOT_FOUND)


if __name__ == "__main__":
    unittest.main()
