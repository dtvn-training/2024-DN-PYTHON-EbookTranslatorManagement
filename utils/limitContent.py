def limit_content(content="", max_words=1000):
    content = content.split(' ')
    content = " ".join(content[:max_words])
    return content
