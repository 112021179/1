import csv
import os
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
import threading
import queue
import time

data_queue = queue.Queue()

def get_ex_chinese(i, table):
    example = table.find_all('div', class_='tradchinese')[i - 1].text
    return example.replace('\u200b', '')


def get_ex_translation(i, table):
    ex_translation = table.find_all('div', class_='translation')[i - 1].text
    return ex_translation


def filtering_chinese(i, char_list, table):
    ex_translation = get_ex_translation(i, table)
    if 'phr.' not in ex_translation:
        return [0, '--', '--']

    example = get_ex_chinese(i, table)

    if any(char in example for char in char_list) or len(example) > 8:
        return len(example), example, ex_translation.replace('phr. ', '')
    return [0, '--', '--']

def get_examples(num_tr_elements, char_list, table):
    if num_tr_elements == 0:
        return [0, '--', '--'], [0, '--', '--']

    if num_tr_elements == 1:
        return filtering_chinese(1, char_list, table), [0, '--', '--']

    example1 = filtering_chinese(1, char_list, table)
    example2 = filtering_chinese(2, char_list, table)
    if num_tr_elements == 2:
        if example1 != [0, '--', '--'] and example1 is not None:
            return example1, example2
        return example2, example1
    pairs = []
    if example1 != [0, '--', '--'] and example1 is not None:
        pairs.append(example1)
        
    if example2 != [0, '--', '--'] and example2 is not None:
        pairs.append(example2)
        
    for i in range(3, num_tr_elements + 1):

        pair = filtering_chinese(i, char_list, table)
        if pair != [0, '--', '--'] and pair is not None:
            pairs.append(pair)
    if len(pairs) == 0:
        return [0, '--', '--'], [0, '--', '--']
    if len(pairs) == 1:
        return pairs[0], [0, '--', '--']
    
    pairs = sorted(pairs, key=lambda x: x[0], reverse=True)
    longest_pairs = tuple(pair for pair in pairs[:2])
    return longest_pairs
    

def enqueue_data(data):
    data_queue.put(data)

def bulk_save_to_csv(filename):
    with open(filename, 'a', newline='', encoding='utf-8') as file:
        writer = None
        while not data_queue.empty():
            data = data_queue.get()
            if writer is None:
                writer = csv.DictWriter(file, fieldnames=data.keys(), delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
                if os.stat(filename).st_size == 0:
                    writer.writeheader()
            writer.writerow(data)

def collect_data(word, transcription, translation, example1, ex_translation1, example2, ex_translation2):
    
    return {
        'word': word,
        'transcription': transcription,
        'translation': translation,
        'example1': example1,
        'ex.translaton1': ex_translation1,
        'example2': example2,
        'ex.translaton2': ex_translation2
    }

def get_soup(word, word_id, session):
    
    if word_id:
        url = f'https://www.trainchinese.com/v2/wordDetails.php?rAp=0&wordId={word_id}&tcLanguage=en'
        response = session.get(url)
        source_code = response.text
        soup = BeautifulSoup(source_code, 'lxml')
        return soup
    
    if word == '台灣':
        url = f"https://www.trainchinese.com/v2/search.php?searchWord=臺灣&tcLanguage=en"
    
    else:
        url = f"https://www.trainchinese.com/v2/search.php?searchWord={word}&tcLanguage=en"
    response = session.get(url)
    source_code = response.text
    soup = BeautifulSoup(source_code, 'lxml')
    return soup

def get_td_element(soup, word):
    td_element = soup.find_all('td')
    if len(td_element) == 0:
        print(f'nothing was found for this word {word}')
        return None
    return td_element

def get_wordid(td_element):
    word_id = re.search(r'\d+', td_element['onclick']).group()
    return word_id

def get_translation(td_element):
    translation = td_element.find('span', style='color:#0066FF').text.strip()
    return translation

def get_transcription(td_element):
    transcription = td_element.find('span', class_ = 'pinyin').text.strip()
    return transcription
 
def check_the_word(word):
    if word[-1] == ' ':
        return (word.strip(), 2) 
    if '/' in word:
        return (word.split('/')[0], 1)
    return (word, 1)

def get_the_table(soup2):
    table = soup2.find_all('table', class_='table')
    if len(table) == 0:
        return None
    if len(table) == 1 and soup2.find('div', class_='panel-heading').text == 'Other meanings':
        return None
    if len(table) == 1:
        return table[0]
    return table[1]

def process_word(char_list, row, session):
        word = row['word']
        
        checked_word = check_the_word(word)
        soup = get_soup(checked_word[0], None, session)
        
        
        td_element = get_td_element(soup, word)
        soup = None
        if td_element is None:
            data = collect_data(word, '--', '--', '--', '--', '--', '--')
            enqueue_data(data)
            return
        
        if checked_word[1] == 2:
            word_id = get_wordid(td_element[3])
            translation = get_translation(td_element[3])
            transcription = get_transcription(td_element[3])
        else:
            word_id = get_wordid(td_element[0])
            translation = get_translation(td_element[0])
            transcription = get_transcription(td_element[0])
        soup2 = get_soup('', word_id, session)

        table = get_the_table(soup2)
        soup2 = None
        if table is None:
            data = collect_data(word, transcription, translation, '--', '--', '--', '--')
            enqueue_data(data)
            return

        tr_elements = table.find_all('tr')
        
        num_tr_elements = len(tr_elements)
        pairs = get_examples(num_tr_elements, char_list, table)

        example1 = pairs[0][1]
        ex_translation1 = pairs[0][2]
        example2 = pairs[1][1]
        ex_translation2 = pairs[1][2]

        data = collect_data(word, transcription, translation, example1, ex_translation1, example2, ex_translation2)
            
        enqueue_data(data)
        return
        
def thread_function(char_list, df):
    with requests.Session() as session:
        for index, row in df.iterrows():
            start = time.time()
            
            process_word(char_list, row, session)
            end = time.time()
            print(f"Time taken for word {row['word']}: {end - start}")
        
def main():
    
    file_path = "try.csv"
    char_list = ['​。', '​？', '.', '！']
    char_list = [char.replace('\u200b', '') for char in char_list]
    df = pd.read_csv(file_path)
        
    num_threads = 20
    threads = []
    chunk_size = len(df) // num_threads
    remaining = len(df) % num_threads
    if remaining > 0:
        threads.append(threading.Thread(target=thread_function, args=(char_list, df[-remaining:])))
        threads[-1].start()
    for i in range(num_threads):
        start = i * chunk_size
        end = start + chunk_size 
        thread = threading.Thread(target=thread_function, args=(char_list, df[start:end]))
        threads.append(thread)
        thread.start()
        
    for thread in threads:
        thread.join()
    bulk_save_to_csv('output.csv')
    print('Done')
    
    
if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(f"Time taken: {end - start}")
