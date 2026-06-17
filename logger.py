from datetime import datetime


class Logger:

    LOG_FILE = "organizer_log.txt"

    @staticmethod
    def log(message):

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        with open(
            Logger.LOG_FILE,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(
                f"[{timestamp}] {message}\n"
            )