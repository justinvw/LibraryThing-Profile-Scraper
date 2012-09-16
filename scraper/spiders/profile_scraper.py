import dateutil.parser
from scrapy.conf import settings
from scrapy.http import Request
from scrapy.http.cookies import CookieJar
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scraper.utils import parse_seedlist, get_crawled_profiles
from scraper.items import (LibraryThingUser, LibraryThingGroupMembership,
    LibraryThingUserConnection, LibraryThingLibraryItem)


class ProfileScraper(BaseSpider):
    name = 'Librarything User Profiles'

    start_urls = parse_seedlist()
    crawled_profiles = get_crawled_profiles()
    print crawled_profiles

    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        is_crawled = False
        if response.url in self.crawled_profiles:
            is_crawled = True

        if not is_crawled:
            user = LibraryThingUser()
            user['profile_url'] = response.url
            user['username'] = response.url.split('/')[-1]

            for item in hxs.select('//div[@class="profile"]/p'):
                item_type = item.select('./span/text()').extract()

                if item_type:
                    item_type = item_type[0]
                else:
                    item_type = None

                if item_type == 'Real name':
                    user['real_name'] = item.select('./text()').extract()[0]

                if item_type == 'Member since':
                    user['member_since'] = str(dateutil.parser.parse(\
                        item.select('./text()').extract()[0]).date())

                if item_type == 'About me':
                    about = item.select('./text()').extract()
                    if about:
                        user['about'] = about[0]

                if item_type == 'About my library':
                    about_library = item.select('./text()').extract()
                    if about_library:
                        user['about_library'] = about_library[0]

                if item_type == 'Homepage':
                    hompage = item.select('.//@href').extract()
                    if hompage:
                        user['homepage'] = hompage[0]

                if item_type == 'Account type':
                    account_type = item.select('./text()').extract()
                    if account_type:
                        user['account_type'] = account_type[0]

                if item_type == 'Groups':
                    for group in item.select('a'):
                        g_member = LibraryThingGroupMembership()
                        g_member['profile_url'] = response.url
                        g_member['group_name'] = group.select('text()')\
                            .extract()[0]
                        g_member['group_url'] = 'http://www.librarything.com%s'\
                            % group.select('@href').extract()[0]

                        yield g_member
            yield user

        # Extract 'friends' and 'Interesting library' connections
        for greenbox in hxs.select("//div[@class='greenbox']"):
            # Skip other 'greenboxes'
            if greenbox.select('.//h2/text()').extract()[0] != \
                                'Member connections':
                continue

            for p in greenbox.select('.//p'):
                connection_type = p.select('./b/text()').extract()
                if connection_type:
                    if connection_type[0] == 'Friends:':
                        connection_type = 'friend'
                    elif connection_type[0] == 'Interesting library:':
                        connection_type = 'interesting_library'
                    # Skip other types of connections
                    else:
                        continue

                for connection in p.select('a'):
                    user_connection = LibraryThingUserConnection()
                    user_connection['source_profile_url'] = response.url
                    user_connection['target_profile_url'] = \
                        'http://www.librarything.com%s'\
                        % connection.select('@href').extract()[0]
                    user_connection['connection_type'] = connection_type

                    if settings['FOLLOW_USER_CONNECTIONS'] and\
                            user_connection['target_profile_url'] not in\
                            self.crawled_profiles:
                        yield Request(user_connection['target_profile_url'])

                    if not is_crawled:
                        yield user_connection
                    else:
                        del user_connection

        if not is_crawled:
            self.crawled_profiles.add(response.url)
            yield Request('http://www.librarything.com/catalog_bottom.php?view=%s'\
                % user['username'], meta={'profile_url': response.url,
                'dont_merge_cookies': True},
                callback=self.scrape_library)

    def scrape_library(self, response):
        profile_url = response.meta['profile_url']
        hxs = HtmlXPathSelector(response)

        for item in hxs.select('//div[@id="content"]/table[@id="lt_catalog_list"]/tbody/tr'):
            book = LibraryThingLibraryItem()
            book['profile_url'] = profile_url

            cells = item.select('td')
            book['work_url'] = 'http://www.librarything.com%s'\
                % cells[1].select('.//a/@href').extract()[0]
            book['work_id'] = book['work_url'].split('/')[-3]
            book['rating'] = cells[5].select('.//input/@value').extract()[0]
            book['date_added'] = str(dateutil.parser.parse(cells[6]\
                .select('.//text()') .extract()[0]).date())

            yield book

        next_page = hxs.select('//div[@id="content"]/table//nobr/a[contains(text(), "next page")]')
        if next_page:
            cookie_jar = response.meta.setdefault('cookie_jar', CookieJar())
            cookie_jar.extract_cookies(response, response.request)

            request = Request('http://www.librarything.com%s'\
                % next_page.select('@href').extract()[0],
                meta={'profile_url': profile_url, 'dont_merge_cookies': True,\
                'cookie_jar': cookie_jar}, callback=self.scrape_library)
            cookie_jar.add_cookie_header(request)
            yield request


