from scrapy.item import Item, Field

class LibraryThingUser(Item):
    field_order = ['profile_url', 'username', 'real_name', 'member_since',
        'about', 'about_library', 'hompage', 'account_type']

    profile_url = Field()
    username = Field()
    real_name = Field(default='')
    member_since = Field()
    about = Field(default='')
    about_library = Field(default='')
    homepage = Field(default='')
    account_type = Field(default='')

class LibraryThingGroupMembership(Item):
    field_order = ['profile_url', 'group_name', 'group_url']

    profile_url = Field()
    group_name = Field()
    group_url = Field()

class LibraryThingUserConnection(Item):
    field_order = ['source_profile_url', 'target_profile_url',
        'connection_type']

    source_profile_url = Field()
    target_profile_url = Field()
    connection_type = Field()

class LibraryThingLibraryItem(Item):
    field_order = ['profile_url', 'work_url', 'work_id', 'rating', 'date_added']

    profile_url = Field()
    work_url = Field()
    work_id = Field()
    rating = Field()
    date_added = Field()
