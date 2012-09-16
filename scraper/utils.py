import os
from scrapy.conf import settings

def parse_seedlist(path_to_file=settings['PROFILE_SEEDLIST']):
    with open(path_to_file, 'r') as seedlist:
        profiles = [profile.rstrip('\n') for profile in seedlist]

    return profiles

def get_crawled_profiles(csv_store=settings['CSV_STORE_LOCATION']):
    profiles = set()

    try:
        with open(os.path.join(csv_store, 'user_profiles.csv'), 'r') as users:
            [profiles.add(user.split(';')[0]) for user in users]
    except IOError:
        pass

    return profiles
