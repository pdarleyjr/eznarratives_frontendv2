import reflex as rx
from app.states.chat_state import ChatState
from app.components.typing_indicator import typing_indicator


def input_area() -> rx.Component:
    """Input area for chat."""
    return rx.el.div(
        rx.el.div(
            rx.el.form(
                rx.el.textarea(
                    name="message",
                    placeholder="Ask me anything...",
                    enter_key_submit=True,
                    class_name="bg-transparent resize-none outline-none text-base py-2 px-3 min-h-10 text-gray-800 max-h-36 peer !overflow-y-auto w-full",
                    auto_height=True,
                    required=True,
                ),
                rx.el.div(
                    rx.cond(
                        ChatState.messages,
                        rx.el.button(
                            rx.icon("square-pen", size=16),
                            title="New chat",
                            class_name="rounded-full bg-gray-100 text-gray-600 p-2 shadow-sm size-9 inline-flex items-center justify-center hover:bg-gray-200 transition-colors border border-gray-300",
                            type="button",
                            on_click=ChatState.clear_messages,
                        ),
                    ),
                    rx.el.button(
                        rx.cond(
                            ChatState.typing,
                            rx.icon(
                                "square",
                                class_name="text-white",
                            ),
                            rx.icon(
                                "arrow-up",
                                class_name="text-white",
                            ),
                        ),
                        class_name="self-end rounded-full bg-blue-600 hover:bg-blue-700 text-white p-2 shadow-sm size-9 inline-flex items-center justify-center transition-colors",
                        type=rx.cond(
                            ChatState.typing,
                            "button",
                            "submit",
                        ),
                        disabled=False,
                        on_click=rx.cond(
                            ChatState.typing,
                            ChatState.cancel_typing,
                            rx.noop(),
                        ),
                    ),
                    class_name="flex flex-row mb-2 w-full",
                    style={
                        "justifyContent": rx.cond(
                            ChatState.messages,
                            "space-between",
                            "flex-end",
                        )
                    },
                ),
                reset_on_submit=True,
                on_submit=ChatState.send_message,
                class_name="flex flex-col gap-2",
            ),
            class_name="rounded-2xl bg-white w-full border border-gray-200 px-3 py-1 shadow-lg mx-auto z-10 focus-within:ring-2 focus-within:ring-blue-200 transition-shadow",
        ),
        class_name="px-4 sm:px-6 lg:px-8 w-full max-w-3xl mx-auto",
    )