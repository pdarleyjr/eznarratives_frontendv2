import reflex as rx
from app.states.chat_state import ChatState


def input_area() -> rx.Component:
    """Component for the chat input area."""
    return rx.el.form(
        rx.el.div(
            rx.el.textarea(
                name="message",
                placeholder="Type your message here...",
                default_value=ChatState.current_message,
                rows=1,
                class_name="flex-1 resize-none p-3 pr-14 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 min-h-[48px] max-h-40 overflow-y-auto scrollbar-thin",
                on_change=ChatState.set_current_message,
            ),
            rx.el.button(
                rx.icon(tag="send", size=20),
                type="submit",
                is_disabled=ChatState.processing
                | (ChatState.current_message.strip() == ""),
                class_name="absolute right-2.5 bottom-2.5 p-2.5 rounded-lg text-white bg-accent hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-accent focus:ring-offset-1 dark:focus:ring-offset-gray-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-150 ease-in-out transform active:scale-95",
                aria_label="Send message",
            ),
            class_name="relative flex items-end",
        ),
        on_submit=ChatState.send_message,
        reset_on_submit=True,
        width="100%",
        padding_x="1rem",
        padding_y="0.75rem",
        class_name="bg-gray-100 dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 sticky bottom-0 pb-safe-bottom",
    )