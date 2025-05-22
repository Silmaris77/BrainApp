import streamlit as st

def get_device_type():
    """
    Determines the type of device being used based on screen width.
    
    Returns:
    - str: 'mobile', 'tablet', or 'desktop'
    """
    # Get the current viewport width
    width = st.session_state.get('viewport_width', 1200)
    
    # Determine device type based on width
    if width < 768:
        return 'mobile'
    elif width < 992:
        return 'tablet'
    else:
        return 'desktop'

def get_responsive_figure_size(device_type=None):
    """
    Returns an appropriate figure size based on the device type
    
    Args:
    - device_type: str, 'mobile', 'tablet', or 'desktop'
    
    Returns:
    - tuple: (width, height) for the figure
    """
    if device_type is None:
        device_type = get_device_type()
    
    if device_type == 'mobile':
        return (5, 4)
    elif device_type == 'tablet':
        return (7, 6)
    else:  # desktop
        return (8, 7)

def responsive_width(desktop_width, tablet_width=None, mobile_width=None):
    """
    Returns the appropriate width based on device type
    
    Args:
    - desktop_width: Width for desktop devices
    - tablet_width: Width for tablet devices (optional)
    - mobile_width: Width for mobile devices (optional)
    
    Returns:
    - float: Width value appropriate for the current device
    """
    device_type = get_device_type()
    
    if device_type == 'mobile' and mobile_width is not None:
        return mobile_width
    elif device_type == 'tablet' and tablet_width is not None:
        return tablet_width
    else:
        return desktop_width

def responsive_columns(num_desktop=3, num_tablet=2, num_mobile=1):
    """
    Creates a responsive column layout
    
    Args:
    - num_desktop: Number of columns for desktop
    - num_tablet: Number of columns for tablet
    - num_mobile: Number of columns for mobile
    
    Returns:
    - list: Streamlit columns based on device type
    """
    device_type = get_device_type()
    
    if device_type == 'mobile':
        return st.columns(num_mobile)
    elif device_type == 'tablet':
        return st.columns(num_tablet)
    else:
        return st.columns(num_desktop)

def responsive_padding(desktop=1.0, tablet=0.7, mobile=0.3):
    """
    Returns the appropriate padding based on device type
    
    Args:
    - desktop: Padding for desktop devices
    - tablet: Padding for tablet devices
    - mobile: Padding for mobile devices
    
    Returns:
    - float: Padding value appropriate for the current device
    """
    device_type = get_device_type()
    
    if device_type == 'mobile':
        return mobile
    elif device_type == 'tablet':
        return tablet
    else:
        return desktop

def responsive_font_size(desktop=16, tablet=14, mobile=12):
    """
    Returns the appropriate font size based on device type
    
    Args:
    - desktop: Font size for desktop devices
    - tablet: Font size for tablet devices
    - mobile: Font size for mobile devices
    
    Returns:
    - int: Font size appropriate for the current device
    """
    device_type = get_device_type()
    
    if device_type == 'mobile':
        return mobile
    elif device_type == 'tablet':
        return tablet
    else:
        return desktop