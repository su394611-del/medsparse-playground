"""Verify the installed launcher serves its page, worker and worker imports."""
from importlib.metadata import version
from tempfile import TemporaryFile
from urllib.parse import urljoin
from urllib.request import urlopen
import re
import subprocess
import sys
import time


def read(url):
    with urlopen(url, timeout=10) as response:
        return response.read().decode("utf-8")


with TemporaryFile(mode="w+", encoding="utf-8") as output:
    with subprocess.Popen(
        [sys.executable, "-c",
         "from medsparse_playground.cli import main; main()", "--no-browser"],
        stdout=output, stderr=output,
    ) as launcher:
        try:
            for _ in range(100):
                output.seek(0)
                text = output.read()
                match = re.search(r"^http://127\.0\.0\.1:\d+/$", text, re.M)
                if match:
                    break
                if launcher.poll() is not None:
                    raise RuntimeError(text)
                time.sleep(0.1)
            else:
                raise RuntimeError(f"Launcher did not report a URL: {text}")

            home = match.group()
            page = read(home)
            script = re.search(r'<script\b[^>]*\bsrc="([^"]*page-behavior\.js)"', page)
            assert script, "The playground page did not reference its behavior script"
            code = read(urljoin(home, script.group(1)))
            worker = re.search(r"""new Worker\(["']([^"']+)["']""", code)
            assert worker, "The behavior script did not reference a worker"
            # In a classic script the Worker URL is relative to the document, not the script.
            worker_url = urljoin(home, worker.group(1))
            worker_code = read(worker_url)
            engine = re.search(r"""importScripts\(["']([^"']+)["']""", worker_code)
            assert engine, "The worker did not reference its inference engine"
            assert read(urljoin(worker_url, engine.group(1))).strip()
            print(f"medsparse-playground {version('medsparse-playground')}: launcher, worker and engine OK")
        finally:
            launcher.terminate()
            launcher.wait(timeout=10)
