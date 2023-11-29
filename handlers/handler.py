from aiogram import Router, F,types
from main import Bot
import os
from dotenv import load_dotenv
from aiogram.filters.command import Command
from aiogram.types import Message,CallbackQuery
from aiogram.types.message import ContentType
from models import get_description,add_user_and_purchases,get_color_id,get_memory_id
# from keyboards.keyboard import main
import keyboards.keyboard as kb

load_dotenv('.env')
PAYMENTS_TOKEN = os.getenv("PAYMENTS_TOKEN")


class Settings:
    def __init__(self):
        self.model = None
        self.color = None
        self.memory = None

    def set_model(self,value):
        self.model = value

    def set_color(self,value):
        self.color = value

    def set_memory(self,value):
        self.memory = value

    def get_settings(self):
        return {
            'model': self.model,
            'color': self.color,
            'memory': self.memory
        }

router = Router()

settings = Settings()





photos = {
    '1': 'https://i.pinimg.com/564x/86/5b/4f/865b4ffa4d109700e22343051ae4922f.jpg',
    '2': 'https://i.pinimg.com/564x/c9/0b/73/c90b7302d866c27a7263b5ec49a82e2b.jpg',
    '3': 'https://i.pinimg.com/564x/df/10/8e/df108ea01b988b641e02e28a518c4997.jpg'
}


@router.message(Command("start"))
async def command_start(message :types.Message):
    await message.answer( text='hello my owner',reply_markup=kb.main)



@router.message(F.text == 'Католог')
async def catalog(message :Message):
    await message.answer('Выберите вариант из католога', reply_markup= await kb.categories())



@router.callback_query(F.data.startswith('category_'))
async def category_selected(callback: CallbackQuery): 
    await callback.message.delete() 
    category_id = callback.data.split('_')[1]
    if category_id == "1":
        await callback.message.answer('Выберите вариант модели', reply_markup= await kb.models())
    await callback.answer("Выбрано!")


@router.callback_query(F.data.startswith('model_'))
async def model_selected(callback: CallbackQuery,bot: Bot): 
    await callback.message.delete()
    model_id = callback.data.split('_')[1]
    text = await get_description(model_id)
    settings.set_model(model_id)
    photo_path = photos[model_id]
    if model_id == "1":
        await bot.send_photo(callback.message.chat.id, photo=photo_path, caption=f'{text.description}\n\n цена {text.price}', reply_markup= kb.color_kb)
    elif model_id == '2':
        await bot.send_photo(callback.message.chat.id, photo=photo_path, caption=f'{text.description}\n\n цена {text.price}', reply_markup= kb.color_kb)
    elif model_id == '3':
        await bot.send_photo(callback.message.chat.id, photo=photo_path, caption=f'{text.description}\n\n цена {text.price}', reply_markup= kb.color_kb)
    await callback.answer("Выбрано!")
    
    

    
@router.callback_query(F.data.startswith('select_'))
async def select_selected(callback: CallbackQuery,bot: Bot): 
    await callback.message.delete()
    model_id = settings.get_settings()['model']
    select = callback.data.split('_')[1]
    await bot.send_photo(callback.message.chat.id, photo=photos[model_id], caption='Выбирите цвет', reply_markup= await kb.colors(model_id)) 


@router.callback_query(F.data.startswith('color_'))
async def color_selected(callback: CallbackQuery,bot: Bot): 
    await callback.message.delete()

    model_id = settings.get_settings()['model']
    select = callback.data.split('_')[1]
    settings.set_color(select)
    await bot.send_photo(callback.message.chat.id, photo=photos[model_id], caption='Выбирите память', reply_markup= await kb.memory(model_id)) 
    



@router.callback_query(F.data.startswith('memory_'))
async def memory_selected(callback: CallbackQuery,bot: Bot): 
    await callback.message.delete()
    model_id = settings.get_settings()['model']
    color_id = settings.get_settings()['color']
    select = callback.data.split('_')[1]
    settings.set_memory(select)
    photo_path = photos[model_id]
    text = await get_description(model_id)
    color = await get_color_id(color_id)
    memory = await get_memory_id(select)
    await bot.send_photo(callback.message.chat.id, photo=photo_path, caption=f'{text.description}\n\n цена {text.price}\n\n цвет {color.name}\n\n память {memory.memory}', reply_markup= kb.buy_and_exit)
      

@router.callback_query(F.data.startswith('select2_'))
async def buy_or_exit_selected(callback: CallbackQuery,bot:Bot): 
    await callback.message.delete() 
    select = callback.data.split('_')[1]
    if select == 'buy':
        model = settings.get_settings()['model']
        color = settings.get_settings()['color']
        memory = settings.get_settings()['memory']
        text_id = await get_description(model)
        color_id = await get_color_id(color)
        memory_id = await get_memory_id(memory)
        photo_path = photos[model]
        user_id = callback.from_user.id
        PRICE = types.LabeledPrice(label=text_id.name,amount=text_id.price*100)
        await add_user_and_purchases(user_id,model,color,memory)
        if PAYMENTS_TOKEN.split(':')[1] == 'TEST':
            await  callback.message.answer('Оплата товара')
            await bot.send_invoice(callback.message.chat.id,
                title=text_id.name,
                description=f'цвет {color_id.name}, память {memory_id.memory} Гб',
                provider_token=PAYMENTS_TOKEN,
                currency='UAH',
                photo_url=photo_path,
                is_flexible=False,
                prices=[PRICE], 
                start_parameter='onedwdwdwd',
                payload='test-infewif')

    elif select == 'exit':
        settings.set_color(None)
        settings.set_memory(None)   
        settings.set_model(None)
        await callback.message.answer('Выберите вариант из католога', reply_markup= await kb.categories())

@router.pre_checkout_query(lambda query:True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery,bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)



@router.message(F.content_type == types.ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message, bot: Bot):
    print('successful_payment:')
    pmnt = message.successful_payment
    for key in pmnt.__fields__:
        print(f'{key} = {getattr(pmnt, key)}')
    await bot.send_message(
        message.chat.id,
        f'Successful payment: {pmnt.total_amount // 100} {pmnt.currency} all good',
    )

