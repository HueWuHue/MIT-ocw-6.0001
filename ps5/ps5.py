# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


# -----------------------------------------------------------------------

# ======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
# ======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
        #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
        #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret


# ======================
# Data structure design
# ======================

# Problem 1

# TODO: NewsStory
class NewsStory():
    def __init__(self, guid, title, description, link, pubdate):
        self.__guid = guid
        self.__title = title
        self.__description = description
        self.__link = link
        self.__pubdate = pubdate

    def get_guid(self):
        return self.__guid

    def get_title(self):
        return self.__title

    def get_description(self):
        return self.__description

    def get_link(self):
        return self.__link

    def get_pubdate(self):
        return self.__pubdate


# ======================
# Triggers
# ======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError


# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.__phrase = phrase

    def get_phrase(self):
        return self.__phrase

    def is_phrase_in(self, story):
        state = False
        punct = string.punctuation
        txt = story.lower()
        for word in txt:
            if word in punct:
                txt = txt.replace(word, " ")
        text_list = self.get_phrase().lower().split()
        txt = txt.split()
        match = 0
        full_match = len(text_list)
        max_index = len(txt) - 1
        for num in range(len(txt)):
            if txt[num] == text_list[0]:
                for i in range(len(text_list)):
                    index = num + i
                    if index <= max_index:
                        if txt[index] == text_list[i]:
                            match += 1
                if match == full_match:
                    state = True
                else:
                    match = 0
        return state


# Problem 3
# TODO: TitleTrigger
class TitleTrigger(PhraseTrigger):
    def __init__(self, phrase):
        super().__init__(phrase)

    def evaluate(self, story):
        title = story.get_title()
        if self.is_phrase_in(title):
            return True


# Problem 4
# TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger):
    def __init__(self, phrase):
        super().__init__(phrase)

    def evaluate(self, story):
        title = story.get_description()
        if self.is_phrase_in(title):
            return True


# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
class TimeTrigger(Trigger):
    def __init__(self, time):
        time = datetime.strptime(time, "%d %b %Y %H:%M:%S")
        self.__time = time

    def get_time(self):
        return self.__time


# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    def __init__(self, time):
        super().__init__(time)

    def evaluate(self, story):
        pub_time = story.get_pubdate()
        if self.get_time() > pub_time:
            return True


class AfterTrigger(TimeTrigger):
    def __init__(self, time):
        super().__init__(time)

    def evaluate(self, story):
        pub_time = story.get_pubdate()
        if self.get_time() < pub_time:
            return True


# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.__trigger = trigger

    def get_trigger(self):
        return self.__trigger

    def evaluate(self, story):
        return not self.get_trigger().evaluate(story)


# Problem 8
# TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.__trigger1 = trigger1
        self.__trigger2 = trigger2

    def get_trigger1(self):
        return self.__trigger1

    def get_trigger2(self):
        return self.__trigger2

    def evaluate(self, story):
        return self.get_trigger1().evaluate(story) and self.get_trigger2().evaluate(story)


# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.__trigger1 = trigger1
        self.__trigger2 = trigger2

    def get_trigger1(self):
        return self.__trigger1

    def get_trigger2(self):
        return self.__trigger2

    def evaluate(self, story):
        return self.get_trigger1().evaluate(story) or self.get_trigger2().evaluate(story)


# ======================
# Filtering
# ======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    filtered_stories = []
    for triggers in triggerlist:
        for story in stories:
            if triggers.evaluate(story):
                filtered_stories.append(story)
                break
    return filtered_stories


# ======================
# User-Specified Triggers
# ======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    trigger_list = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers
    trigger_dict = {'title':TitleTrigger,'description':DescriptionTrigger,'after':AfterTrigger,'and':AndTrigger}
    for i in range(len(lines)):
        lines[i] = lines[i].split(",")
    for i in range(5):
        list = lines[i]
        var = list[0]
        object_class = trigger_dict[list[1].lower()]
        intake = list[2]

        if len(list) > 3:
            intake2 = list[3]
            var = object_class(intake,intake2)
        else:
            var = object_class(intake)
        trigger_list.append(var)

    return trigger_list

SLEEPTIME = 120  # seconds -- how often we poll


def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("Singapore")
        t2 = DescriptionTrigger("")
        t3 = DescriptionTrigger("")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        #triggerlist = read_trigger_config('triggers.txt')

        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT, fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica", 14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []

        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title() + "\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:
            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)

            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    read_trigger_config("triggers.txt")
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()
