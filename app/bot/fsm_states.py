from aiogram.fsm.state import State, StatesGroup

class RegistrationStates(StatesGroup):
    waiting_first_name = State()
    waiting_last_name = State()

class ScoreStates(StatesGroup):
    waiting_subject = State()
    waiting_score = State()
    waiting_score_value = State()
    view_scores = State()


