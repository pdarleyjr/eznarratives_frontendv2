import reflex as rx
from app.states.chat_state import ChatState


def card(
    icon: str,
    title: str,
    description: str,
    icon_color_class: str,
) -> rx.Component:
    """A card component for preset chat prompts."""
    return rx.el.button(
        rx.el.div(
            rx.icon(
                tag=icon,
                size=16,
                class_name=f"{icon_color_class}",
            ),
            rx.el.p(
                title,
                class_name="font-medium text-gray-800 dark:text-gray-200 text-base",
            ),
            class_name="flex flex-row gap-2 items-center",
        ),
        rx.el.p(
            description,
            class_name="text-gray-600 dark:text-gray-400 text-sm font-medium",
        ),
        on_click=lambda: ChatState.send_preset_message(
            description
        ),
        type="button",
        class_name="flex flex-col gap-1 border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 hover:bg-gray-100 dark:hover:bg-gray-700 shadow-sm px-4 py-3 rounded-xl text-start transition-colors flex-1 min-h-[44px] focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-1 dark:focus:ring-offset-gray-900 transform active:scale-[0.98]",
    )


def preset_cards() -> rx.Component:
    """Displays preset chat prompt cards."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "bot",
                    size=24,
                    class_name="stroke-gray-800 dark:stroke-gray-200",
                ),
                class_name="rounded-full bg-gray-200 dark:bg-gray-700 p-2 size-10 inline-flex items-center justify-center",
            ),
            rx.el.p(
                "How can I help you today?",
                class_name="text-2xl md:text-xl font-medium text-gray-800 dark:text-gray-200",
            ),
            class_name="text-black dark:text-white flex flex-row gap-4 items-center",
        ),
        rx.el.div(
            card(
                "message-square",
                "Ask a question",
                "What is the capital of France?",
                "stroke-green-500",
            ),
            card(
                "calculator",
                "Solve a math problem",
                "What is the square root of 144?",
                "stroke-rose-500",
            ),
            card(
                "globe",
                "Get a fun fact",
                "Tell me an interesting fact about dolphins.",
                "stroke-blue-500",
            ),
            card(
                "book",
                "Recommend a book",
                "What's a good mystery novel for beginners?",
                "stroke-amber-500",
            ),
            class_name="gap-4 grid grid-cols-1 lg:grid-cols-2 w-full max-w-3xl",
        ),
        class_name="absolute inset-0 flex flex-col justify-center items-center gap-8 p-4 sm:p-6 lg:p-8",
    )