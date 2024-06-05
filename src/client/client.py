from typing import List
import os
from book_management import BookManager


class Client:

    @staticmethod
    def clear_console() -> None:
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def display_menu_and_get_choice() -> int:
        options = {
            1: "Add a single book",
            2: "Add books",
            3: "Exit"
        }

        print("Choose an option: ")
        for key, value in options.items():
            print(f"[{key}] {value}")

        choice = input("Enter your choice: ").strip()
        return int(choice) if choice.isdigit() and int(choice) in options else Client.display_menu_and_get_choice()

    @staticmethod
    def get_genres_from_user() -> str:
        genres = input("Enter the genres you want to add (format: genre genre): ").strip().split()
        return "".join([f"/genres/{genre}" for genre in genres]) if genres else ""

    @staticmethod
    def get_authors_from_user() -> List[str]:
        authors = input("Enter the authors you want to add (format: name-lastname name-secondname-lastname): ").strip().lower().split()
        return [f'/authors/{author}' for author in authors] if authors else []

    @staticmethod
    def process_single_book_addition() -> None:
        title = input("Enter the title of the book: ").strip()

        if book := BookManager.find_book_by_title(title):
            BookManager.submit_book_to_api(book)
            input("Press any key to go back to the menu")
        else:
            print("Book not found")

    @staticmethod
    def process_bulk_book_addition() -> None:
        genres = Client.get_genres_from_user()
        authors = Client.get_authors_from_user()

        if books := BookManager.fetch_filtered_books(authors, genres):
            BookManager.add_books_to_db(books)
        else:
            print("Books not found")
            return

        input("Press any key to go back to the menu")

    @staticmethod
    def main() -> None:
        while True:
            Client.clear_console()
            choice = Client.display_menu_and_get_choice()

            if choice == 1:
                Client.clear_console()
                Client.process_single_book_addition()
            elif choice == 2:
                Client.clear_console()
                Client.process_bulk_book_addition()
            elif choice == 3:
                print("Exiting")
                break


if __name__ == "__main__":
    Client.main()
