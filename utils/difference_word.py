from difflib import SequenceMatcher


def difference_word(original_text="", beta_text=""):
    # Chuyển văn bản thành danh sách các từ
    original_words = original_text.split()
    beta_words = beta_text.split()

    # Tạo trình so khớp chuỗi
    matcher = SequenceMatcher(None, original_words, beta_words)
    modified_count = 0

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag in {'replace', 'delete', 'insert'}:
            modified_count += max(i2 - i1, j2 - j1)
    return modified_count
