from telegram import (
    Update,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackContext,
)
from database.models import User
from database.db import SessionLocal
from bot.models.marksmakes import car_brands, motorcycle_brands

# Conversation states
(
    SELECT_VEHICLE_TYPE,
    SELECT_BRAND,
    SELECT_MODEL,
    SELECT_CONDITION,
    SELECT_PRICE_RANGE,
    SELECT_YEAR_RANGE,
    SELECT_MILEAGE_RANGE,
    SELECT_CAR_COLOR,
    SELECT_CAR_CONDITION,
    SELECT_OPTIONAL_LOCATION,
    SELECT_OPTIONAL_TRANSMISSION,
    SELECT_OPTIONAL_FUEL_TYPE,
    SELECT_OPTIONAL_DRIVE_TYPE,
    SELECT_OPTIONAL_DOORS,
    SELECT_OPTIONAL_LISTING_CONDITION,
    SELECT_OPTIONAL_KEYWORDS,
    SELECT_OPTIONAL_IMAGES,
    CONFIRM,
) = range(18)

# Example brand data (replace with your own dictionaries)
# car_brands = {
#     "Toyota": ["Corolla", "Camry"],
#     "Honda": ["Civic", "Accord"],
# }
# motorcycle_brands = {
#     "Harley-Davidson": ["Street 750", "Iron 883"],
#     "Yamaha": ["YZF-R3", "MT-07"],
# }

async def handle_search_new_vehicle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Entry point for searching a new vehicle."""
    await update.message.reply_text(
        text="Let's start setting up your vehicle search preferences.\n"
             "First, what type of vehicle are you looking for?",
        reply_markup=ReplyKeyboardMarkup(
            [
                [KeyboardButton("Car"), KeyboardButton("Motorcycle")],
                [KeyboardButton("Skip")],
            ],
            one_time_keyboard=True,
            resize_keyboard=True
        )
    )

    # Initialize a preferences dict in user_data to accumulate answers
    context.user_data["preferences"] = {}
    return SELECT_VEHICLE_TYPE


async def ask_vehicle_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the response for vehicle type and moves to brand selection."""
    user_choice = update.message.text.strip()

    # Check if user wants to skip
    if user_choice.lower() == "skip":
        # If skipped, you might decide to skip the entire flow or proceed with defaults
        context.user_data["preferences"]["vehicle_type"] = None
        return await proceed_to_condition(update, context)

    context.user_data["preferences"]["vehicle_type"] = user_choice  # Car or Motorcycle

    # Ask brand next
    if user_choice.lower() == "car":
        # Present car brands
        brand_buttons = [[KeyboardButton(brand)] for brand in car_brands.keys()]
    elif user_choice.lower() == "motorcycle":
        # Present motorcycle brands
        brand_buttons = [[KeyboardButton(brand)] for brand in motorcycle_brands.keys()]
    else:
        # If user typed something else
        await update.message.reply_text(
            "I didn't recognize that choice. Please select 'Car', 'Motorcycle' or 'Skip'."
        )
        return SELECT_VEHICLE_TYPE

    brand_buttons.append([KeyboardButton("Skip")])

    await update.message.reply_text(
        "Please select a brand:",
        reply_markup=ReplyKeyboardMarkup(
            brand_buttons, one_time_keyboard=True, resize_keyboard=True
        )
    )
    return SELECT_BRAND


async def ask_brand(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the selected brand and asks for the model."""
    user_choice = update.message.text.strip()

    if user_choice.lower() == "skip":
        context.user_data["preferences"]["make"] = None
        context.user_data["preferences"]["model"] = None
        # Proceed to condition question
        return await proceed_to_condition(update, context)

    vehicle_type = context.user_data["preferences"].get("vehicle_type", "").lower()
    brand_dict = car_brands if vehicle_type == "car" else motorcycle_brands

    if user_choice not in brand_dict:
        await update.message.reply_text(
            "Invalid brand. Please pick from the displayed options or 'Skip'."
        )
        return SELECT_BRAND

    context.user_data["preferences"]["make"] = user_choice

    # Ask for model
    model_buttons = [[KeyboardButton(m)] for m in brand_dict[user_choice]]
    model_buttons.append([KeyboardButton("Skip")])
    await update.message.reply_text(
        f"Select a model for {user_choice}:",
        reply_markup=ReplyKeyboardMarkup(
            model_buttons, one_time_keyboard=True, resize_keyboard=True
        )
    )
    return SELECT_MODEL


async def ask_model(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the selected model, then proceeds to vehicle condition."""
    user_choice = update.message.text.strip()

    if user_choice.lower() == "skip":
        context.user_data["preferences"]["model"] = None
    else:
        context.user_data["preferences"]["model"] = user_choice

    # Proceed to condition question
    return await proceed_to_condition(update, context)


async def proceed_to_condition(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Do you want to see New, Old, or Both types of listings?",
        reply_markup=ReplyKeyboardMarkup(
            [
                [KeyboardButton("New"), KeyboardButton("Old")],
                [KeyboardButton("Both"), KeyboardButton("Skip")],
            ],
            one_time_keyboard=True,
            resize_keyboard=True
        )
    )
    return SELECT_CONDITION


async def ask_condition(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_choice = update.message.text.strip()

    if user_choice.lower() == "skip":
        context.user_data["preferences"]["condition"] = None
    else:
        context.user_data["preferences"]["condition"] = user_choice

    # Proceed to vehicle details: price, year, mileage
    await update.message.reply_text("What is your price range? Example: `1000 - 5000` or `Skip`")
    return SELECT_PRICE_RANGE


async def ask_price_range(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_choice = update.message.text.strip()

    if user_choice.lower() == "skip":
        context.user_data["preferences"]["price_range"] = None
    else:
        # Remove any $ and extra spaces
        price_range = user_choice.replace("$", "").replace(" ", "")
        context.user_data["preferences"]["price_range"] = price_range

    await update.message.reply_text("What is your preferred year range? Example: `2000 - 2020` or `Skip`")
    return SELECT_YEAR_RANGE


async def ask_year_range(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_choice = update.message.text.strip()

    if user_choice.lower() == "skip":
        context.user_data["preferences"]["year_range"] = None
    else:
        context.user_data["preferences"]["year_range"] = user_choice.replace(" ", "")

    await update.message.reply_text("What is your preferred mileage range? Example: `0 - 50000` or `Skip`")
    return SELECT_MILEAGE_RANGE


async def ask_mileage_range(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_choice = update.message.text.strip()

    if user_choice.lower() == "skip":
        context.user_data["preferences"]["mileage_range"] = None
    else:
        context.user_data["preferences"]["mileage_range"] = user_choice.replace(" ", "")

    # Next: If vehicle_type is 'Car', ask car-specific details; else go to confirmation
    vehicle_type = context.user_data["preferences"].get("vehicle_type", "").lower()
    if vehicle_type == "car":
        await update.message.reply_text(
            "What color of car do you prefer? (e.g., Red, Black, White) or Skip"
        )
        return SELECT_CAR_COLOR
    else:
        # Motorcycle chosen, skip car-specific steps
        return await confirm_preferences(update, context)

async def ask_car_color(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_choice = update.message.text.strip()

    if user_choice.lower() == "skip":
        context.user_data["preferences"]["color"] = None
    else:
        context.user_data["preferences"]["color"] = user_choice

    await update.message.reply_text(
        "Car condition? (New, Used, Certified) or Skip",
        reply_markup=ReplyKeyboardMarkup(
            [
                [KeyboardButton("New"), KeyboardButton("Used"), KeyboardButton("Certified")],
                [KeyboardButton("Skip")],
            ],
            resize_keyboard=True,
            one_time_keyboard=True,
        )
    )
    return SELECT_CAR_CONDITION


async def ask_car_condition(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_choice = update.message.text.strip()

    if user_choice.lower() == "skip":
        context.user_data["preferences"]["car_condition"] = None
    else:
        context.user_data["preferences"]["car_condition"] = user_choice

    # Proceed with optional details
    await update.message.reply_text("Any preferred location? (e.g., 'New York') or Skip")
    return SELECT_OPTIONAL_LOCATION


async def ask_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_choice = update.message.text.strip()

    if user_choice.lower() == "skip":
        context.user_data["preferences"]["location"] = None
    else:
        context.user_data["preferences"]["location"] = user_choice

    await update.message.reply_text(
        "Preferred transmission type? (Automatic, Manual) or Skip",
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton("Automatic"), KeyboardButton("Manual")], [KeyboardButton("Skip")]],
            one_time_keyboard=True,
            resize_keyboard=True
        )
    )
    return SELECT_OPTIONAL_TRANSMISSION


async def ask_transmission(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_choice = update.message.text.strip()

    if user_choice.lower() == "skip":
        context.user_data["preferences"]["transmission"] = None
    else:
        context.user_data["preferences"]["transmission"] = user_choice

    await update.message.reply_text(
        "Preferred fuel type? (Gas, Diesel, Electric, Hybrid) or Skip",
        reply_markup=ReplyKeyboardMarkup(
            [
                [KeyboardButton("Gas"), KeyboardButton("Diesel")],
                [KeyboardButton("Electric"), KeyboardButton("Hybrid")],
                [KeyboardButton("Skip")]
            ],
            one_time_keyboard=True,
            resize_keyboard=True
        )
    )
    return SELECT_OPTIONAL_FUEL_TYPE


async def ask_fuel_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_choice = update.message.text.strip()

    if user_choice.lower() == "skip":
        context.user_data["preferences"]["fuel_type"] = None
    else:
        context.user_data["preferences"]["fuel_type"] = user_choice

    await update.message.reply_text(
        "Preferred drive type? (FWD, RWD, AWD) or Skip",
        reply_markup=ReplyKeyboardMarkup(
            [
                [KeyboardButton("FWD"), KeyboardButton("RWD"), KeyboardButton("AWD")],
                [KeyboardButton("Skip")]
            ],
            one_time_keyboard=True,
            resize_keyboard=True
        )
    )
    return SELECT_OPTIONAL_DRIVE_TYPE


async def ask_drive_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_choice = update.message.text.strip()

    if user_choice.lower() == "skip":
        context.user_data["preferences"]["drive_type"] = None
    else:
        context.user_data["preferences"]["drive_type"] = user_choice

    await update.message.reply_text("How many doors do you prefer? (2, 4, 6) or Skip")
    return SELECT_OPTIONAL_DOORS


async def ask_doors(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_choice = update.message.text.strip()

    if user_choice.lower() == "skip":
        context.user_data["preferences"]["doors"] = None
    else:
        # Convert to integer if possible
        try:
            context.user_data["preferences"]["doors"] = int(user_choice)
        except ValueError:
            context.user_data["preferences"]["doors"] = user_choice  # fallback as string

    await update.message.reply_text(
        "Do you want 'Certified' listings or 'Not Certified' or Skip?",
        reply_markup=ReplyKeyboardMarkup(
            [
                [KeyboardButton("Certified"), KeyboardButton("Not Certified")],
                [KeyboardButton("Skip")]
            ],
            one_time_keyboard=True,
            resize_keyboard=True
        )
    )
    return SELECT_OPTIONAL_LISTING_CONDITION


async def ask_listing_condition(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_choice = update.message.text.strip()

    if user_choice.lower() == "skip":
        context.user_data["preferences"]["listing_condition"] = None
    else:
        context.user_data["preferences"]["listing_condition"] = user_choice

    await update.message.reply_text("Any specific keywords? (e.g., 'Leather seats, Sunroof') or type Skip")
    return SELECT_OPTIONAL_KEYWORDS


async def ask_keywords(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_choice = update.message.text.strip()

    if user_choice.lower() == "skip":
        context.user_data["preferences"]["keywords"] = None
    else:
        # Split by comma to get list
        keywords = [kw.strip() for kw in user_choice.split(",")]
        context.user_data["preferences"]["keywords"] = keywords

    await update.message.reply_text(
        "Do you require listings with images only?\nChoose 'Yes' or 'No' or 'Skip'",
        reply_markup=ReplyKeyboardMarkup(
            [
                [KeyboardButton("Yes"), KeyboardButton("No")],
                [KeyboardButton("Skip")]
            ],
            one_time_keyboard=True,
            resize_keyboard=True
        )
    )
    return SELECT_OPTIONAL_IMAGES


async def ask_has_images(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_choice = update.message.text.strip().lower()

    if user_choice == "skip":
        context.user_data["preferences"]["has_images"] = None
    elif user_choice == "yes":
        context.user_data["preferences"]["has_images"] = True
    elif user_choice == "no":
        context.user_data["preferences"]["has_images"] = False
    else:
        # If an invalid entry
        await update.message.reply_text(
            "Please select 'Yes', 'No', or 'Skip'."
        )
        return SELECT_OPTIONAL_IMAGES

    # Finally, confirm preferences
    return await confirm_preferences(update, context)


import json

async def confirm_preferences(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Final step: show user the gathered preferences and save to DB."""
    prefs = context.user_data.get("preferences", {})

    # Build a pretty JSON string for display
    prefs_json_str = json.dumps(prefs, indent=4)

    await update.message.reply_text(
        text=f"Here are your current preferences:\n\n{prefs_json_str}\n\nSaving to database..."
    )

    # ==== Save to the database ====
    user_id = update.effective_user.id  # or get from context / your logic
    with SessionLocal() as session:
        existing_user = session.query(User).filter(User.id == user_id).first()
        if existing_user:
            existing_user.preferences = prefs  # store as a dictionary; many ORMs handle JSON automatically
            session.commit()
            await update.message.reply_text("Preferences saved successfully!")
        else:
            await update.message.reply_text(
                "User not found in the database. Could not save preferences."
            )

    # End the conversation
    return ConversationHandler.END


# search_vehicle_conv_handler = ConversationHandler(
#     entry_points=[CommandHandler("search", handle_search_new_vehicle)],
#     states={
#         SELECT_VEHICLE_TYPE: [MessageHandler(Filters.text & ~Filters.command, ask_vehicle_type)],
#         SELECT_BRAND: [MessageHandler(Filters.text & ~Filters.command, ask_brand)],
#         SELECT_MODEL: [MessageHandler(Filters.text & ~Filters.command, ask_model)],
#         SELECT_CONDITION: [MessageHandler(Filters.text & ~Filters.command, ask_condition)],
#         SELECT_PRICE_RANGE: [MessageHandler(Filters.text & ~Filters.command, ask_price_range)],
#         SELECT_YEAR_RANGE: [MessageHandler(Filters.text & ~Filters.command, ask_year_range)],
#         SELECT_MILEAGE_RANGE: [MessageHandler(Filters.text & ~Filters.command, ask_mileage_range)],
#         SELECT_CAR_COLOR: [MessageHandler(Filters.text & ~Filters.command, ask_car_color)],
#         SELECT_CAR_CONDITION: [MessageHandler(Filters.text & ~Filters.command, ask_car_condition)],
#         SELECT_OPTIONAL_LOCATION: [MessageHandler(Filters.text & ~Filters.command, ask_location)],
#         SELECT_OPTIONAL_TRANSMISSION: [MessageHandler(Filters.text & ~Filters.command, ask_transmission)],
#         SELECT_OPTIONAL_FUEL_TYPE: [MessageHandler(Filters.text & ~Filters.command, ask_fuel_type)],
#         SELECT_OPTIONAL_DRIVE_TYPE: [MessageHandler(Filters.text & ~Filters.command, ask_drive_type)],
#         SELECT_OPTIONAL_DOORS: [MessageHandler(Filters.text & ~Filters.command, ask_doors)],
#         SELECT_OPTIONAL_LISTING_CONDITION: [MessageHandler(Filters.text & ~Filters.command, ask_listing_condition)],
#         SELECT_OPTIONAL_KEYWORDS: [MessageHandler(Filters.text & ~Filters.command, ask_keywords)],
#         SELECT_OPTIONAL_IMAGES: [MessageHandler(Filters.text & ~Filters.command, ask_has_images)],
#         CONFIRM: [MessageHandler(Filters.text & ~Filters.command, confirm_preferences)],
#     },
#     fallbacks=[],
# )
