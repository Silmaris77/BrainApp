"""
Moduł inicjalizacyjny dla nowego systemu UI.
Importuj ten moduł, aby uzyskać dostęp do wszystkich komponentów UI.
"""

# Import komponentów
from utils.ui.components.cards import (
    stat_card,
    skill_card,
    mission_card,
    lesson_card
)

from utils.ui.components.interactive import (
    zen_button,
    notification,
    progress_bar
)

from utils.ui.components.text import (
    zen_header,
    quote_block,
    tip_block,
    content_section
)

from utils.ui.layouts.grid import (
    create_grid_container,
    render_dashboard_header,
    render_stats_section,
    render_two_column_layout,
    get_device_type,
    responsive_container,
    responsive_grid
)

from utils.ui.theme_manager import (
    load_theme,
    get_current_theme,
    set_theme,
    theme_selector
)

# Import funkcji mostkujących (bridge)
from utils.ui.bridge import (
    initialize_bridge,
    bridge_degen_card,
    bridge_stat_card,
    bridge_mission_card,
    bridge_lesson_card,
    bridge_content_section,
    bridge_quote_block,
    bridge_tip_block,
    bridge_zen_button,
    bridge_notification,
    bridge_progress_bar
)

# Funkcja inicjalizacyjna
def initialize_ui(theme_name=None):
    """
    Inicjalizuje system UI.
    
    Parametry:
    - theme_name: Nazwa motywu do załadowania (opcjonalna)
      Jeśli nie podano, użyje motywu zapisanego w sesji lub domyślnego.
    
    Zwraca:
    - bool: True jeśli inicjalizacja się powiodła, False w przeciwnym razie
    """
    # Jeśli podano nazwę motywu, użyj jej
    if theme_name:
        return set_theme(theme_name)
    
    # W przeciwnym razie użyj zapisanego motywu lub domyślnego
    current_theme = get_current_theme()
    return load_theme(current_theme)

# Wersja
__version__ = "1.0.0"
