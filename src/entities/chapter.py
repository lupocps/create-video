'''Module with the content of all sections of the chapter
'''
import os
#from coursecreator.utils import log
#from coursecreator.compiler import is_path_creatable
#from coursecreator.compiler import slugify
from settings import Settings
from section import Section
from src.utils import log
from src.lupo.compiler_lupo import is_path_creatable
from src.lupo.compiler_lupo import slugify

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


    # def generate_slides(self) -> list:
    #     '''Generate a PowerPoint presentation of the entire course.

    #     Return:
    #         str: The generated file path of the PowerPoint presentation
    #     '''

    #     output_directory_files = f"{self.output_directory}/{self.name}"
    #     md_file = f"{output_directory_files}-slides.md"

    #     markdown_content = ""

    #     for section in self.sections:
    #         if markdown_content == "":
    #             with open(section.markdown_file, 'r', encoding='utf-8') as f:
    #                 markdown_content += "---\n" + f.read().split("---")[1]

    #         for page in section.pages:

    #             slide = f"{page.markdown_text} \n\n<!--\n{page.source_audio_notes}\n-->\n"

    #             markdown_content += "\n---\n\n" + slide

    #     with open(md_file, 'w+', encoding='utf-8') as f:
    #         f.write(markdown_content)

    #     #themes = ' '.join([theme for theme in self.settings.themes])
    #     themes = self.settings.themes

    #     os.system(
    #         f"npx @marp-team/marp-cli@latest --theme-set {themes} --html --allow-local-files {md_file} --pdf-notes -o {output_directory_files}-pdf.pdf ")
    #     # os.system(f"marp --allow-local-files  {md_file} --pdf-notes -o {output_directory_files}-pdf.pdf") # install marp
    #     os.system(
    #         f"npx @marp-team/marp-cli@latest --theme-set {themes} --html --allow-local-files {md_file} -o {output_directory_files}-slides.pptx ")
    #     # os.system(f"marp --allow-local-files  {md_file} -o {output_directory_files}-slides.pptx") # install marp
    #     os.system(
    #         f"npx @marp-team/marp-cli@latest --theme-set {themes} --html --allow-local-files {md_file} -o {output_directory_files}-html.html ")

    #     os.remove(md_file)
    #     return (f"{output_directory_files}-slides.pptx", f"{output_directory_files}-pdf.pdf", f"{output_directory_files}-html.html")


    # def generate_transcript(self) -> str: ##### does not work now
    #     '''Generate the transcripts for the entire course.

    #     Return:
    #         str: The generated file path of the transcript
    #     '''
    #     transcript = f"{self.output_directory}/{self.name}-transcript.txt"
    #     with open(transcript, 'w+', encoding='utf-8') as f:
    #         for section in self.sections:
    #             for page in section.pages:
    #                 f.write(f"{page.source_audio_notes} ")
    #     return transcript
