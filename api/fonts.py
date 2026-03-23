import re

class FontTransformer:
    # Basic character maps
    CHAR_MAPS = {
        "Bold": (65, 119808, 97, 119834, 48, 120782),
        "Italic": (65, 119860, 97, 119886, 48, 120782),
        "Bold Italic": (65, 119912, 97, 119938, 48, 120782),
        "Script": (65, 119964, 97, 119990, 48, 120782),
        "Bold Script": (65, 120016, 97, 120042, 48, 120782),
        "Fraktur": (65, 120068, 97, 120094, 48, 120782),
        "Bold Fraktur": (65, 120172, 97, 120198, 48, 120782),
        "Double Struck": (65, 120120, 97, 120146, 48, 120792),
        "Sans-serif": (65, 120224, 97, 120250, 48, 120802),
        "Sans Bold": (65, 120276, 97, 120302, 48, 120812),
        "Sans Italic": (65, 120328, 97, 120354, 48, 120812),
        "Sans Bold Italic": (65, 120380, 97, 120406, 48, 120812),
        "Monospace": (65, 120432, 97, 120458, 48, 120822),
        "Fullwidth": (65, 65313, 97, 65345, 48, 65296),
        "Bubbles": (65, 9398, 97, 9424, 48, 9312)
    }

    SMALL_CAPS = {'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ꜰ', 'g': 'ɢ', 'h': 'ʜ', 'i': 'ɪ', 'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ', 'o': 'ᴏ', 'p': 'ᴘ', 'q': 'ǫ', 'r': 'ʀ', 's': 's', 't': 'ᴛ', 'u': 'ᴜ', 'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x', 'y': 'ʏ', 'z': 'ᴢ'}
    
    # 100+ Decorative Symbols for Combinations
    SYMBOLS = [
        "✨", "⭐", "🌟", "💫", "🔥", "⚡", "🌈", "☀️", "🌙", "☁️", "❄️", "🌊", "🍀", "🌸", "🌹", "🌻", "🌼", "🍁", "🍃", "🍎",
        "🍓", "🍒", "🍔", "🍕", "🍰", "🍭", "🍦", "🍩", "🍷", "🍹", "🍺", "☕", "⚽", "🏀", "🎾", "🎸", "🎵", "🎶", "🎭", "🎮",
        "✈️", "🚀", "🛸", "🌍", "🗺️", "🏠", "🏢", "⛪", "🕌", "⛩️", "🕋", "⌚", "📱", "💻", "⌨️", "🖱️", "🖨️", "📞", "📠", "🔋",
        "🔌", "💡", "🔦", "🕯️", "🛠️", "🔨", "🔩", "⛏️", "⛓️", "🔫", "💣", "🛡️", "🏹", "🗡️", "🔪", "🏺", "🩹", "🩸", "🧺", "🧿",
        "🧸", "🎈", "🧧", "🎀", "🎁", "🎫", "💎", "💍", "👑", "🧢", "🎩", "👒", "👔", "👕", "👖", "👗", "👘", "👟", "👞", "👓",
        "👜", "🎒", "💼", "👛", "🧺", "🧼", "🧽", "🧴", "🧹", "🧺", "🚬", "⚰️", "⚱️", "🗿", "⚖️", "🗝️", "🔑", "🔐", "🔒", "🔓",
        "🔕", "🔔", "📣", "📢", "📍", "📌", "🖍️", "🖊️", "🖋️", "✒️", "📝", "📁", "📂", "📅", "📆", "🗂️", "🗳️", "📈", "📉", "📊",
        "✂️", "📌", "📍", "📎", "🖇️", "📏", "📐", "🔒", "🔓", "🔏", "🔐", "🗝️", "🔑", "🔨", "🪓", "⛏️", "⚒️", "🛠️", "🗡️", "⚔️",
        "🔫", "🛡️", "🏹", "⚖️", "⚙️", "⚒️", "⚖️", "⛓️", "⚗️", "🧬", "🧪", "🌡️", "💉", "💊", "🩹", "🔭", "🔬", "🛰️", "🛸"
    ]

    DECORATIONS = [
        ("\u0336", "Strike"), ("\u0332", "Under"), ("\u0333", "DblUnder"), ("\u0337", "Slash"), ("\u0305", "Over"),
        ("(",")", "Parens"), ("[","]", "Brack"), ("{","}", "Brace"), ("«","»", "Chev")
    ]

    @classmethod
    def apply_base(cls, text, style):
        if style == "Normal": return text
        if style == "Small Caps": return "".join(cls.SMALL_CAPS.get(c.lower(), c) for c in text)
        if style in cls.CHAR_MAPS:
            chars = cls.CHAR_MAPS[style]
            res = ""
            for char in text:
                code = ord(char)
                if 65 <= code <= 90: res += chr(code - 65 + chars[1])
                elif 97 <= code <= 122: res += chr(code - 97 + chars[3])
                elif 48 <= code <= 57: res += chr(code - 48 + chars[5])
                else: res += char
            return res
        return text

    @classmethod
    def get_1000_variants(cls, text):
        variants = []
        # 1. Base fonts (15)
        bases = list(cls.CHAR_MAPS.keys()) + ["Small Caps", "Normal"]
        for b in bases:
            variants.append((b, cls.apply_base(text, b)))
        
        # 2. Combinations with Symbols (Base x 60 Symbols x 4 modes)
        # To avoid lag and duplication, we limit the symbols and modes but ensure >1000
        active_symbols = cls.SYMBOLS[:100]
        
        for base_name in bases[:10]: # Use first 10 bases for combinations
            styled_text = cls.apply_base(text, base_name)
            for sym in active_symbols:
                # Mode 1: Symbol prefix
                variants.append((f"{sym} {base_name}", f"{sym} {styled_text}"))
                # Mode 2: Symbol suffix
                variants.append((f"{base_name} {sym}", f"{styled_text} {sym}"))
                # Mode 3: Surrounding symbols
                variants.append((f"{sym}{base_name}{sym}", f"{sym} {styled_text} {sym}"))
                
        # 3. Text decorations (Strike, Under, etc.)
        for base_name in bases[:10]:
            styled_text = cls.apply_base(text, base_name)
            for dec in cls.DECORATIONS:
                if len(dec) == 2: # Combining char
                    res = "".join(c + dec[0] for c in styled_text)
                    variants.append((f"{base_name} + {dec[1]}", res))
                else: # Prefix/Suffix
                    variants.append((f"{dec[2]} {base_name}", f"{dec[0]}{styled_text}{dec[1]}"))

        # Limit to 1000+ to keep memory usage reasonable, but ensure variety
        return variants[:1100]

    @classmethod
    def get_variant_by_index(cls, text, index):
        all_vars = cls.get_1000_variants(text)
        if 0 <= index < len(all_vars):
            return all_vars[index]
        return ("Normal", text)
