"""Defines all existing forms for all pokemon that have special forms.
Each data source maps each of its files to a form which in turn produces standardized names.

Source:
https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_with_form_differences

According to
https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_with_gender_differences
significant differences between male and female pokemon
start happening from generation 5:
    => 521, 592, 593, 668, 678, 876
"""

from dataclasses import dataclass
import itertools
from typing import Any, Dict, Union

from pokemon_image_dataset.utils import name, dename


DISMISS_FORM = object()


class Form:
    NORMAL = '__normal__'
    # normal is implicit as there currently is no non-normal female form
    # with significant differences
    FEMALE = 'female'

    MEGA = 'mega'
    MEGA_X = name('mega', 'x')
    MEGA_Y = name('mega', 'y')
    GIGANTAMAX = 'gigantamax'
    ALOLA = 'alola'
    GALAR = 'galar'
    HISUI = 'hisui'


@dataclass
class PokemonForm:
    """Specifies an appearance of a pokemon."""

    ndex: int
    name: str
    color_only: bool = False

    @property
    def complete_name(self):
        if self.name == Form.NORMAL:
            return f'{self.ndex}'
        else:
            return name(str(self.ndex), self.name)


class NoNormal(tuple):
    ...


def to_kwargs(form_descriptor: Union[str, Dict[str, Any], ]):
    """Converts a form descriptor to kwargs suitable for a PokemonForm instance."""
    if isinstance(form_descriptor, str):
        kwargs = dict(name=form_descriptor)
    elif isinstance(form_descriptor, dict):
        assert all(isinstance(key, str) for key in form_descriptor.keys()), (
            'dict with non-string keys cannot be used as kwargs'
        )
        kwargs = form_descriptor
    return kwargs


def get_instances(ndex, form_descriptors: Union[str, tuple]):
    if not isinstance(form_descriptors, tuple):
        form_descriptors = (form_descriptors,)

    if not isinstance(form_descriptors, NoNormal):
        form_descriptors = (Form.NORMAL, *form_descriptors)

    return tuple(
        PokemonForm(ndex=ndex, **to_kwargs(form))
        for form in form_descriptors
    )


def get_forms(forms_by_ndex):
    default_forms = {
        ndex: (PokemonForm(ndex=ndex, name=Form.NORMAL), )
        for ndex in range(1, max(forms_by_ndex.keys()) + 1)
    }
    return {
        **default_forms,
        **{
            ndex: get_instances(ndex, forms)
            for ndex, forms in forms_by_ndex.items()
        },
    }


GET_FORM_SENTINEL = object()


def get_form(ndex: int, form_name: str, default=GET_FORM_SENTINEL) -> PokemonForm:
    forms = POKEMON_FORMS[ndex]
    matches = [f for f in forms if f.name == form_name]
    if len(matches) == 0 and default is not GET_FORM_SENTINEL:
        return default
    else:
        assert len(
            matches) == 1, (
                f'got {len(matches)} matching forms instead 1 for {name(str(ndex), form_name)}'
            )
        return matches[0]


def no_normal(*forms):
    return NoNormal(forms)


def color_only(*forms):
    return tuple(
        {**to_kwargs(form), 'color_only': True}
        for form in forms
    )




POKEMON_FORMS = get_forms({
    3: (Form.MEGA, Form.GIGANTAMAX),  # Venusaur
    6: (Form.MEGA_X, Form.MEGA_Y, Form.GIGANTAMAX),  # Charizard
    9: (Form.MEGA, Form.GIGANTAMAX),  # Blastoise
    12: Form.GIGANTAMAX,  # Butterfree
    15: Form.MEGA,  # Beedrill
    18: Form.MEGA,  # Pidgeot
    19: Form.ALOLA,  # Rattata
    20: Form.ALOLA,  # Raticate
    25: (
        Form.GIGANTAMAX,
        'cosplay', 'cosplay-rock-star', 'cosplay-belle',
        'cosplay-pop-star', 'cosplay-phd', 'cosplay-libre',
        'cap-original', 'cap-hoenn', 'cap-sinnoh', 'cap-unova',
        'cap-kalos', 'cap-alola', 'cap-partner', 'cap-world',
    ),  # Pikachu
    26: Form.ALOLA,  # Raichu
    27: Form.ALOLA,  # Sandshrew
    28: Form.ALOLA,  # Sandslash
    37: Form.ALOLA,  # Vulpix
    38: Form.ALOLA,  # Ninetales
    50: Form.ALOLA,  # Diglett
    51: Form.ALOLA,  # Dugtrio
    52: (Form.ALOLA, Form.GALAR, Form.GIGANTAMAX),  # Meowth
    53: Form.ALOLA,  # Persian
    58: Form.HISUI,  # Growlithe
    65: Form.MEGA,  # Alakazam
    68: Form.GIGANTAMAX,  # Machamp
    74: Form.ALOLA,  # Geodude
    75: Form.ALOLA,  # Graveler
    76: Form.ALOLA,  # Golem
    77: Form.GALAR,  # Ponyta
    78: Form.GALAR,  # Rapidash
    79: Form.GALAR,  # Slowpoke
    80: (Form.MEGA, Form.GALAR),  # Slowbro
    83: Form.GALAR,  # Farfetch'd
    88: Form.ALOLA,  # Grimer
    89: Form.ALOLA,  # Muk
    94: (Form.MEGA, Form.GIGANTAMAX),  # Gengar
    99: Form.GIGANTAMAX,  # Kingler
    103: Form.ALOLA,  # Exeggutor
    105: Form.ALOLA,  # Marowak
    110: Form.GALAR,  # Weezing
    115: Form.MEGA,  # Kangaskhan
    122: Form.GALAR,  # Mr. Mime
    127: Form.MEGA,  # Pinsir
    130: Form.MEGA,  # Gyarados
    131: Form.GIGANTAMAX,  # Lapras
    133: Form.GIGANTAMAX,  # Eevee
    142: Form.MEGA,  # Aerodactyl
    143: Form.GIGANTAMAX,  # Snorlax
    144: Form.GALAR,  # Articuno
    145: Form.GALAR,  # Zapdos
    146: Form.GALAR,  # Moltres
    150: (Form.MEGA_X, Form.MEGA_Y),  # Mewtwo
    172: 'spiky-eared',  # Pichu
    181: Form.MEGA,  # Ampharos
    199: Form.GALAR,  # Slowking
    201: no_normal(
        'a', 'b', 'c', 'd', 'e', 'f', 'g',
        'h', 'i', 'j', 'k', 'l', 'm', 'n',
        'o', 'p', 'q', 'r', 's', 't', 'u',
        'v', 'w', 'x', 'y', 'z',
        'exclamation', 'question',
    ),  # Unown
    208: Form.MEGA,  # Steelix
    212: Form.MEGA,  # Scizor
    214: Form.MEGA,  # Heracross
    222: Form.GALAR,  # Corsola
    229: Form.MEGA,  # Houndoom
    248: Form.MEGA,  # Tyranitar
    254: Form.MEGA,  # Sceptile
    257: Form.MEGA,  # Blaziken
    260: Form.MEGA,  # Swampert
    263: Form.GALAR,  # Zigzagoon
    264: Form.GALAR,  # Linoone
    282: Form.MEGA,  # Gardevoir
    302: Form.MEGA,  # Sableye
    303: Form.MEGA,  # Mawile
    306: Form.MEGA,  # Aggron
    308: Form.MEGA,  # Medicham
    310: Form.MEGA,  # Manectric
    319: Form.MEGA,  # Sharpedo
    323: Form.MEGA,  # Camerupt
    334: Form.MEGA,  # Altaria
    351: ('sunny', 'rainy', 'snowy'),  # Castform
    354: Form.MEGA,  # Banette
    359: Form.MEGA,  # Absol
    362: Form.MEGA,  # Glalie
    373: Form.MEGA,  # Salamence
    376: Form.MEGA,  # Metagross
    380: Form.MEGA,  # Latias
    381: Form.MEGA,  # Latios
    382: 'primal',  # Kyogre
    383: 'primal',  # Groudon
    384: Form.MEGA,  # Rayquaza
    386: ('attack', 'defense', 'speed'),  # Deoxys
    412: no_normal('plant', 'sandy', 'trash'),  # Burmy
    413: no_normal('plant', 'sandy', 'trash'),  # Wormadam
    421: no_normal('overcast', 'sunshine'),  # Cherrim
    422: no_normal('east', 'west'),  # Shellos
    423: no_normal('east', 'west'),  # Gastrodon
    428: Form.MEGA,  # Lopunny
    445: Form.MEGA,  # Garchomp
    448: Form.MEGA,  # Lucario
    460: Form.MEGA,  # Abomasnow
    475: Form.MEGA,  # Gallade
    479: ('fan', 'frost', 'heat', 'mow', 'wash'),  # Rotom
    487: no_normal('altered', 'origin'),  # Giratina
    492: no_normal('land', 'sky'),  # Shaymin
    # TODO: COLOR ONLY
    493: (
        'bug', 'dark', 'dragon', 'electric', 'fighting', 'fire',
        'flying', 'ghost', 'grass', 'ground', 'ice', 'fairy',
        'poison', 'psychic', 'rock', 'steel', 'water',
    ),  # Arceus
    521: Form.FEMALE,  # Unfezant
    531: Form.MEGA,  # Audino
    550: no_normal('blue-striped', 'red-striped'),  # Basculin
    554: Form.GALAR,  # Darumaka
    555: ('zen', Form.GALAR, f'{Form.GALAR}-zen'),  # Darmanitan
    569: Form.GIGANTAMAX,  # Garbodor
    # TODO: COLOR ONLY
    585: no_normal('spring', 'summer', 'autumn', 'winter'),  # Deerling
    586: no_normal('spring', 'summer', 'autumn', 'winter'),  # Sawsbuck
    592: Form.FEMALE,  # Frillish
    593: Form.FEMALE,  # Jellicent
    628: Form.HISUI,  # Braviary
    641: no_normal('incarnate', 'therian'),  # Tornadus
    642: no_normal('incarnate', 'therian'),  # Thundurus
    643: 'overdrive',  # Reshiram
    644: 'overdrive',  # Zekrom
    645: no_normal('incarnate', 'therian'),  # Landorus
    646: (
        'black', 'black-overdrive',
        'white', 'white-overdrive',
    ),  # Kyurem
    647: no_normal('ordinary', 'resolute'),  # Keldeo
    648: no_normal('aria', 'pirouette'),  # Meloetta
    # TODO: COLOR ONLY
    649: ('burn', 'chill', 'douse', 'shock'),  # Genesect
    658: 'ash',  # Greninja
    # TODO: COLOR ONLY
    666: (
        'archipelago', 'continental', 'elegant', 'fancy', 'garden', 'high-plains',
        'icy-snow', 'jungle', 'marine', 'meadow', 'modern', 'monsoon',
        'ocean', 'poke-ball', 'polar', 'river', 'sandstorm', 'savanna', 'sun', 'tundra',
    ),  # Vivillon
    668: Form.FEMALE,  # Pyroar
    # TODO: COLOR ONLY
    669: no_normal('blue', 'orange', 'red', 'white', 'yellow'),  # Flabébé
    # TODO: COLOR ONLY except 'az'
    670: ('blue', 'orange', 'red', 'white', 'yellow', 'az'),  # Floette
    # TODO: COLOR ONLY
    671: ('blue', 'orange', 'red', 'white', 'yellow'),  # Florges
    676: (
        'dandy', 'debutante', 'diamond', 'heart', 'kabuki',
        'la-reine', 'matron', 'pharaoh', 'star',
    ),  # Furfrou
    678: Form.FEMALE,  # Meowstic
    681: no_normal('blade', 'shield'),  # Aegislash
    # 710, 711 => size differences don't matter for us
    716: no_normal('active', 'neutral'),  # Xerneas
    # Zygarde
    718: no_normal('cell', 'core', '10-percent', '50-percent', 'complete'),
    719: Form.MEGA,  # Diancie
    720: no_normal('confined', 'unbound'),  # Hoopa
    741: no_normal('baile', 'pau', 'pom-pom', 'sensu'),  # Oricorio
    745: no_normal('dusk', 'midday', 'midnight'),  # Lycanroc
    746: no_normal('solo', 'school'),  # Wishiwashi
    773: (
        'bug', 'dark', 'dragon', 'electric', 'fairy', 'fighting',
        'fire', 'flying', 'ghost', 'grass', 'ground', 'ice',
        'poison', 'psychic', 'rock', 'steel', 'water',
    ),  # Silvally
    774: no_normal(
        'meteor',
        *color_only(
            'core-blue', 'core-green', 'core-indigo', 'core-orange',
            'core-red', 'core-violet', 'core-yellow',
        ),
    ),  # Minior
    778: no_normal('busted', 'disguised'),  # Mimikyu
    791: 'radiant-sun',  # Solgaleo
    792: 'full-moon',  # Lunala
    800: ('dusk-mane', 'dawn-wings', 'ultra'),  # Necrozma
    # TODO: COLOR ONLY
    801: 'original-color',  # Magearna
    802: 'zenith',  # Marshadow
    809: Form.GIGANTAMAX,  # Melmetal
    812: Form.GIGANTAMAX,  # Rillaboom
    815: Form.GIGANTAMAX,  # Cinderace
    818: Form.GIGANTAMAX,  # Inteleon
    823: Form.GIGANTAMAX,  # Corviknight
    826: Form.GIGANTAMAX,  # Orbeetle
    834: Form.GIGANTAMAX,  # Drednaw
    839: Form.GIGANTAMAX,  # Coalossal
    841: Form.GIGANTAMAX,  # Flapple
    842: Form.GIGANTAMAX,  # Appletun
    844: Form.GIGANTAMAX,  # Sandaconda
    845: ('gorging', 'gulping'),  # Cramorant
    849: no_normal(Form.GIGANTAMAX, 'amped', 'low-key'),  # Toxtricity
    851: Form.GIGANTAMAX,  # Centiskorch
    854: no_normal('antique', 'phony'),  # Sinistea
    855: no_normal('antique', 'phony'),  # Polteageist
    858: Form.GIGANTAMAX,  # Hatterene
    861: Form.GIGANTAMAX,  # Grimmsnarl
    869: no_normal(
        Form.GIGANTAMAX,
        # TODO: COLOR ONLY
        *[
            f'{cream}-{sweet}' for cream, sweet in itertools.product(
                [
                    'vanilla-cream', 'ruby-cream', 'matcha-cream', 'mint-cream', 'lemon-cream',
                    'salted-cream', 'ruby-swirl', 'caramel-swirl', 'rainbow-swirl',
                ],
                [
                    'strawberry-sweet', 'love-sweet', 'berry-sweet', 'clover-sweet', 'flower-sweet',
                    'star-sweet', 'ribbon-sweet',
                ],
            )
        ],
    ),  # Alcremie
    875: no_normal('ice-face', 'noice-face'),  # Eiscue
    877: no_normal('full-belly', 'hangry'),  # Morpeko
    879: Form.GIGANTAMAX,  # Copperajah
    884: Form.GIGANTAMAX,  # Duraludon
    888: no_normal('hero-of-many-battles', 'crowned-sword'),  # Zacian
    889: no_normal('hero-of-many-battles', 'crowned-shield'),  # Zamazenta
    890: 'eternamax',  # Eternatus
    # Urshufi
    892: no_normal(Form.GIGANTAMAX, 'single-strike', 'rapid-strike'),
    893: 'dada',  # Zarude
    898: ('ice-rider', 'shadow-rider'),  # Calyrex
})
