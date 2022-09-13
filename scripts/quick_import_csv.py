import csv
import os
from settings import BASE_DIR
from tracks.models import Artist


def run():
    with open(os.path.join(BASE_DIR, 'scripts', 'quick_import_csv.csv')) as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)

        for row in reader:
            try:
                if row[1]:
                    artist, created = Artist.objects.get_or_create(name=row[1])
                    # print(created)
            except:
                print('whoops')
