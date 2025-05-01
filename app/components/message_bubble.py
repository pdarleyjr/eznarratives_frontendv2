import reflex as rx
from app.components.typing_indicator import typing_indicator


def ai_bubble(
    message: str, is_last: bool = False
) -> rx.Component:
    """AI message bubble."""
    return rx.el.div(
        rx.el.div(
            rx.icon("bot", size=16),
            class_name="rounded-full bg-gray-200 text-gray-800 p-2 size-8 inline-flex items-center justify-center",
        ),
        rx.cond(
            message,
            rx.el.p(
                message,
                class_name="text-sm sm:text-base text-gray-800",
            ),
            rx.cond(is_last, typing_indicator()),
        ),
        class_name="text-base max-w-4xl flex flex-row gap-4",
    )


def user_bubble(message: str) -> rx.Component:
    """User message bubble."""
    return rx.el.div(
        rx.el.p(
            message,
            class_name="text-sm sm:text-base text-white",
        ),
        class_name="px-3 py-2 bg-blue-500 rounded-xl w-fit self-end max-w-[90%]",
    )


def message_bubble(
    message: str, is_ai: bool = False, is_last: bool = False
) -> rx.Component:
    """Displays a single message bubble."""
    return rx.el.div(
        rx.cond(
            is_ai,
            ai_bubble(message, is_last),
            user_bubble(message),
        ),
        class_name="w-full flex flex-col gap-6 mx-auto max-w-3xl px-4 sm:px-6 lg:px-8",
    )