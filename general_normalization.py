import re
from decimal import Decimal
import copy
from itertools import groupby
from string import punctuation


class General_normalization:
    def __init__(self):

        self.persian_erab = {'ٰ': '', 'ً': '', 'ٌ': '', 'ٍ': '', 'َ': '', 'ُ': '', 'ِ': '', 'ّ': '', 'ْ': '', 'ٓ': '',
                                'ٔ': '', 'ٖ': '', 'ؕ': '', 'ٕ': '', 'ٙ': '', 'ٴ': '', '̒': '', '́': ''}
        self.keshide = {'ـ': ''}

        self.persian_A = {'ﺁ': 'ا', 'ﺂ': 'ا',"آ":'ا'}

        self.persian_a = {  'ﺍ': 'ا', 'ﺎ': 'ا', 'ٲ': 'ا', 'ٵ': 'ا', 'ﭐ': 'ا', 'ﭑ': 'ا', 'ﺃ': 'ا', 'ﺄ': 'ا', 'ٳ': 'ا',
                            'ﺇ': 'ا', 'ﺈ': 'ا', 'إ': 'ا', 'أ': 'ا', 'ꙇ': 'ا', 'ٱ': 'ا'}

        self.persian_b = {  'ٮ': 'ب', 'ٻ': 'ب', 'ڀ': 'ب', 'ݐ': 'ب', 'ݒ': 'ب', 'ݔ': 'ب', 'ݕ': 'ب', 'ݖ': 'ب', 'ﭒ': 'ب',
                            'ﭓ': 'ب', 'ﭔ': 'ب', 'ﭕ': 'ب', 'ﺏ': 'ب', 'ﺐ': 'ب', 'ﺑ': 'ب', 'ﺒ': 'ب'}

        self.persian_p = {'ﭖ': 'پ', 'ﭗ': 'پ', 'ﭘ': 'پ', 'ﭙ': 'پ', 'ﭚ': 'پ', 'ﭛ': 'پ', 'ﭜ': 'پ', 'ﭝ': 'پ'}

        self.persian_t1 = { 'ٹ': 'ت', 'ٺ': 'ت', 'ټ': 'ت', 'ٿ': 'ت', 'ݓ': 'ت', 'ﭞ': 'ت', 'ﭟ': 'ت', 'ﭠ': 'ت', 'ﭡ': 'ت',
                            'ﭦ': 'ت', 'ﭧ': 'ت', 'ﭨ': 'ت', 'ﭩ': 'ت', 'ﺕ': 'ت', 'ﺖ': 'ت', 'ﺗ': 'ت', 'ﺘ': 'ت'}

        self.persian_c1 = { 'ٽ': 'ث', 'ݑ': 'ث', 'ﺙ': 'ث', 'ﺚ': 'ث', 'ﺛ': 'ث', 'ﺜ': 'ث', 'ﭢ': 'ث', 'ﭣ': 'ث', 'ﭤ': 'ث',
                            'ﭥ': 'ث'}

        self.persian_j = {  'ڃ': 'ج', 'ڄ': 'ج', 'ﭲ': 'ج', 'ﭳ': 'ج', 'ﭴ': 'ج', 'ﭵ': 'ج', 'ﭶ': 'ج', 'ﭷ': 'ج', 'ﭸ': 'ج',
                            'ﭹ': 'ج', 'ﺝ': 'ج', 'ﺞ': 'ج', 'ﺟ': 'ج', 'ﺠ': 'ج'}

        self.persian_ch = { 'ڇ': 'چ', 'ڿ': 'چ', 'ﭺ': 'چ', 'ﭻ': 'چ', 'ݘ': 'چ', 'ﭼ': 'چ', 'ﭽ': 'چ', 'ﭾ': 'چ', 'ﭿ': 'چ',
                            'ﮀ': 'چ', 'ﮁ': 'چ', 'ݯ': 'چ'}

        self.persian_h1 = {'ځ': 'ح', 'ڂ': 'ح', 'څ': 'ح', 'ݗ': 'ح', 'ݮ': 'ح', 'ﺡ': 'ح', 'ﺢ': 'ح', 'ﺣ': 'ح', 'ﺤ': 'ح'}

        self.persian_kh = {'ﺥ': 'خ', 'ﺦ': 'خ', 'ﺧ': 'خ', 'ﺨ': 'خ'}

        self.persian_d = {'ڈ': 'د', 'ډ': 'د', 'ڊ': 'د', 'ڋ': 'د', 'ڍ': 'د', 'ۮ': 'د', 'ݙ': 'د', 'ݚ': 'د', 'ﮂ': 'د',
                            'ﮃ': 'د', 'ﮄ': 'د', 'ﮈ': 'د', 'ﮉ': 'د', 'ﺩ': 'د', 'ﺪ': 'د'}

        self.persian_zal = {'ڌ': 'ذ', 'ﱛ': 'ذ', 'ﺫ': 'ذ', 'ﺬ': 'ذ', 'ڎ': 'ذ', 'ڏ': 'ذ', 'ڐ': 'ذ', 'ﮅ': 'ذ', 'ﮆ': 'ذ',
                            'ﮇ': 'ذ'}

        self.persian_r = {'ڑ': 'ر', 'ڒ': 'ر', 'ړ': 'ر', 'ڔ': 'ر', 'ڕ': 'ر', 'ږ': 'ر', 'ۯ': 'ر', 'ݛ': 'ر', 'ﮌ': 'ر',
                            'ﮍ': 'ر', 'ﱜ': 'ر', 'ﺭ': 'ر', 'ﺮ': 'ر'}

        self.persian_z = {'ڗ': 'ز', 'ݫ': 'ز', 'ݬ': 'ز', 'ﺯ': 'ز', 'ﺰ': 'ز'}

        self.persian_zh = {'ڙ': 'ژ', 'ﮊ': 'ژ', 'ﮋ': 'ژ'}

        self.persian_s = {'ښ': 'س', 'ڛ': 'س', 'ﺱ': 'س', 'ﺲ': 'س', 'ﺳ': 'س', 'ﺴ': 'س'}

        self.persian_sh = {'ڜ': 'ش', 'ۺ': 'ش', 'ﺵ': 'ش', 'ﺶ': 'ش', 'ﺷ': 'ش', 'ﺸ': 'ش', 'ݜ': 'ش', 'ݭ': 'ش'}

        self.persian_sad = {'ڝ': 'ص', 'ڞ': 'ص', 'ﺹ': 'ص', 'ﺺ': 'ص', 'ﺻ': 'ص', 'ﺼ': 'ص'}

        self.persian_zad = {'ۻ': 'ض', 'ﺽ': 'ض', 'ﺾ': 'ض', 'ﺿ': 'ض', 'ﻀ': 'ض'}

        self.persian_ta = {'ﻁ': 'ط', 'ﻂ': 'ط', 'ﻃ': 'ط', 'ﻄ': 'ط'}

        self.persian_za = {'ﻅ': 'ظ', 'ﻆ': 'ظ', 'ﻇ': 'ظ', 'ﻈ': 'ظ', 'ڟ': 'ظ'}

        self.persian_eyn = {'ڠ': 'ع', 'ݝ': 'ع', 'ݞ': 'ع', 'ݟ': 'ع', 'ﻉ': 'ع', 'ﻊ': 'ع', 'ﻋ': 'ع', 'ﻌ': 'ع'}

        self.persian_ghein = {'ۼ': 'غ', 'ﻍ': 'غ', 'ﻎ': 'غ', 'ﻏ': 'غ', 'ﻐ': 'غ'}

        self.persian_f = {  'ڡ': 'ف', 'ڢ': 'ف', 'ڣ': 'ف', 'ڤ': 'ف', 'ڥ': 'ف', 'ڦ': 'ف', 'ݠ': 'ف', 'ݡ': 'ف', 'ﭪ': 'ف',
                            'ﭫ': 'ف', 'ﭬ': 'ف', 'ﭭ': 'ف', 'ﭮ': 'ف', 'ﭯ': 'ف', 'ﭰ': 'ف', 'ﭱ': 'ف', 'ﻑ': 'ف', 'ﻒ': 'ف',
                            'ﻓ': 'ف', 'ﻔ': 'ف', 'ᓅ': 'ف'}

        self.persian_gh = {'ٯ': 'ق', 'ڧ': 'ق', 'ڨ': 'ق', 'ﻕ': 'ق', 'ﻖ': 'ق', 'ﻗ': 'ق', 'ﻘ': 'ق'}

        self.persian_k = {  'ك': 'ک', 'ػ': 'ک', 'ؼ': 'ک', 'ڪ': 'ک', 'ګ': 'ک', 'ڬ': 'ک', 'ڭ': 'ک', 'ڮ': 'ک', 'ݢ': 'ک',
                            'ݣ': 'ک', 'ݤ': 'ک', 'ﮎ': 'ک', 'ﮏ': 'ک', 'ﮐ': 'ک', 'ﮑ': 'ک', 'ﯓ': 'ک', 'ﯔ': 'ک', 'ﯕ': 'ک',
                            'ﯖ': 'ک', 'ﻙ': 'ک', 'ﻚ': 'ک', 'ﻛ': 'ک', 'ﻜ': 'ک'}

        self.persian_g = {  'ڰ': 'گ', 'ڱ': 'گ', 'ڲ': 'گ', 'ڳ': 'گ', 'ڴ': 'گ', 'ﮒ': 'گ', 'ﮓ': 'گ', 'ﮔ': 'گ', 'ﮕ': 'گ',
                            'ﮖ': 'گ', 'ﮗ': 'گ', 'ﮘ': 'گ', 'ﮙ': 'گ', 'ﮚ': 'گ', 'ﮛ': 'گ', 'ﮜ': 'گ', 'ﮝ': 'گ'}

        self.persian_l = {'ڵ': 'ل', 'ڶ': 'ل', 'ڷ': 'ل', 'ڸ': 'ل', 'ݪ': 'ل', 'ﻝ': 'ل', 'ﻞ': 'ل', 'ﻟ': 'ل', 'ﻠ': 'ل'}

        self.persian_m = {'۾': 'م', 'ݥ': 'م', 'ݦ': 'م', 'ﻡ': 'م', 'ﻢ': 'م', 'ﻣ': 'م', 'ﻤ': 'م'}

        self.persian_n = {  'ڹ': 'ن', 'ں': 'ن', 'ڻ': 'ن', 'ڼ': 'ن', 'ڽ': 'ن', 'ݧ': 'ن', 'ݨ': 'ن', 'ݩ': 'ن', 'ﮞ': 'ن',
                            'ﮟ': 'ن', 'ﮠ': 'ن', 'ﮡ': 'ن', 'ﮢ': 'ن', 'ﮣ': 'ن', 'ﻥ': 'ن', 'ﻦ': 'ن', 'ﻧ': 'ن', 'ﻨ': 'ن'}

        self.persian_v = {  'ٶ': 'و', 'ٷ': 'و', 'ﯗ': 'و', 'ﯘ': 'و', 'ﯙ': 'و', 'ﯚ': 'و', 'ﯛ': 'و', 'ﯜ': 'و', 'ﯝ': 'و',
                            'ﯞ': 'و', 'ﯟ': 'و', 'ﺅ': 'و', 'ﺆ': 'و', 'ۄ': 'و', 'ۅ': 'و', 'ۆ': 'و', 'ۇ': 'و', 'ۈ': 'و',
                            'ۉ': 'و', 'ۊ': 'و', 'ۋ': 'و', 'ۏ': 'و', 'ﯠ': 'و', 'ﯡ': 'و', 'ﯢ': 'و', 'ﯣ': 'و', 'ﻭ': 'و',
                            'ﻮ': 'و', 'ؤ': 'و', 'פ': 'و'}

        self.persian_h2 = { 'ھ': 'ه', 'ۿ': 'ه', 'ۀ': 'ه', 'ہ': 'ه', 'ۂ': 'ه', 'ۃ': 'ه', 'ە': 'ه', 'ﮤ': 'ه', 'ﮥ': 'ه',
                            'ﮦ': 'ه', 'ﮧ': 'ه', 'ﮨ': 'ه', 'ﮩ': 'ه', 'ﮪ': 'ه', 'ﮫ': 'ه', 'ﮬ': 'ه', 'ﮭ': 'ه', 'ﺓ': 'ه',
                            'ﺔ': 'ه', 'ﻩ': 'ه', 'ﻪ': 'ه', 'ﻫ': 'ه', 'ﻬ': 'ه'}

        self.persian_y = {  'ؠ': 'ی', 'ؽ': 'ی', 'ؾ': 'ی', 'ؿ': 'ی', 'ى': 'ی', 'ي': 'ی', 'ٸ': 'ی', 'ۍ': 'ی', 'ێ': 'ی',
                            'ې': 'ی', 'ۑ': 'ی', 'ے': 'ی', 'ۓ': 'ی', 'ﮮ': 'ی', 'ﮯ': 'ی', 'ﮰ': 'ی', 'ی': 'ی', 'ﯤ': 'ی',
                            'ﯥ': 'ی', 'ﯦ': 'ی', 'ﯧ': 'ی', 'ﯼ': 'ی', 'ﯽ': 'ی', 'ﯾ': 'ی', 'ﯿ': 'ی', 'ﻯ': 'ی', 'ﻰ': 'ی',
                            'ﻱ': 'ی', 'ﻲ': 'ی', 'ﻳ': 'ی', 'ﻴ': 'ی', 'ﯨ': 'ی', 'ﯩ': 'ی', 'ﯪ': 'ی', 'ی': 'ی', 'ﯬ': 'ی',
                            'ﯭ': 'ی', 'ﯮ': 'ی', 'ﯯ': 'ی', 'ﯰ': 'ی', 'ﯱ': 'ی', 'ﯲ': 'ی', 'ﯳ': 'ی', 'ی': 'ی', 'ﯵ': 'ی',
                            'ﯶ': 'ی', 'ﯷ': 'ی', 'ﯸ': 'ی', 'ﯹ': 'ی', 'ﯺ': 'ی', 'ﯻ': 'ی', 'ﱝ': 'ی', 'ی': 'ی', 'ﺊ': 'ی',
                            'ﺋ': 'ی', 'ﺌ': 'ی', 'ئ': 'ی'}
        
        self.persian_alphabet_replaces = [
             self.persian_erab,
            self.keshide,
            self.persian_A,
            self.persian_a,
            self.persian_b,
            self.persian_p,
            self.persian_t1,
            self.persian_c1,
            self.persian_j,
            self.persian_ch,
            self.persian_h1,
            self.persian_kh,
            self.persian_d,
            self.persian_zal,
            self.persian_r,
            self.persian_z,
            self.persian_zh,
            self.persian_s,
            self.persian_sh,
            self.persian_sad,
            self.persian_zad,
            self.persian_ta,
            self.persian_za,
            self.persian_eyn,
            self.persian_ghein,
            self.persian_f,
            self.persian_gh,
            self.persian_k,
            self.persian_g,
            self.persian_l,
            self.persian_m,
            self.persian_n,
            self.persian_v,
            self.persian_h2,
            self.persian_y
        ]

        self.arabic_la = {'ﻵ': 'لا', 'ﻶ': 'لا', 'ﻻ': 'لا', 'ﻼ': 'لا', 'ﻷ': 'لا', 'ﻸ': 'لا', 'ﻹ': 'لا', 'ﻺ': 'لا'}
        self.arabic_sali = {'ﷰ': 'صلی', 'ﷹ': 'صلی'}
        self.arabic_gholi = {'ﷱ': 'قلی'}
        self.arabic_allah = {'ﷲ': 'الله'}
        self.arabic_akbar = {'ﷳ': 'اکبر'}
        self.arabic_mohammad = {'ﷴ': 'محمد'}
        self.arabic_rasol = {'ﷶ': 'رسول'}
        self.arabic_alayh = {'ﷷ': 'علیه'}
        self.arabic_vasalam = {'ﷸ': 'وسلم'}
        self.arabic_rial = {'﷼': 'ریال'}
        self.arabic_senat = {'\u0601': 'سنه'}
        self.arabic_salam = {'ﷵ': 'صلعم'}
        self.arabic_senat = {'ﷺ': 'صلی الله علیه و سلم'}
        self.arabic_jal = {'ﷻ': 'جل جلاله'}
        
        

        self.arabic_replaces = [
            self.arabic_la,
            self.arabic_sali,
            self.arabic_gholi,
            self.arabic_allah,
            self.arabic_akbar,
            self.arabic_mohammad,
            self.arabic_rasol,
            self.arabic_alayh,
            self.arabic_rial,
            self.arabic_senat,
            self.arabic_salam,
            self.arabic_senat,
            self.arabic_jal,
        ]

        self.number_replaces_zero = {'0': '۰', '٠': '۰', '𝟢': '۰', '𝟬': '۰', '٠': '۰'}

        self.number_replaces_one = {'1': '۱', '١': '۱', '𝟣': '۱', '𝟭': '۱', '⑴': '۱', '⒈': '۱', '⓵': '۱', '①': '۱',
                                    '❶': '۱', '𝟙': '۱', '𝟷': '۱', 'ı': '۱'}

        self.number_replaces_two = {'2': '۲', '٢': '۲', '𝟤': '۲', '𝟮': '۲', '⑵': '۲', '⒉': '۲', '⓶': '۲', '②': '۲',
                                    '❷': '۲', '²': '۲', '𝟐': '۲', '𝟸': '۲', '𝟚': '۲', 'ᒿ': '۲', 'շ': '۲'}

        self.number_replaces_three = {'3': '۳', '٣': '۳', '𝟥': '۳', '𝟯': '۳', '⑶': '۳', '⒊': '۳', '⓷': '۳', '③': '۳',
                                      '❸': '۳', '³': '۳', 'ვ': '۳'}

        self.number_replaces_four = {'4': '۴', '٤': '۴', '𝟦': '۴', '𝟰': '۴', '⑷': '۴', '⒋': '۴', '⓸': '۴', '④': '۴',
                                     '❹': '۴', '⁴': '۴'}

        self.number_replaces_five = {'5': '۵', '٥': '۵', '𝟧': '۵', '𝟱': '۵', '⑸': '۵', '⒌': '۵', '⓹': '۵', '⑤': '۵',
                                     '❺': '۵', '⁵': '۵'}

        self.number_replaces_six = {'6': '۶', '٦': '۶', '𝟨': '۶', '𝟲': '۶', '⑹': '۶', '⒍': '۶', '⓺': '۶', '⑥': '۶',
                                    '❻': '۶', '⁶': '۶'}

        self.number_replaces_seven = {'7': '۷', '٧': '۷', '𝟩': '۷', '𝟳': '۷', '⑺': '۷', '⒎': '۷', '⓻': '۷', '⑦': '۷',
                                      '❼': '۷', '⁷': '۷'}

        self.number_replaces_eight = {'8': '۸', '٨': '۸', '𝟪': '۸', '𝟴': '۸', '⑻': '۸', '⒏': '۸', '⓼': '۸', '⑧': '۸',
                                      '❽': '۸', '⁸': '۸', '۸': '۸', }

        self.number_replaces_nine = {'9': '۹', '٩': '۹', '𝟫': '۹', '𝟵': '۹', '⑼': '۹', '⒐': '۹', '⓽': '۹', '⑨': '۹',
                                     '❾': '۹', '⁹': '۹'}
        
        
        self.number_replaces = [
            self.number_replaces_zero,
            self.number_replaces_one,
            self.number_replaces_two,
            self.number_replaces_three,
            self.number_replaces_four,
            self.number_replaces_five,
            self.number_replaces_six,
            self.number_replaces_seven,
            self.number_replaces_eight,
            self.number_replaces_nine
        ]

        self.punctuation_three_dot = {'…': ' '}

        self.punctuation_pipe = {'▕': ' ', '❘': ' ', '❙': ' ', '❚': ' ', '▏': ' ', '│': ' '}

        self.punctuation_dash = {'ㅡ': '-', '一': '-', '—': '-', '–': '-', 'ー': '-', '̶': '-', 'ـ': '-'}

        self.punctuation_underline = {'▁': '_', '_': '_', '̲': '_'}

        self.punctuation_question = {'❔': ' ', '?': ' ', '�': ' ', '？': ' ', 'ʕ': ' ', 'ʔ': ' ', '🏻': ' ', '\x08': ' ',
                                     '\x97': ' ', '\x9d': ' '}

        self.punctuation_Exclamation = {'❕': ' ', '！': ' '}

        self.punctuation_Exclamation_Question = {'⁉': ' '}

        self.punctuation_double_Exclamation = {'‼': ' '}

        self.punctuation_percent = {'℅': ' درصد ', '٪': ' درصد '}

        self.punctuation_devide = {'÷': ' '}

        self.punctuation_multiply = {'×': ' '}

        self.punctuation_double_dot = {'：': ' '}

        self.punctuation_semicolun = {'؛': ' ', '；': ' '}

        self.punctuation_greater = {'›': ' '}

        self.punctuation_smaller = {'‹': ' ', '＜': ' '}

        self.punctuation_double_smaller = {'《': ' '}

        self.punctuation_double_greater = {'》': ' '}

        self.punctuation_dot = {'•': '.'}

        self.punctuation_replaces = [
            self.punctuation_three_dot,
            self.punctuation_pipe,
            self.punctuation_dash,
            self.punctuation_underline,
            self.punctuation_question,
            self.punctuation_Exclamation,
            self.punctuation_Exclamation_Question,
            self.punctuation_double_Exclamation,
            self.punctuation_percent,
            self.punctuation_devide,
            self.punctuation_multiply,
            self.punctuation_double_dot,
            self.punctuation_semicolun,
            self.punctuation_greater,
            self.punctuation_smaller,
            self.punctuation_double_smaller,
            self.punctuation_double_greater,
            self.punctuation_dot,
        ]

        self.characters_to_remain = ["۰", "۱", "۲", "۳", "۴", "۵", "۶", "۷", "۸", "۹", "ا","ب", "پ",
                                     "ت", "ث", "ج", "چ", "ح", "خ", "د", "ذ", "ر", "ز", "ژ", "س", "ش", "ص", "ض", "ط",
                                     "ظ", "ع", "غ", "ف", "ک", "گ", "ق", "ل", "م", "ن", "و", "ه", "ی",
                                     "a", "A", "b", "B", "c", "C", "d", "D", "e", "E", "f", "F", "g", "G", "h",
                                     "H", "i", "I", "j", "J", "k", "K", "l", "L", "m", "M", "n", "N", "o", "O", "p",
                                     "P", "q", "Q", "r", "R", "s", "S", "t", "T", "u", "U", "v", "V", "w", "W", "x",
                                     "X", "y", "Y", "z", "Z", "\u200c", "\u200e", r"\s"," ", "","@"]
        
        

    def alphabet_correction(self, sentence):
        for persian_alphabet_replace in self.persian_alphabet_replaces:
            sentence = sentence.translate(str.maketrans(persian_alphabet_replace))
        return sentence

    def arabic_correction(self, sentence):
        for arabic_replace in self.arabic_replaces:
            sentence = sentence.translate(str.maketrans(arabic_replace))
        return sentence

    def number_correction(self, sentence):
        for number_replace in self.number_replaces:
            sentence = sentence.translate(str.maketrans(number_replace))
        return sentence

    def punctuation_correction(self, sentence):
        for punctuation_replace in self.punctuation_replaces:
            sentence = sentence.translate(str.maketrans(punctuation_replace))
        return sentence


    def space_between_punctuations_and_text(self, sentence):
        sentence = re.sub('([.,!?()])', r'\1', sentence)
        sentence = re.sub(r'\s{2,}', ' ', sentence)
        return sentence


    def remove_not_desired_chars(self, sentence):
        for character in sentence:
            if character not in self.characters_to_remain:
                sentence = sentence.replace(character," ")
        return sentence

    def space_correction(self, sentence):
        ## This Function is a mixture of HAZM and ParsiVar Features
        punc_after, punc_before = r'\.:!،؛؟»\]\)\}', r'«\[\(\{'
        sentence = re.sub(r'^(بی|می|نمی)( )', r'\1‌', sentence)  # verb_prefix
        sentence = re.sub(r'( )(می|نمی)( )', r'\1\2‌', sentence)  # verb_prefix
        sentence = re.sub(r'([^ ]ه) ی ', r'\1‌ی ', sentence)  # nouns ends with ه when having ی
        sentence = re.sub(r'(\ )(هایی|ها|های|ایی|هایم|هایت|هایش|ی|هایمان|هایتان|هایشان|ات|ین' \
                          r'|انی|بان|ام|ای|یم|ید|اید|اند|بودم|بودی|بود|بودیم|بودید|بودند|ست|تر|تری|ترین|گری|گر)( )',
                          r'‌\2\3', sentence)
        complex_word_suffix_pattern = r'( )(طلبان|طلب|گرایی|گرایان|شناس|شناسی|گذاری|گذار|گذاران|شناسان|گیری|پذیری|بندی|آوری|سازی|' \
                                      r'بندی|کننده|کنندگان|گیری|پرداز|پردازی|پردازان|آمیز|سنجی|ریزی|داری|دهنده|آمیز|پذیری' \
                                      r'|پذیر|پذیران|گر|ریز|ریزی|رسانی|یاب|یابی|گانه|گانه‌ای|انگاری|گا|بند|رسانی|دهندگان|دار)( )'
        sentence = re.sub(complex_word_suffix_pattern, r'‌\2\3', sentence)
        sentence = sentence.replace(r'‌ ',' ')
        sentence = sentence.replace(r' ‌',' ')
        return sentence
    
    def normalize(self,sentence):
        x = sentence
        x = self.alphabet_correction(x)
        x = self.arabic_correction(x)
        x = self.punctuation_correction(x)
        x = self.number_correction(x)
        x = self.space_correction(x)
        x = self.space_between_punctuations_and_text(x)
        x = self.remove_not_desired_chars(x)
        return x
        



        