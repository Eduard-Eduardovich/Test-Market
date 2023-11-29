from models import get_categories,get_models,get_colors,get_memory
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from aiogram.utils.keyboard import InlineKeyboardBuilder


main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Католог')],
    [KeyboardButton(text='Контакты')]
], resize_keyboard=True, input_field_placeholder='Выбирите пункт ниже')

color_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Цвет', callback_data='select_color')      
        ]

    ]
    
)


async def categories():
    categories_kb = InlineKeyboardBuilder()
    categories = await get_categories()
    for category in categories:
        categories_kb.add(InlineKeyboardButton(text=category.name, callback_data=f'category_{category.id}'))
    return categories_kb.adjust(2).as_markup()


async def models():
    models_kb = InlineKeyboardBuilder()
    models = await get_models()
    for model in models:
        models_kb.add(InlineKeyboardButton(text= model.name, callback_data=f'model_{model.id}'))
    return models_kb.adjust(2).as_markup()


async def colors(color_product_id):
    colors_kb = InlineKeyboardBuilder()
    colors = await get_colors(color_product_id)
    for color in colors:
        colors_kb.add(InlineKeyboardButton(text= color.name, callback_data=f'color_{color.id}'))
    return colors_kb.adjust(1).as_markup() 


async def memory(memory_product_id):
    memory_kb = InlineKeyboardBuilder()
    memorys = await get_memory(memory_product_id)
    for memory in memorys:
        memory_kb.add(InlineKeyboardButton(text= memory.memory,callback_data=f'memory_{memory.id}'))
    return memory_kb.adjust(1).as_markup()


buy_and_exit = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Купить', callback_data='select2_buy')      
        ],
        [
            InlineKeyboardButton(text='Отмена', callback_data='select2_exit')     
        ]  
    ]
    
)