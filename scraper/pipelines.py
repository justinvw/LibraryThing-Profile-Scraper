import os
from scrapy.conf import settings
from scraper.items import (LibraryThingUser, LibraryThingGroupMembership,
    LibraryThingUserConnection, LibraryThingLibraryItem)

class CSVExportPipeline(object):
    def open_spider(self, spider):
        csv_store = settings['CSV_STORE_LOCATION']

        # Open required file handlers
        self.users = open(os.path.join(csv_store, 'user_profiles.csv'), 'a')
        self.connections = open(os.path.join(csv_store, 'user_connections.csv'),
            'a')
        self.groups = open(os.path.join(csv_store, 'group_memberships.csv'), 'a')
        self.libraries = open(os.path.join(csv_store, 'user_libraries.csv'), 'a')

    def process_item(self, item, spider):
        item_file_mapping = {
            LibraryThingUser: self.users,
            LibraryThingUserConnection: self.connections,
            LibraryThingGroupMembership: self.groups,
            LibraryThingLibraryItem: self.libraries
        }

        csv_line = ';'.join([item.get(field, '') for field in item.field_order])
        csv_line = csv_line.encode('UTF-8')

        # Write item to correct file
        item_file_mapping[type(item)].write('%s\n' % csv_line)

        return item

    def close_spider(self, spider):
        # Close all opened file handlers
        self.users.close()
        self.connections.close()
        self.groups.close()
        self.libraries.close()
