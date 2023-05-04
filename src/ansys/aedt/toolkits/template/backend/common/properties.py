try:
    from properties_data import PropertiesData
except ModuleNotFoundError:
    from .properties_data import PropertiesData

_default_properties = {}

###############################
# put here below the properties

# general settings
_default_properties["project_name"] = False
_default_properties["design_name"] = False
_default_properties["units"] = False

#############################
# don't touch the lines below

properties = PropertiesData(_default_properties)


def check_property_file_against_defaults(prop_filename):
    """
    Check if property exists in defaults.

    Parameters
    ----------
    prop_filename : str
        Qualified path of the property file to be checked

    Returns
    -------
    bool
        `True` if the files check passes, `False` otherwise
    """
    tmp_properties = PropertiesData(_default_properties)
    try:
        tmp_properties.read_from_file(prop_filename)
        return True
    except Exception as e:
        print(e)
        return False
