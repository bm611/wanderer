import reflex as rx
from .components import hero
from .components import trip
from app.state import State


@rx.page(route="/", title="TBD")
def index() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        hero.hero_section(),
        rx.cond(
            State.is_loading,
            trip.trip_section(),
            rx.text(),
        ),
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
