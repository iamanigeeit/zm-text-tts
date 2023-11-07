import os
import re

O_TO_UO, O_TO_UO_SUB = re.compile(r'^([bpmf])o(?!u)'), r'\1uo'
U_TO_V, U_TO_V_SUB = re.compile(r'^([jqxy])u'), r'\1v'
I_TO_IH, I_TO_IH_SUB = re.compile(r'^([zcs]h?|r)i'), r'\1ɨ'
AN_TO_EN, AN_TO_EN_SUB = re.compile(r'([iv])an(?!g)'), r'\1en'

NULL_INITIAL = 'ʔ'

def regularize_pinyin(pinyin):
    pinyin = O_TO_UO.sub(O_TO_UO_SUB, pinyin)
    pinyin = U_TO_V.sub(U_TO_V_SUB, pinyin)
    pinyin = I_TO_IH.sub(I_TO_IH_SUB, pinyin)
    pinyin = AN_TO_EN.sub(AN_TO_EN_SUB, pinyin)
    if pinyin[0] in 'aoe':
        pinyin = NULL_INITIAL + pinyin
    return pinyin

INITIALS_TO_IPA = {
    'ʔ': 'ʔ',

    'b': 'p',
    'p': 'p h',
    'm': 'm',
    'f': 'f',

    'd': 't',
    't': 't h',
    'n': 'n',
    'l': 'l',

    'g': 'k',
    'k': 'k h',
    'h': 'x',

    'j': 'tɕ',
    'q': 'tɕ h',
    'x': 'ɕ',

    'zh': 'tʃ',
    'ch': 'tʃ h',
    'sh': 'ʂ',
    'r': 'ɹ',

    'z': 'ts',
    'c': 'ts h',
    's': 's',

    'y': 'j',
    'w': 'w'
}

RIMES_TO_IPA = {
    'ɨ': 'ɨ',
    'a': 'a',
    'ai': 'aɪ',
    'an': 'a n',
    'ang': 'a ŋ',
    'ao': 'aʊ',

    'e': 'ə',
    'ei': 'eɪ',
    'en': 'ə n',
    'eng': 'ə ŋ',

    'er': 'ɚ',

    'i': 'i',
    'ia': 'j a',
    'iang': 'j a ŋ',
    'iao': 'j aʊ',
    'ie': 'j ɛ',
    'ien': 'j ɛ n',
    'in': 'i n',
    'ing': 'i ŋ',
    'iong': 'j oʊ ŋ',
    'iu': 'j oʊ',

    'o': 'ɔ',
    'ou': 'oʊ',
    'ong': 'ʊ ŋ',

    'u': 'u',
    'ua': 'w a',
    'uai': 'w aɪ',
    'uan': 'w a n',
    'uang': 'w a ŋ',
    'ui': 'w eɪ',
    'un': 'w ə n',
    'uo': 'w ɔ',

    'v': 'y',
    've': 'y ɛ',
    'vn': 'y n',
    'ven': 'y ɛ n',
}

INITIALS = set(INITIALS_TO_IPA)
RIMES = set(RIMES_TO_IPA)
PINYIN_WITH_TONE_REGEX = re.compile(
    rf"({'|'.join(INITIALS)})({'|'.join(RIMES)})(r?)([1-5])"
)

def pinyin2ipa(pinyin):
    pinyin = regularize_pinyin(pinyin)
    m = PINYIN_WITH_TONE_REGEX.fullmatch(pinyin)
    if m is None:
        raise ValueError(f'Unrecognized character or pinyin: {pinyin}')
    else:
        initial, rime, r, tone = m.groups()
    init_ipa = INITIALS_TO_IPA[initial]
    rime_ipa = RIMES_TO_IPA[rime]
    if r:
        if rime == 'e':
            return f'{init_ipa} ɚ'
        else:
            return f'{init_ipa} {rime_ipa} ɹ'
    else:
        return f'{init_ipa} {rime_ipa}'


def convert_text_file(text_path):
    os.rename(text_path, text_path + '.old')
    with open(text_path, 'w') as new_f:
        with open(text_path + '.old') as f:
            for line in f:
                utt_id, pinyins = line.strip().split(maxsplit=1)
                pinyins = pinyins.split()
                ipa = ' '.join(pinyin2ipa(pinyin) for pinyin in pinyins)
                new_f.write(f'{utt_id} {ipa}\n')

if __name__ == '__main__':
    convert_text_file('../data/test_phn/text')