


class ModuleNotCheckedOut(Exception):
    """module does not exist"""


class InvalidModuleFile(Exception):
    """provided module file does not exist"""


class MetadataJsonMissing(Exception):
    """no metadata.json for module"""