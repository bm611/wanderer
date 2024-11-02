import reflex as rx
from app.state import State


def heading():
    return (
        rx.box(
            rx.text(
                f"{State.trip_data['city']}, {State.trip_data['state']}",
                class_name="text-slate-700 font-light text-3xl md:text-5xl",
            ),
            class_name="rounded-full p-6 border-2 bg-[#a2cf6e]",
        ),
    )


def city_image():
    return (
        rx.image(
            src=State.img_url,
            width="1024px",
            height="720",
            border_radius="50px 50px",
        ),
    )


def basic_info_layout(title, data):
    return rx.box(
        rx.vstack(
            rx.text(title, class_name="text-2xl font-bold mb-4"),
            rx.text(
                data,
                class_name="text-xl font-light text-[#4CAF50]",
            ),
            class_name="flex items-left justify-around p-4",
        ),
        class_name="rounded-2xl bg-gray-100 w-auto h-auto",
    )


def basic_info():
    return (
        rx.hstack(
            basic_info_layout("Currency", State.trip_data["currency"]),
            basic_info_layout("Timezone", State.trip_data["timezone"]),
            basic_info_layout("Best Time", State.formatted_best_visit),
            basic_info_layout("Language", State.trip_data["language"]),
            class_name="mt-6",
        ),
    )


def weather_box(quarter_data: list):
    return rx.box(
        rx.vstack(
            rx.text(
                quarter_data[0],
                class_name="text-sm text-gray-600 font-medium",
            ),
            rx.text(quarter_data[1], class_name="text-xl font-light"),
            class_name="p-4",
        ),
        background_color="#F0E5FF",
        class_name="rounded-xl border border-gray-100",
    )


def weather_section():
    return rx.box(
        rx.text("Weather by Quarter", class_name="text-2xl font-bold mb-4"),
        rx.grid(
            rx.foreach(State.weather_quarterly, weather_box),
            columns="4",
            spacing="2",
            flow="row",
            class_name="w-full",
        ),
        class_name="mt-2 p-4 bg-gray-100 rounded-3xl",
    )


def display_box(data: str):
    return rx.box(
        rx.text(
            data,
            class_name="text-sm font-light",
        ),
        class_name="rounded-lg bg-white shadow-xl hover:shadow-md transition-all duration-200 px-4 py-2",
    )


# transport
def transport_box(transport_data: list):
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.match(
                    transport_data[0],
                    ("Rideshare", rx.icon("car-taxi-front", color="#2196F3")),
                    ("Public Transit", rx.icon("train-front", color="#4CAF50")),
                    ("Car Rental", rx.icon("car", color="#FF9800")),
                    ("Airport Code", rx.icon("plane", color="#9C27B0")),
                ),
                rx.text(
                    transport_data[0],
                    class_name="text-lg text-gray-800 font-semibold",
                ),
                class_name="flex items-center justify-center space-x-2 bg-white p-3 rounded-t-xl",
            ),
            rx.vstack(
                rx.grid(
                    rx.foreach(
                        transport_data[1],
                        display_box,
                    ),
                    columns="2",
                    spacing="3",
                    flow="row",
                ),
                align_items="start",
                class_name="p-4",
            ),
            class_name="",
        ),
        background_color="white",
        class_name="rounded-xl border border-gray-200 shadow-lg hover:shadow-xl transition-all duration-200",
    )


def transport_section():
    return rx.box(
        rx.text("Transportation Options", class_name="text-2xl font-bold mb-4"),
        rx.grid(
            rx.foreach(
                State.formatted_transport,
                transport_box,
            ),
            columns="2",
            spacing="4",
            class_name="w-full",
        ),
        class_name="mt-2 p-6 bg-gray-100 rounded-3xl",
    )


def place_card(title: str, items: list):
    return rx.box(
        rx.vstack(
            rx.text(title, class_name="text-lg font-medium text-gray-700 mb-2"),
            rx.grid(
                rx.foreach(
                    items,
                    lambda item: rx.box(
                        rx.hstack(
                            rx.icon("navigation", class_name=""),
                            rx.text(item, class_name="text-sm font-light"),
                            class_name="p-2",
                        ),
                        class_name="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200",
                    ),
                ),
                columns="1",
                spacing="3",
                class_name="w-full",
            ),
            class_name="w-full",
        ),
        class_name="p-4 bg-gray-50 rounded-xl w-full",
    )


def places_section():
    return rx.box(
        rx.text("Places to Visit", class_name="text-2xl font-bold mb-4"),
        rx.grid(
            rx.box(place_card("Top Attractions", State.things_to_do), col_span=1),
            rx.box(place_card("Hidden Gems", State.hidden_gems), col_span=1),
            columns="2",
            spacing="4",
            class_name="w-full",
        ),
        class_name="mt-2 p-4 bg-gray-100 rounded-3xl",
    )


# trip layout
def trip_section() -> rx.Component:
    return rx.container(
        rx.vstack(
            heading(),
            city_image(),
            basic_info(),
            rx.hstack(
                rx.vstack(
                    weather_section(),
                    # transport
                    transport_section(),
                    class_name="flex items-center justify-center",
                ),
                # places to see, hidden gems
                places_section(),
            ),
            # tourist traps
            # hotels, restaurants
            class_name="flex items-center justify-center",
        ),
        class_name="w-full mt-24",
    )
