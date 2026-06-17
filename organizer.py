import os
import shutil
import hashlib

from logger import Logger


class FileOrganizer:

    FILE_TYPES = {

        "Images": [
            ".jpg",
            ".jpeg",
            ".png",
            ".gif"
        ],

        "Documents": [
            ".pdf",
            ".doc",
            ".docx",
            ".txt"
        ],

        "Videos": [
            ".mp4",
            ".mkv",
            ".avi"
        ],

        "Music": [
            ".mp3",
            ".wav"
        ],

        "Archives": [
            ".zip",
            ".rar"
        ]
    }

    def __init__(self, folder_path):

        self.folder_path = folder_path
        self.file_hashes = {}
        self.duplicates = []
        self.undo_moves = []

        self.stats = {
            "Images": 0,
            "Documents": 0,
            "Videos": 0,
            "Music": 0,
            "Archives": 0,
            "Others": 0
        }

    def get_category(self, extension):

        for category, extensions in self.FILE_TYPES.items():

            if extension.lower() in extensions:
                return category

        return "Others"
    
    def get_file_hash(self, filepath):

        hasher = hashlib.md5()

        with open(filepath, "rb") as file:

            chunk = file.read(4096)

            while chunk:

                hasher.update(chunk)

                chunk = file.read(4096)

        return hasher.hexdigest()

    def is_duplicate(self, filepath):
        file_hash = self.get_file_hash(filepath)
        if file_hash in self.file_hashes:

            self.duplicates.append(
                os.path.basename(filepath)
            )

            return True

        self.file_hashes[file_hash] = filepath

        return False

    def organize(self):

        files = os.listdir(self.folder_path)

        for file in files:

            source = os.path.join(
                self.folder_path,
                file
            )

            if os.path.isdir(source):
                continue

            if self.is_duplicate(source):
                Logger.log(
                f"Duplicate detected: {file}"
            )
                continue

            extension = os.path.splitext(file)[1]

            category = self.get_category(
                extension
            )

            destination_folder = os.path.join(
                self.folder_path,
                category
            )

            os.makedirs(
                destination_folder,
                exist_ok=True
            )

            destination = os.path.join(
                destination_folder,
                file
            )

            shutil.move(
                source,
                destination
            )

            self.undo_moves.append(
                (
                    destination,
                    source
                )
            )

            self.stats[category] += 1

            Logger.log(
                f"Moved {file} to {category}"
            )
        
        return self.stats
        
    def undo(self):

        for destination, source in reversed(
            self.undo_moves
        ):

            if os.path.exists(destination):

                shutil.move(
                    destination,
                    source
                )

        Logger.log(
            "Undo operation completed"
        )
