import streamlit as st
from PIL import Image, ImageDraw
import random

# Constants
SCENE_SIZE_OPTIONS = ["Small", "Medium", "Large"]
COMPLEXITY_LEVELS = ["Low Complexity", "Medium Complexity", "High Complexity"]

# Helper Functions
def get_random_character_image():
    """Generate a random character image."""
    img = Image.new("RGBA", (30, 30), (255, 0, 0, 0))
    return img

def check_overlap(existing_positions, new_position, threshold=30):
    """Check if the new position overlaps with existing positions."""
    for position in existing_positions:
        if abs(position[0] - new_position[0]) < threshold and abs(position[1] - new_position[1]) < threshold:
            return True
    return False

def draw_box(image, position, char_size, color="red"):
    """Draw a box around a character."""
    draw = ImageDraw.Draw(image)
    top_left = position
    bottom_right = (position[0] + char_size[0], position[1] + char_size[1])
    draw.rectangle([top_left, bottom_right], outline=color)
    return image

def resize_image(image, size_factor):
    """Resize the image based on the given size factor."""
    new_size = (int(image.size[0] * size_factor), int(image.size[1] * size_factor))
    return image.resize(new_size, Image.ANTIALIAS)

def place_characters(background, artemis_path, apollo_path, num_characters):
    """Place characters on the background image."""
    bg = background.copy()
    artemis = Image.open(artemis_path)
    apollo = Image.open(apollo_path)
    placed_positions = [(50, 50), (100, 100)]
    
    bg.paste(artemis, placed_positions[0], artemis)
    bg.paste(apollo, placed_positions[1], apollo)

    for _ in range(num_characters):
        char_img = get_random_character_image()
        random_x, random_y = random.randint(0, bg.size[0] - char_img.size[0]), random.randint(0, bg.size[1] - char_img.size[1])

        while check_overlap(placed_positions, (random_x, random_y)):
            random_x, random_y = random.randint(0, bg.size[0] - char_img.size[0]), random.randint(0, bg.size[1] - char_img.size[1])

        bg.paste(char_img, (random_x, random_y), char_img)
        placed_positions.append((random_x, random_y))

    return bg, placed_positions[0], placed_positions[1], {'artemis': artemis.size, 'apollo': apollo.size}

# Streamlit UI
def main():
    st.title("Where's Artemis & Apollo? Puzzle Generator")
    st.sidebar.header("Puzzle Settings")

    scene_size = st.sidebar.selectbox("Choose the Scene Size", SCENE_SIZE_OPTIONS, index=1)
    complexity = st.sidebar.selectbox("Choose Complexity Level", COMPLEXITY_LEVELS, index=1)
    
    background_path = st.sidebar.file_uploader("Choose a background image", type=["jpg", "jpeg", "png"])
    artemis_path = st.sidebar.file_uploader("Choose an Artemis image", type=["png"])
    apollo_path = st.sidebar.file_uploader("Choose an Apollo image", type=["png"])
    
    show_box_artemis = st.sidebar.checkbox("Show box around Artemis")
    show_box_apollo = st.sidebar.checkbox("Show box around Apollo")
    
    scene_sizes = {"Small": 0.5, "Medium": 1.0, "Large": 1.5}
    complexities = {"Low Complexity": 50, "Medium Complexity": 100, "High Complexity": 150}
    
    num_characters = int(scene_sizes[scene_size] * complexities[complexity])
    st.sidebar.text(f"Number of Characters: {num_characters}")

    if st.sidebar.button("Generate Puzzle"):
        if background_path and artemis_path and apollo_path:
            background_image = Image.open(background_path)
            size_factor = {"Small": 0.5, "Medium": 1, "Large": 2}[scene_size]
            resized_background = resize_image(background_image, size_factor)
            
            result_image, artemis_position, apollo_position, char_sizes = place_characters(
                resized_background, artemis_path, apollo_path, num_characters
            )
            
            if show_box_artemis:
                result_image = draw_box(result_image, artemis_position, char_sizes['artemis'])
            if show_box_apollo:
                result_image = draw_box(result_image, apollo_position, char_sizes['apollo'], color="blue")
            
            st.image(result_image, caption="Can you find Artemis & Apollo?", use_column_width=True)
        else:
            st.warning("Please upload the background, Artemis, and Apollo images to generate the puzzle.")

if __name__ == "__main__":
    main()
