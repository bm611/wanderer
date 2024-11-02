import reflex as rx
from .components import hero
from .components import trip
from app.state import State


@rx.page(route="/", title="Wanderer")
def index() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        hero.hero_section(),
        class_name="w-full",
        size="4",
    )


@rx.page(route="/trip", title="Trip Details")
def trip_page() -> rx.Component:
    return rx.container(
        rx.link(
            rx.heading(
                "Wanderer",
                class_name="text-5xl md:text-7xl text-slate-600 font-extrabold text-center mt-20",
            ),
            href="/",
            on_click=lambda: State.reset_vars,
        ),
        trip.trip_section(),
        class_name="w-full",
        size="4",
    )


style = {
    "font_family": "product_regular",
    "background_color": "#FFFFFF",
    "color": "black",
}


app = rx.App(
    style=style,
    stylesheets=["/fonts/font.css"],
    theme=rx.theme(
        appearance="light",
        has_background=True,
    ),
)
