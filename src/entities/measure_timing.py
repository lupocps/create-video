'''Module to measure the time of the videos'''

from datetime import timedelta

class MeasureTiming:
    '''A class to measure timing data for videos.

    Attributes:
        total_time (timedelta): The total time of all videos.
        videos_amount (int): The number of videos.

    '''
    def __init__(self):
        '''Initialize the MeasureTiming class.
        '''
        self.total_time = timedelta(minutes= 0, seconds=0)
        self.videos_amount = 0


    def add_time(self, time:timedelta):
        '''Add time of one video to the total time

        Parameters:
            time(timedelta): time of one video
        '''
        self.total_time += time


    def add_video_amount(self):
        '''Add one by one the video amount
        '''
        self.videos_amount += 1
