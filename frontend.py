from lib import (
    get_all_models,
    get_black_white_models,
    get_color_models,
    get_default_black_white_model,
    get_default_color_model,
    set_default_black_white_model,
    set_default_color_model,
)


def list_all_models():
    bw_models, c_models = get_all_models()
    default_bw_model = get_default_black_white_model()
    default_c_model = get_default_color_model()
    message = "# All Available Models"
    if len(bw_models) > 0:
        message += "\n## Black and White Models:"
        for bw_model in bw_models:
            if bw_model == default_bw_model:
                message += "\n- `" + bw_model + "`\t**default**"
            else:
                message += "\n- `" + bw_model + "`"
    message += "\n"
    if len(c_models) > 0:
        message += "\n## Color Models:"
        for c_model in c_models:
            if c_model == default_c_model:
                message += "\n- `" + c_model + "`\t**default**"
            else:
                message += "\n- `" + c_model + "`"
    return message


def list_bw_models():
    bw_models = get_black_white_models()
    default_bw_model = get_default_black_white_model()
    message = ""
    if len(bw_models) > 0:
        message += "# Available Black and White Models:"
        for bw_model in bw_models:
            if bw_model == default_bw_model:
                message += "\n- `" + bw_model + "`\t**default**"
            else:
                message += "\n- `" + bw_model + "`"
    else:
        message += "# No Black and White Models available"
    return message


def list_c_models():
    c_models = get_color_models()
    default_c_model = get_default_color_model()
    message = ""
    if len(c_models) > 0:
        message += "# Available Color Models:"
        for c_model in c_models:
            if c_model == default_c_model:
                message += "\n- `" + c_model + "`\t**default**"
            else:
                message += "\n- `" + c_model + "`"
    else:
        message += "# No Color Models available"
    return message


def set_default_bw_model(model_name):
    if set_default_black_white_model(model_name):
        return "Default Black and White Model has been set to `" + model_name + "`"
    bw_models = get_black_white_models()
    if len(bw_models) == 0:
        return "Could not set a default Black and White Model because there are no Black and White Models available"
    else:
        return (
            "Could not set default Black and White Model to `"
            + model_name
            + "`\n"
            + list_bw_models()
        )


def set_default_c_model(model_name):
    if set_default_color_model(model_name):
        return "Default Color Model has been set to `" + model_name + "`"
    c_models = get_color_models()
    if len(c_models) == 0:
        return "Could not set a default Color Model because there are no Color Models available"
    else:
        return (
            "Could not set default Color Model to `"
            + model_name
            + "`\n"
            + list_c_models()
        )


print(set_default_c_model("4x_eula_digimanga_bw_v2_nc1_307k.pth"))
