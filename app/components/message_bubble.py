import reflex as rx
from app.components.typing_indicator import typing_indicator


def ai_bubble(
    message: str, is_last: bool = False
) -> rx.Component:
    """AI message bubble."""
    return rx.el.div(
        rx.el.div(
            rx.icon(
                "bot", size=16, class_name="stroke-gray-800"
            ),
            class_name="rounded-full bg-gray-200 text-gray-800 p-2 size-8 inline-flex items-center justify-center flex-shrink-0",
        ),
        rx.cond(
            message,
            rx.el.p(
                message,
                class_name="text-sm sm:text-base text-gray-800 dark:text-gray-200",
            ),
            rx.cond(is_last, typing_indicator()),
        ),
        class_name="text-base max-w-4xl flex flex-row gap-4 items-start",
    )


def user_bubble(message: str) -> rx.Component:
    """User message bubble."""
    return rx.el.div(
        rx.el.p(
            message,
            class_name="text-sm sm:text-base text-white",
        ),
        class_name="px-3 py-2 bg-primary rounded-xl w-fit self-end max-w-[90%]",
    )


def message_bubble(
    message: str, is_ai: bool = False, is_last: bool = False
) -> rx.Component:
    """Displays a single message bubble."""
    justify_class = rx.cond(
        is_ai, "justify-start", "justify-end"
    )
    return rx.el.div(
        rx.cond(
            is_ai,
            ai_bubble(message, is_last),
            user_bubble(message),
        ),
        class_name=f"w-full flex {justify_class} mx-auto max-w-3xl px-4 sm:px-6 lg:px-8",
    )