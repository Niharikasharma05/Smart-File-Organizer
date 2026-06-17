from organizer import FileOrganizer


def main():

    print("""
        ====================================
            SMART FILE ORGANIZER PRO
        ====================================
        Automate file sorting with ease.
    """)

    folder_path = input(
        "Enter folder path: "
    )

    try:

        organizer = FileOrganizer(
            folder_path
        )

        stats = organizer.organize()

        print("\n====================================")
        print("      ORGANIZATION COMPLETE")
        print("====================================\n")

        for category, count in stats.items():

            print(
                f"{category:<12} : {count}"
            )

        if organizer.duplicates:

            print("\nDuplicate Files Detected:")

            for duplicate in organizer.duplicates:

                print(f"• {duplicate}")

        print(
            "\nLog file created successfully."
        )

        choice = input(
            "\nUndo operation? (y/n): "
        ).lower()

        if choice == "y":

            organizer.undo()

            print(
                "\nFiles restored successfully."
            )

    except FileNotFoundError:

        print(
            "\nFolder not found."
        )

    except Exception as error:

        print(
            f"\nError: {error}"
        )


if __name__ == "__main__":
    main()