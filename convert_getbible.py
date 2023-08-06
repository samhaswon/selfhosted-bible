import json
from bibles.compresscache import CompressCache

if __name__ == '__main__':
    abbreviation = 'bbe'
    filename = f'{abbreviation}.json'
    with open(filename, "r") as data_file:
        input_file = json.load(data_file)
    output = {}
    for book in input_file['books']:
        name = book['name']
        output[name] = {}
        for chapter in book['chapters']:
            chapter_number = chapter['chapter']
            output[name][chapter_number] = []
            for verse in chapter['verses']:
                output[name][chapter_number].append(f"{verse['verse']} {verse['text']}")

    compress_cache = CompressCache(abbreviation)
    compress_cache.save(output)
