from loader import bot, states

from telebot.types import Message


@bot.message_handler(state=states.prime_cost, is_positive_digit=True)
def prime_cost_handler(message: Message):
    id = message.chat.id
    prime_cost = int(message.text)

    bot.add_data(id, prime_cost=prime_cost)
    bot.send_message(
        id,
        f"Введено значение: {prime_cost}.\nСколько заплатил клиент?",
    )
    bot.set_state(id, states.choose_gross)
