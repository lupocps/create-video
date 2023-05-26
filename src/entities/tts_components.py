
'''Module with components of text-to-speech service.
'''
class TTSComponents:
    '''This class contain the voice speaker, speed and pitch of the course

        Attributes:
            course_speaker (str): Voice speaker of the course
            speed (str): Speaking speed of the course
            pitch (str): Speaking pitch of the course
            course_style (str): Speaking style of the course
    '''

    def __init__(self, voice_speaker:str, speed:str, pitch:str, course_style:str) -> None:
        '''The constructor for TTSComponents Class

            Parameters:
                voice_speaker (str): Voice speaker of the course 
        '''
        self.voice_speaker = voice_speaker
        self.speed = speed
        self.pitch = pitch
        self.course_style = course_style
