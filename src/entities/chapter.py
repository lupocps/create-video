'''Module with the content of all sections of the chapter
'''
import os
from src.utils import log
from src.lupo.compiler_lupo import slugify
from src.lupo.compiler_lupo import is_path_creatable
from src.entities.settings import Settings
from src.entities.section import Section


class Chapter:
    '''This class contains all sections of the chapter.

        Attributes:


        Methods:


    '''

    def __init__(
            self,
            chapter_id: int,
            name: str,
            yml_sections: list,
            settings: Settings):
        '''The constructor of the Chapter class.

            Parameters:

        '''
        self.chapter_id = chapter_id
        self.name = name
        self.settings = settings
        self.sections = []



        section_id = 1
        for section in yml_sections:
            if "name" in section and "href" in section:
                if not is_path_creatable(str(section['name'])):
                    log(f"Special characters in folder {section['name']} are not allowed .", 'warning')

                section_name = slugify(section['name'])
                self.sections.append(
                     Section(
                         section_id=section_id,
                         name=section_name,
                         markdown_file=section["href"],
                         settings=settings
                     )
                 )

                section_id += 1
            else:
                log("The 'href' key is not found in one section", "error")
        print("sections", self.sections)
