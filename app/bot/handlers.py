import os

from aiogram import types, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import Router
import requests
from fsm_states import RegistrationStates, ScoreStates

API_URL = os.getenv("API_URL")

router = Router()

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Регистрация")],
        [KeyboardButton(text="Ввести баллы")],
        [KeyboardButton(text="Мои баллы")],
    ],
    resize_keyboard=True
)

#----------------- check_student_id -------------------------------
async def validate_student_id(message: types.Message, state: FSMContext | None = None) -> int | None:
    try:
        student_id = int(message.text)
    except ValueError:
        await message.answer(
            "Введите корректный числовой ID студента."
        )
        return None

    r = requests.get(f"{API_URL}/students/")
    if r.status_code != 200:
        await message.answer(
            "Ошибка сервера. Попробуйте позже.",
            reply_markup=main_kb
        )
        return None

    students = r.json()
    if not any(s["id"] == student_id for s in students):
        await message.answer(
            "Студент с таким ID не найден. Попробуйте снова.",
            reply_markup=main_kb
        )
        if state:
            await state.clear()
        return None

    return student_id

# ------------------ /start ------------------

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я бот для ввода баллов ЕГЭ.\n"
        "Выберите действие кнопкой ниже 👇",
        reply_markup=main_kb
    )

# ------------------ /register ------------------
@router.message(Command("register"))
async def cmd_register(message: types.Message, state: FSMContext):
    await message.answer("Введите ваше имя:")
    await state.set_state(RegistrationStates.waiting_first_name)

@router.message(F.text == "Регистрация")
async def register_button(message: types.Message, state: FSMContext):
    await cmd_register(message, state)

@router.message(RegistrationStates.waiting_first_name)
async def first_name(message: types.Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await message.answer("Введите вашу фамилию:")
    await state.set_state(RegistrationStates.waiting_last_name)

@router.message(RegistrationStates.waiting_last_name)
async def last_name(message: types.Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    data = await state.get_data()
    payload = {"first_name": data["first_name"], "last_name": data["last_name"]}
    r = requests.post(f"{API_URL}/students/register", json=payload)
    if r.status_code == 200:
        student_id = r.json()["id"]
        await message.answer(
            f"Вы зарегистрированы! Ваш ID: {student_id}\nСохраните его для ввода баллов.",
            reply_markup=main_kb)
    else:
        await message.answer("Ошибка регистрации")
    await state.clear()

# ------------------ /enter_scores ------------------
@router.message(Command("enter_scores"))
async def cmd_enter_scores(message: types.Message, state: FSMContext):
    await message.answer("Введите ваш ID студента:")
    await state.set_state(ScoreStates.waiting_subject)

@router.message(F.text == "Ввести баллы")
async def enter_scores_button(message: types.Message, state: FSMContext):
    await cmd_enter_scores(message, state)

@router.message(ScoreStates.waiting_subject)
async def get_student_id(message: types.Message, state: FSMContext):
    student_id = await validate_student_id(message, state)
    if student_id is None:
        return

    await state.update_data(student_id=student_id)

    r = requests.get(f"{API_URL}/subjects/")
    subjects = r.json()
    buttons = [[KeyboardButton(text=sub["name"])] for sub in subjects]

    kb = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    await message.answer("Выберите предмет:", reply_markup=kb)
    await state.set_state(ScoreStates.waiting_score)

@router.message(ScoreStates.waiting_score)
async def get_score(message: types.Message, state: FSMContext):
    data = await state.get_data()
    student_id = int(data["student_id"])
    subject_name = message.text
    subjects = requests.get(f"{API_URL}/subjects/").json()
    subject_id = next((s["id"] for s in subjects if s["name"] == subject_name), None)
    if subject_id is None:
        await message.answer("Предмет не найден. Попробуйте снова.")
        return
    await state.update_data(subject_id=subject_id)
    await message.answer(f"Введите балл по {subject_name} (0-100):")


    await state.set_state(ScoreStates.waiting_score_value)

@router.message(ScoreStates.waiting_score_value)
async def save_score(message: types.Message, state: FSMContext):
    data = await state.get_data()
    student_id = int(data["student_id"])
    subject_id = data["subject_id"]
    try:
        value = int(message.text)
        if value < 0 or value > 100:
            raise ValueError
    except ValueError:
        await message.answer("Введите корректный балл от 0 до 100.")
        return
    payload = {"student_id": student_id, "subject_id": subject_id, "value": value}
    r = requests.post(f"{API_URL}/scores/add", json=payload)
    if r.status_code == 200:
        await message.answer(
            "Балл успешно сохранён ✅",
            reply_markup=main_kb)
    else:
        await message.answer(
            "Ошибка при сохранении балла. Пожалуйста попробуйте снова",
            reply_markup=main_kb)
    await state.clear()

# ------------------ /view_scores ------------------
@router.message(Command("view_scores"))
async def view_scores(message: types.Message, state: FSMContext):
    await message.answer("Введите ваш ID студента:")
    await state.set_state(ScoreStates.view_scores)

@router.message(F.text == "Мои баллы")
async def view_scores_button(message: types.Message, state: FSMContext):
    await view_scores(message, state)

@router.message(ScoreStates.view_scores)
async def show_scores(message: types.Message, state: FSMContext):
    student_id = await validate_student_id(message, state)
    if student_id is None:
        return

    r = requests.get(f"{API_URL}/scores/{student_id}")
    if r.status_code == 200:
        scores = r.json()
        if not scores:
            await message.answer("У этого студента нет баллов.", reply_markup=main_kb)
        else:
            text = "\n".join([f"{s['subject']}: {s['value']}" for s in scores])
            await message.answer(
                f"Баллы студента {student_id}:\n{text}",
                reply_markup=main_kb)


    await state.clear()
