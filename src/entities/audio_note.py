'''Entity for slide audio notes.
'''
from src.lupo.api_lupo import generate_audio
from src.entities.tts_components import TTSComponents
from src.lupo.compiler_lupo import rectify_voice_speaker

class AudioNote:
    '''Class with the information of the audio notes from the markdown file.

        Attributes:
            text (str): Text of the audio note
            time (str): Time in which the audio note will sound
            output_path (str): Path where the audio note is saved
    '''

    def __init__(
        self,
        text: str,
        time: str,
        tts_components: TTSComponents,
        style):
        '''Add the time (if any) to the text of the audio note to create the audio

            Parameters:
                text (srt): Text of the audio note
                time (str): Time in which the audio note will sound
                output_path (str): Path where the audio note will be saved
                tts (TextToSpeech): Object that can convert text-to-speech with azure
                tts_components (TTSComponents): Object with voice speaker, speed and pitch for the audio notes
        '''
        self.text = text.strip()
        self.time = time
        
        print("enter audionote class")
        if time is not None:

            times = time.split(',')

            self.seconds = float(times[-1])
            self.minutes = float(times[-2]) if len(times) >= 2 else 0
            self.hours = float(times[-3]) if len(times) >= 3 else 0

        output_audio_path = generate_audio(self.text, rectify_voice_speaker(tts_components.voice_speaker),
                       tts_components.speed, tts_components.pitch, style,)

       
        self.output_path = output_audio_path
        print("output_path audio note", self.output_path)
