class Validators:

    @staticmethod
    def validate_mod_name(mod_name: str) -> str:
        if not mod_name or not isinstance(mod_name, str):
            raise ValueError('O nome de mod não pode ser vazio ou nulo.')
        
        to_replace = [
            ('_', ''),
            (' - ', '_'),
            (' ', '_'),
            ('-', '_'),
            ('/', '_'),
            ('\\', '_'),
            (':', '_'),
            ('*', '_'),
            ('?', '_'),
            ('"', '_'),
            ('<', '_'),
            ('>', '_'),
            ('|', '_')
        ]
        for old, new in to_replace:
            mod_name = mod_name.replace(old, new)
        return mod_name.lower()