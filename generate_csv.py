import csv
import os


HTML_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'html')


with open(os.path.join(HTML_DIR, 'classifications.csv'), 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['', 'Lexical', 'Syntactic', 'Semantic'])
    for row in range(103):
        writer.writerow(['Conversation {counter}'.format(counter=row + 1), '', '', ''])
