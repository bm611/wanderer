import reflex as rx
from app.state import State


def hero_section() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading(
                "Wanderer",
                class_name="text-5xl md:text-7xl text-slate-600 font-extrabold mx-10",
            ),
            rx.text(
                "Your AI Trip Planner. Get personalized travel recommendations, local insights, and essential information for your next adventure.",
                class_name="text-slate-600 text-xl md:text-2xl mx-10 mb-10",
            ),
            rx.hstack(
                rx.input(
                    placeholder="Enter a City name",
                    class_name="w-full h-20 md:h-28 px-10 pr-8 md:pr-16 rounded-full text-slate-600 text-xl md:text-3xl bg-transparent",
                    on_change=State.handle_city_change,
                    value=State.city_input,
                ),
                rx.button(
                    rx.icon("arrow-up"),
                    class_name="rounded-full bg-gray-700 hover:bg-black absolute right-8 top-1/2 transform -translate-y-1/2",
                    size="4",
                    type="submit",
                    on_click=[
                        State.start_generation,
                        State.generate_city_guide,
                    ],
                    loading=State.is_loading,
                    disabled=State.is_loading,
                ),
                class_name="w-full max-w-[800px] relative flex items-center px-4",
            ),
            width="100%",
            max_width="100%",
        ),
        class_name="mt-20 w-full",
    )
