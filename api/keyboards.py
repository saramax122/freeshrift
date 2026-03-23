from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_font_keyboard(variants_subset: list, current_page: int, total_pages: int, start_index: int):
    builder = InlineKeyboardBuilder()
    
    # Font style buttons (10 per page)
    # variants_subset is a list of (name, styled_text)
    for i, (name, _) in enumerate(variants_subset):
        # We store the global index in callback_data to retrieve it later
        global_idx = start_index + i
        # Use a short prefix to save space in callback_data
        builder.row(InlineKeyboardButton(text=name, callback_data=f"fnt_{global_idx}"))
    
    # Pagination row
    nav_buttons = []
    if current_page > 0:
        nav_buttons.append(InlineKeyboardButton(text="⬅️", callback_data=f"pg_{current_page - 1}"))
    
    # Page indicator
    nav_buttons.append(InlineKeyboardButton(text=f"{current_page + 1}/{total_pages}", callback_data="ignore"))
    
    if current_page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"pg_{current_page + 1}"))
    
    builder.row(*nav_buttons)
    
    # Jump buttons (e.g., +10 pages)
    jump_buttons = []
    if current_page >= 10:
        jump_buttons.append(InlineKeyboardButton(text="⏪ -10", callback_data=f"pg_{max(0, current_page - 10)}"))
    if current_page + 10 < total_pages:
        jump_buttons.append(InlineKeyboardButton(text="+10 ⏩", callback_data=f"pg_{min(total_pages - 1, current_page + 10)}"))
    
    if jump_buttons:
        builder.row(*jump_buttons)
        
    return builder.as_markup()
