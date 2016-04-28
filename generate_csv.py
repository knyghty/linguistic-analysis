import csv
import os

from core import constants


with open(os.path.join(constants.HTML_DIR, 'classifications.csv'), 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['', 'Lexical', 'Syntactic', 'Semantic'])
    for row in range(103):
        writer.writerow(['Conversation {counter}'.format(counter=row + 1), '', '', ''])
