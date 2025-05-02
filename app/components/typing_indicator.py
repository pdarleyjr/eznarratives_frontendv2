import reflex as rx


def typing_indicator() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            class_name="size-1.5 bg-gray-500 dark:bg-gray-400 rounded-full animate-pulse"
        ),
        rx.el.div(
            class_name="size-1.5 bg-gray-500 dark:bg-gray-400 rounded-full animate-pulse animation-delay-200"
        ),
        rx.el.div(
            class_name="size-1.5 bg-gray-500 dark:bg-gray-400 rounded-full animate-pulse animation-delay-400"
        ),
        class_name="flex gap-1 justify-center items-center",
    )