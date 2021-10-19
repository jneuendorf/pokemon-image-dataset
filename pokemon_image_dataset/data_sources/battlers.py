import shutil

from py7zr import unpack_7zarchive
from wand.image import Image

from pokemon_image_dataset.data_sources import SpriteSetDataSource, SpriteSetConfig, PathDict
from pokemon_image_dataset.form import DISMISS_FORM, Form, get_form
from pokemon_image_dataset.utils import NAME_DELIMITER, name, with_stem


class BattlersDataSource(SpriteSetDataSource):
    url = 'https://www.mediafire.com/folder/mi31mvoxx98ij/3D_Battlers'
    checksum = 'a282265f827aaf309f08c1be7ea98726de14bca942823ea85e6d7c77338d1205'
    sprite_sets = {
        'Front': SpriteSetConfig(
            dest='3d-battlers-animated',
            glob='*.png',
            extra={
                'Female/521.png': '521-female.png',
                'Female/592.png': '592-female.png',
                'Female/593.png': '593-female.png',
                'Female/668.png': '668-female.png',
                'Female/678.png': '678-female.png',
            },
            post_process='extract_frames',
        ),
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            shutil.register_unpack_format('7zip', ['.7z'], unpack_7zarchive)
        except shutil.RegistryError as error:
            if '.7z is already registered for "7zip"' in str(error):
                pass
            else:
                raise

    def get(self, force):
        # TODO: Implement automatic download
        if not (self.tmp_dir / '3D Battlers [All].7z').exists():
            print('Please manually download the file from')
            print('  https://www.mediafire.com/folder/mi31mvoxx98ij/3D_Battlers')
            print('and save it as tmp/3D Battlers [All].7z')
        return self.tmp_dir / '3D Battlers [All].7z'

    def parse_ndex(self, filename: str) -> int:
        return super().parse_ndex(filename.replace('_', NAME_DELIMITER))

    def extract_frames(self, src: str, conf: SpriteSetConfig):
        # for filename in sorted(self.get_dest(src, conf).iterdir()):
        for filename in sorted(self.renamed_filenames):
            print('extract_frames', filename)
            img = Image(filename=filename)
            assert (
                img.width / img.height).is_integer(), 'invalid/non-integer image ratio'
            frame_width, frame_height = img.height, img.height

            i = 0
            first_frame = None
            # frames = []

            for x in range(0, img.width, frame_width):
                i = x // frame_width
                frame = img[x:x+frame_width, 0:frame_height]
                if x == 0:
                    first_frame = frame
                else:
                    if frame == first_frame:
                        print('found cycle at frame =', i)
                        break
                # frames.append(frame)
                frame.format = 'png'
                frame.save(
                    filename=with_stem(filename, name(filename.stem, str(i))),
                )
            # create_gif_from_frames(frames, filename)
            filename.unlink()

    def assign_forms(self):
        return PathDict.with_prefix(
            '3d-battlers-animated/',
            {
                # Set normal form explicitly because zero padded filenames.
                **{
                    str(i).zfill(3): get_form(i, Form.NORMAL)
                    for i in range(1, 807 + 1)
                    if get_form(i, Form.NORMAL, default=None)
                },
                **{
                    '003_1': get_form(3, Form.MEGA),
                    '006_1': get_form(6, Form.MEGA_X),
                    '006_2': get_form(6, Form.MEGA_Y),
                    '009_1': get_form(9, Form.MEGA),
                    '015_1': get_form(15, Form.MEGA),
                    '018_1': get_form(18, Form.MEGA),
                    '019_1': get_form(19, Form.ALOLA),
                    '020_1': get_form(20, Form.ALOLA),
                    '026_1': get_form(26, Form.ALOLA),
                    '027_1': get_form(27, Form.ALOLA),
                    '028_1': get_form(28, Form.ALOLA),
                    '037_1': get_form(37, Form.ALOLA),
                    '038_1': get_form(38, Form.ALOLA),
                    '050_1': get_form(50, Form.ALOLA),
                    '051_1': get_form(51, Form.ALOLA),
                    '052_1': get_form(52, Form.ALOLA),
                    # only image without leading zeros
                    '53_1': get_form(53, Form.ALOLA),
                    '065_1': get_form(65, Form.MEGA),
                    '074_1': get_form(74, Form.ALOLA),
                    '075_1': get_form(75, Form.ALOLA),
                    '076_1': get_form(76, Form.ALOLA),
                    '080_1': get_form(80, Form.MEGA),
                    '088_1': get_form(88, Form.ALOLA),
                    '089_1': get_form(89, Form.ALOLA),
                    '094_1': get_form(94, Form.MEGA),
                    '103_1': get_form(103, Form.ALOLA),
                    '105_1': get_form(105, Form.ALOLA),
                    '115_1': get_form(115, Form.MEGA),
                    '127_1': get_form(127, Form.MEGA),
                    '130_1': get_form(130, Form.MEGA),
                    '142_1': get_form(142, Form.MEGA),
                    '150_1': get_form(150, Form.MEGA_X),
                    '150_2': get_form(150, Form.MEGA_Y),
                    '181_1': get_form(181, Form.MEGA),
                    '201': get_form(201, 'a'),
                    '201_1': get_form(201, 'b'),
                    '201_2': get_form(201, 'd'),
                    '201_3': get_form(201, 'c'),
                    '201_4': get_form(201, 'e'),
                    '201_5': get_form(201, 'f'),
                    '201_6': get_form(201, 'g'),
                    '201_7': get_form(201, 'h'),
                    '201_8': get_form(201, 'i'),
                    '201_9': get_form(201, 'j'),
                    '201_10': get_form(201, 'k'),
                    '201_11': get_form(201, 'l'),
                    '201_12': get_form(201, 'm'),
                    '201_13': get_form(201, 'n'),
                    '201_14': get_form(201, 'o'),
                    '201_15': get_form(201, 'p'),
                    '201_16': get_form(201, 'q'),
                    '201_17': get_form(201, 'r'),
                    '201_18': get_form(201, 's'),
                    '201_19': get_form(201, 't'),
                    '201_20': get_form(201, 'u'),
                    '201_21': get_form(201, 'v'),
                    '201_22': get_form(201, 'w'),
                    '201_23': get_form(201, 'x'),
                    '201_24': get_form(201, 'y'),
                    '201_25': get_form(201, 'z'),
                    '201_26': get_form(201, 'question'),
                    '201_27': get_form(201, 'exclamation'),
                    '208_1': get_form(208, Form.MEGA),
                    '212_1': get_form(212, Form.MEGA),
                    '214_1': get_form(214, Form.MEGA),
                    '229_1': get_form(229, Form.MEGA),
                    '248_1': get_form(248, Form.MEGA),
                    '254_1': get_form(254, Form.MEGA),
                    '257_1': get_form(257, Form.MEGA),
                    '260_1': get_form(260, Form.MEGA),
                    '282_1': get_form(282, Form.MEGA),
                    '302_1': get_form(302, Form.MEGA),
                    '303_1': get_form(303, Form.MEGA),
                    '306_1': get_form(306, Form.MEGA),
                    '308_1': get_form(308, Form.MEGA),
                    '310_1': get_form(310, Form.MEGA),
                    '319_1': get_form(319, Form.MEGA),
                    '323_1': get_form(323, Form.MEGA),
                    '334_1': get_form(334, Form.MEGA),
                    '351_1': get_form(351, 'sunny'),
                    '351_2': get_form(351, 'rainy'),
                    '351_3': get_form(351, 'snowy'),
                    '354_1': get_form(354, Form.MEGA),
                    '359_1': get_form(359, Form.MEGA),
                    '362_1': get_form(362, Form.MEGA),
                    '373_1': get_form(373, Form.MEGA),
                    '376_1': get_form(376, Form.MEGA),
                    '380_1': get_form(380, Form.MEGA),
                    '381_1': get_form(381, Form.MEGA),
                    '382_1': get_form(382, 'primal'),
                    '383_1': get_form(383, 'primal'),
                    '384_1': get_form(384, Form.MEGA),
                    '386': get_form(386, Form.NORMAL),
                    '386_1': get_form(386, 'attack'),
                    '386_2': get_form(386, 'defense'),
                    '386_3': get_form(386, 'speed'),
                    '412': get_form(412, 'plant'),
                    '412_1': get_form(412, 'sandy'),
                    '412_2': get_form(412, 'trash'),
                    '413': get_form(413, 'plant'),
                    '413_1': get_form(413, 'sandy'),
                    '413_2': get_form(413, 'trash'),
                    '421': get_form(421, 'overcast'),
                    '421_1': get_form(421, 'sunshine'),
                    '422': get_form(422, 'west'),
                    '422_1': get_form(422, 'east'),
                    '423': get_form(423, 'west'),
                    '423_1': get_form(423, 'east'),
                    '428_1': get_form(428, Form.MEGA),
                    '445_1': get_form(445, Form.MEGA),
                    '448_1': get_form(448, Form.MEGA),
                    '460_1': get_form(460, Form.MEGA),
                    '475_1': get_form(475, Form.MEGA),
                    '479': get_form(479, Form.NORMAL),
                    '479_1': get_form(479, 'heat'),
                    '479_2': get_form(479, 'wash'),
                    '479_3': get_form(479, 'frost'),
                    '479_4': get_form(479, 'fan'),
                    '479_5': get_form(479, 'mow'),
                    '487': get_form(487, 'altered'),
                    '487_1': get_form(487, 'origin'),
                    '492': get_form(492, 'land'),
                    '492_1': get_form(492, 'sky'),
                    '493': get_form(493, Form.NORMAL),
                    '493_1': get_form(493, 'fighting'),
                    '493_2': get_form(493, 'flying'),
                    '493_3': get_form(493, 'poison'),
                    '493_4': get_form(493, 'ground'),
                    '493_5': get_form(493, 'rock'),
                    '493_6': get_form(493, 'bug'),
                    '493_7': get_form(493, 'ghost'),
                    '493_8': get_form(493, 'steel'),
                    # does not exist
                    # '493_9': get_form(493, ''),
                    '493_10': get_form(493, 'fire'),
                    '493_11': get_form(493, 'water'),
                    '493_12': get_form(493, 'grass'),
                    '493_13': get_form(493, 'electric'),
                    '493_14': get_form(493, 'psychic'),
                    '493_15': get_form(493, 'ice'),
                    '493_16': get_form(493, 'dragon'),
                    '493_17': get_form(493, 'dark'),
                    '493_18': get_form(493, 'fairy'),
                    '521-female': get_form(521, Form.FEMALE),
                    '531_1': get_form(531, Form.MEGA),
                    '550': get_form(550, 'red-striped'),
                    '550_1': get_form(550, 'blue-striped'),
                    '555': get_form(555, Form.NORMAL),
                    '555_1': get_form(555, 'zen'),
                    '585': get_form(585, 'spring'),
                    '585_1': get_form(585, 'summer'),
                    '585_2': get_form(585, 'autumn'),
                    '585_3': get_form(585, 'winter'),
                    '586': get_form(586, 'spring'),
                    '586_1': get_form(586, 'summer'),
                    '586_2': get_form(586, 'autumn'),
                    '586_3': get_form(586, 'winter'),
                    '592-female': get_form(592, Form.FEMALE),
                    '593-female': get_form(593, Form.FEMALE),
                    '641': get_form(641, 'incarnate'),
                    '641_1': get_form(641, 'therian'),
                    '642': get_form(642, 'incarnate'),
                    '642_1': get_form(642, 'therian'),
                    '645': get_form(645, 'incarnate'),
                    '645_1': get_form(645, 'therian'),
                    '646': get_form(646, Form.NORMAL),
                    '646_1': get_form(646, 'white'),
                    '646_2': get_form(646, 'black'),
                    '647': get_form(647, 'ordinary'),
                    '647_1': get_form(647, 'resolute'),
                    '648': get_form(648, 'aria'),
                    '648_1': get_form(648, 'pirouette'),
                    '649': get_form(649, Form.NORMAL),
                    '649_1': get_form(649, 'shock'),
                    '649_2': get_form(649, 'burn'),
                    '649_3': get_form(649, 'shock'),
                    '649_4': get_form(649, 'douse'),
                    '666': get_form(666, 'meadow'),
                    '666_1': get_form(666, 'polar'),
                    '666_2': get_form(666, 'tundra'),
                    '666_3': get_form(666, 'continental'),
                    '666_4': get_form(666, 'garden'),
                    '666_5': get_form(666, 'elegant'),
                    '666_6': get_form(666, 'icy-snow'),
                    '666_7': get_form(666, 'modern'),
                    '666_8': get_form(666, 'marine'),
                    '666_9': get_form(666, 'archipelago'),
                    '666_10': get_form(666, 'high-plains'),
                    '666_11': get_form(666, 'sandstorm'),
                    '666_12': get_form(666, 'river'),
                    '666_13': get_form(666, 'monsoon'),
                    '666_14': get_form(666, 'savanna'),
                    '666_15': get_form(666, 'sun'),
                    '666_16': get_form(666, 'ocean'),
                    '666_17': get_form(666, 'jungle'),
                    '666_18': get_form(666, 'fancy'),
                    '666_19': get_form(666, 'poke-ball'),
                    '668-female': get_form(668, Form.FEMALE),
                    '669': get_form(669, 'red'),
                    '669_1': get_form(669, 'yellow'),
                    '669_2': get_form(669, 'orange'),
                    '669_3': get_form(669, 'blue'),
                    '669_4': get_form(669, 'white'),
                    '670': get_form(670, 'red'),
                    '670_1': get_form(670, 'yellow'),
                    '670_2': get_form(670, 'orange'),
                    '670_3': get_form(670, 'blue'),
                    '670_4': get_form(670, 'white'),
                    '671': get_form(671, 'red'),
                    '671_1': get_form(671, 'yellow'),
                    '671_2': get_form(671, 'orange'),
                    '671_3': get_form(671, 'blue'),
                    '671_4': get_form(671, 'white'),
                    '678-female': get_form(678, Form.FEMALE),
                    '681': get_form(681, 'shield'),
                    '681_1': get_form(681, 'blade'),
                    '710': DISMISS_FORM,
                    '710_1': DISMISS_FORM,
                    '710_2': DISMISS_FORM,
                    # use biggest image only
                    '710_3': get_form(710, Form.NORMAL),
                    '711': DISMISS_FORM,
                    '711_1': DISMISS_FORM,
                    '711_2': DISMISS_FORM,
                    # use biggest image only
                    '711_3': get_form(711, Form.NORMAL),
                    '716': get_form(716, 'active'),
                    '718': get_form(718, '50-percent'),
                    '718_1': get_form(718, '10-percent'),
                    '718_2': get_form(718, 'complete'),
                    '719_1': get_form(719, Form.MEGA),
                    '720': get_form(720, 'confined'),
                    '720_1': get_form(720, 'unbound'),
                    '741': get_form(741, 'baile'),
                    '741_1': get_form(741, 'pom-pom'),
                    '741_2': get_form(741, 'pau'),
                    '741_3': get_form(741, 'sensu'),
                    '745': get_form(745, 'midday'),
                    '745_1': get_form(745, 'midnight'),
                    '745_2': get_form(745, 'dusk'),
                    '746': get_form(746, 'solo'),
                    '746_1': get_form(746, 'school'),
                    '773': get_form(773, Form.NORMAL),
                    '773_1': get_form(773, 'fighting'),
                    '773_2': get_form(773, 'flying'),
                    '773_3': get_form(773, 'poison'),
                    '773_4': get_form(773, 'ground'),
                    '773_5': get_form(773, 'rock'),
                    '773_6': get_form(773, 'bug'),
                    '773_7': get_form(773, 'ghost'),
                    '773_8': get_form(773, 'steel'),
                    # does not exist
                    # '773_9': get_form(773, ''),
                    '773_10': get_form(773, 'fire'),
                    '773_11': get_form(773, 'water'),
                    '773_12': get_form(773, 'grass'),
                    '773_13': get_form(773, 'electric'),
                    '773_14': get_form(773, 'psychic'),
                    '773_15': get_form(773, 'ice'),
                    '773_16': get_form(773, 'dragon'),
                    '773_17': get_form(773, 'dark'),
                    '773_18': get_form(773, 'fairy'),
                    '774': get_form(774, 'meteor'),
                    '774_1': get_form(774, 'core-red'),
                    '774_2': get_form(774, 'core-orange'),
                    '774_3': get_form(774, 'core-yellow'),
                    '774_4': get_form(774, 'core-green'),
                    '774_5': get_form(774, 'core-blue'),
                    '774_6': get_form(774, 'core-indigo'),
                    '774_7': get_form(774, 'core-violet'),
                    '778': get_form(778, 'disguised'),
                    '778_1': get_form(778, 'busted'),
                    '800': get_form(800, Form.NORMAL),
                    '800_1': get_form(800, 'dusk-mane'),
                    '800_2': get_form(800, 'dawn-wings'),
                    '800_3': get_form(800, 'ultra'),
                    '801': get_form(801, Form.NORMAL),
                    '801_1': get_form(801, 'original-color'),
                },
            },
        )
