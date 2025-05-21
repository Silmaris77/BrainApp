import streamlit as st
import random
import altair as alt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from data.users import load_user_data, save_user_data
from data.test_questions import DEGEN_TYPES
from data.neuroleader_types import NEUROLEADER_TYPES
from config.settings import DAILY_MISSIONS, XP_LEVELS, USER_AVATARS
from data.lessons import load_lessons
from utils.goals import get_user_goals, calculate_goal_metrics
from utils.daily_missions import get_daily_missions_progress
from views.degen_test import plot_radar_chart as plot_degen_radar_chart
from views.neuroleader_test import plot_radar_chart as plot_neuroleader_radar_chart
from utils.material3_components import apply_material3_theme
from utils.layout import get_device_type, responsive_grid, responsive_container, toggle_device_view
from utils.components import (
    zen_header, mission_card, degen_card, progress_bar, stat_card, 
    xp_level_display, zen_button, notification, leaderboard_item, 
    add_animations_css, data_chart, user_stats_panel, lesson_card
)
