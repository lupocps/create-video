'''Settings with the information required to execute the process.
'''

from datetime import datetime
from measure_timing import MeasureTiming


class Settings:
    '''This class contains all the information required to execute the process.

        Attributes:

    '''

    def __init__(self, yaml_dict, course_name, course_version,tts_components ,languages_to_translate, themes, trailer_mode):
        '''The constructor for Settings class.

            Parameters:
             
    
        '''
     #   self.root_folder = root_folder
        self.course_name = course_name
        self.course_version = course_version
        self.yaml_dict = yaml_dict
        self.trailer_mode = trailer_mode
        self.tts_components = tts_components
        self.languages_to_translate = languages_to_translate

        self.generate_captions = (
            'captions' in self.yaml_dict) and self.yaml_dict['captions'] is True
        self.generate_transcript = (
            'transcript' in self.yaml_dict) and self.yaml_dict['transcript'] is True
        self.generate_slides = (
            'slides' in self.yaml_dict) and self.yaml_dict['slides'] is True
        self.generate_logs = (
            'logs' in self.yaml_dict) and self.yaml_dict['logs'] is True
        self.clean_files = (
            'clean' in self.yaml_dict) and self.yaml_dict['clean'] is True
        self.stop_on_warning = (
            'stop' in self.yaml_dict) and self.yaml_dict['stop'] is True

        
        self.measure_timing = MeasureTiming()
    #    self.mail = mail
        self.themes = themes
        
        self.final = (
            'final' in yaml_dict) and yaml_dict['final'] is True

    #    self.output_path = f"{root_folder}/output"
        self.course_uuid = datetime.now().strftime('%m_%d_%Y_%H_%M_%S')

        self.themes = themes
        