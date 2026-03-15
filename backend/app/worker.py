import time


def run_worker() -> None:
    while True:
        time.sleep(60)


if __name__ == "__main__":
    run_worker()
