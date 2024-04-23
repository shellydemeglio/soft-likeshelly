class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, message):
        for observer in self._observers:
            observer.update(message)


class FlashcardSubject(Subject):
    def __init__(self):
        super().__init__()
        self._flashcards = []

    def add_flashcard(self, flashcard):
        self._flashcards.append(flashcard)
        self.notify("New flashcard added")

    def remove_flashcard(self, flashcard):
        if flashcard in self._flashcards:
            self._flashcards.remove(flashcard)
            self.notify("Flashcard removed")


class Observer:
    def update(self, message):
        pass


class UserObserver(Observer):
    def __init__(self, name):
        self._name = name

    def update(self, message):
        print(f"User {self._name} received update: {message}")


# Example usage:
flashcard_subject = FlashcardSubject()

user1 = UserObserver("Alice")
user2 = UserObserver("Bob")

flashcard_subject.attach(user1)
flashcard_subject.attach(user2)

flashcard_subject.add_flashcard("What is the capital of France?")

flashcard_subject.remove_flashcard("What is the capital of France?")
