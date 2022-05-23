from reportlab.pdfgen.canvas import Canvas
import random
import bs4
import requests


# Applies the fizz buzz algorithm to the first 100 positive integers
def fizz_buzz():

    for num in range(1, 101):

        fizz = False
        buzz = False
        result = ''

        if num % 3 == 0:
            result += 'Fizz'
            fizz = True

        if num % 5 == 0:
            result += 'Buzz'
            buzz = True

        if not fizz and not buzz:
            result += str(num)

        print(result)


# Reverses a given string
def reverse_string(user_string):

    return user_string[::-1]


# Translates an english word to its pig-latin equivalent
def pig_latin(word):

    word = word.lower()
    vowels = 'aeiou'

    if word[0] in vowels:

        return word + '-yay'

    else:

        ending = '-{}ay'.format(word[0])

        return word[1:] + ending


# Counts the number of vowels in a given word
def count_vowels(word):

    vowels = 'aeiou'
    num_vowels = 0

    for letter in word:

        if letter in vowels:
            num_vowels += 1

    return num_vowels


# Determines whether or not the given word is a palindrome
def is_palindrome(word):

    return word == word[::-1]


# Counts the number of words in a given string
def word_count(user_string):

    return len(user_string.split())


# User answers ten randomly selected questions, and obtains a pdf file containing a breakdown of their results
def quiz_interface(quiz_file, key_file):

    nums = [x for x in range(10)]
    random.shuffle(nums)
    questions = []
    answers = []
    user_score = 0
    q_and_a = {}

    with open(quiz_file, 'r') as quiz:

        questions.extend(quiz.readlines())

    with open(key_file, 'r') as key:

        answers.extend(key.readlines())

    total_questions = len(questions)

    for num in nums:

       q_and_a[questions[num].strip()] = [input(questions[num]), answers[num].strip()]

    for q, a in q_and_a.items():

        if a[0].lower() == a[1]:

            user_score += 1

    score_percent = round(user_score / total_questions, 2) * 100
    fractional_score = 'Fractional Score: {}/{}'.format(user_score, total_questions)
    percentage_score = 'Percentage Score: {}%'.format(score_percent)

    results = Canvas('quiz_results.pdf')
    results.setFont('Courier', 12)
    results.drawString(260, 780, 'Quiz Results')
    x_q = 80
    y_q = 720
    x_a = 100
    y_a = 690
    q_num = 1

    for q, a in q_and_a.items():

        q_tag = "{}) ".format(q_num)
        results.drawString(x_q, y_q, q_tag + q)
        q_num += 1

        results.drawString(x_a, y_a, a[0])
        results.drawString(x_a + 350, y_a, '{}'.format(a[0].lower() == a[1]))

        y_a -= 60
        y_q -= 60

    results.drawString(190, y_a, fractional_score)
    results.drawString(190, y_a-30, percentage_score)
    results.save()


# A simple web scraper that utilizes the beautiful soup web scraping library (only works on the default site)
def page_scraper(site_url='http://quotes.toscrape.com/'):

    base_url = 'http://quotes.toscrape.com/page/{}/'
    page_index = 1
    has_quotes = True
    all_quotes = []
    all_authors = []

    while has_quotes:

        page_url = base_url.format(page_index)
        page_info = requests.get(page_url)
        page_soup = bs4.BeautifulSoup(page_info.text, 'lxml')
        page_quotes = page_soup.select('.text')
        page_authors = page_soup.select('.author')

        if len(page_quotes) == 0:

            has_quotes = False

        for quote in page_quotes:

            all_quotes.append(quote.text)

        for author in page_authors:

            all_authors.append(author.text)

        page_index += 1

    print('All quotes from {}:'.format(site_url))

    i = 0

    while i < len(all_quotes):

        print('\n{}'.format(all_quotes[i]))
        print('- {}'.format(all_authors[i]))
        i += 1

    sort_key = input('\nPlease enter a keyword to search the quotes by:  \n')

    q = 0
    matches = 0

    while q < len(all_quotes):

        if sort_key in all_quotes[q].split() or sort_key in all_authors[q].split():

            print()
            print(all_quotes[q])
            print('- {}'.format(all_authors[q]))
            matches += 1

        q += 1

    if matches == 0:

        print('Sorry, no quotes containing your keyword were found')
