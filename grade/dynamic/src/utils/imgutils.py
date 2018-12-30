from io import BytesIO
import base64


def encode_img_base64(fig):
    """Encode figure as Base64 string.
    
    Args:
        fig: matplotlib.figure.Figure object.
    
    Returns:
        Encoded Base 64 string.
    """

    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='png')

    encoded = base64.b64encode(tmpfile.getvalue())
    return encoded


def embedded_base64_markdown(fig):
    """Markdown showing up a figure.
    
    Args:
        fig: matplotlib.figure.Figure object.
    
    Returns:
        String in markdown showing the figure.
    """
    return '![](data:image/png;base64,{})'.format(
        encode_img_base64(fig))