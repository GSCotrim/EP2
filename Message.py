SOFT_BREAK = f'\n-------------------------------------------------------------------------------------------------\n'
HARD_BREAK = f'\n=================================================================================================\n'


class Message:
    def __init__(self, text=None):
        self.texts = []
        if text is not None:
            self.texts.append(text)

    def add(self, text):
        if text is not None:
            self.texts.append(text)

    def add_soft_texts(self, texts):
        if len(texts) > 0:
            self.texts.append(SOFT_BREAK.join(texts))

    def add_hard_texts(self, texts):
        if len(texts) > 0:
            self.texts.append(HARD_BREAK.join(texts))

    def add_soft_break(self):
        self.texts.append(SOFT_BREAK)

    def add_hard_break(self):
        self.texts.append(HARD_BREAK)

    def full_text(self):
        return "".join(self.texts)

    def show(self):
        for text in self.texts:
            print(text)

    def __str__(self):
        return "\n".join(self.texts)