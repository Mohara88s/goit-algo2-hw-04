from trie import Trie

class Homework(Trie):
    def get_all_words(self, node=None, prefix=""):
        if node is None:
            node = self.root

        words = []
        if node.value is not None:
            words.append(prefix)

        for char, child_node in node.children.items():
            words.extend(self.get_all_words(child_node, prefix + char))

        return words
    
    def count_words_with_suffix(self, pattern) -> int:
        if not isinstance(pattern, str):
            raise ValueError("The suffix must be a string")
        
        count = sum(1 for word in self.get_all_words() if word.endswith(pattern))
        return count
    
    def has_prefix(self, prefix) -> bool:
        if not isinstance(prefix, str):
            raise ValueError("The prefix must be a string")
        
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]

        return True
    

if __name__ == "__main__":
    trie = Homework()
    words = ["apple", "application", "banana", "cat"]
    for i, word in enumerate(words):
        trie.put(word, i)

    # Перевірка кількості слів, що закінчуються на заданий суфікс
    assert trie.count_words_with_suffix("e") == 1  # apple
    assert trie.count_words_with_suffix("ion") == 1  # application
    assert trie.count_words_with_suffix("a") == 1  # banana
    assert trie.count_words_with_suffix("at") == 1  # cat

    # Перевірка наявності префікса
    assert trie.has_prefix("app") == True  # apple, application
    assert trie.has_prefix("bat") == False
    assert trie.has_prefix("ban") == True  # banana
    assert trie.has_prefix("ca") == True  # cat
