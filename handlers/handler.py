from aiogram import Router, F,types
from aiogram.filters.command import Command
from aiogram.types import Message

# from keyboards.keyboard import main
import keyboards.keyboard as kb


router = Router()

@router.message(Command("start"))
async def command_start(message :types.Message):
    await message.answer( text='hello my owner',reply_markup=kb.main)


@router.message(F.text == 'Католог')
async def catalog(message :Message):
    await message.answer('Выберите вариант из католога', reply_markup= await kb.categories())





