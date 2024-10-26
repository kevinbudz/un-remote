import os
from PIL import Image
from datetime import datetime

STATIC_GRID_WIDTH = 16  
DYNAMIC_GRID_WIDTH = 7   

def create_blank_grid(cell_size, num_rows, grid_width):
    grid_width_px = grid_width * cell_size
    grid_height_px = num_rows * cell_size
    return Image.new("RGBA", (grid_width_px, grid_height_px))

def create_blank_dynamic_sheet(width, total_height):
    return Image.new("RGBA", (width, total_height))

def place_sprite_on_grid(grid_img, sprite, grid_position, cell_size):
    x, y = grid_position
    grid_x = x * cell_size
    grid_y = y * cell_size
    grid_img.paste(sprite, (grid_x, grid_y))

def find_next_spot(filled_spots, current_row, grid_width):
    for y in range(current_row, current_row + 1):
        for x in range(grid_width):
            if (x, y) not in filled_spots:
                return (x, y)
    return None  

def is_mask_image(image):
    red_green_count = 0
    non_transparent_pixel_count = 0

    for pixel in image.getdata():
        r, g, b, a = pixel
        if a > 0:
            non_transparent_pixel_count += 1
            if (r > 150 and g < 100 and b < 100) or (g > 150 and r < 100 and b < 100):
                red_green_count += 1
    
    if non_transparent_pixel_count == 0:
        return False
    
    return red_green_count / non_transparent_pixel_count > 0.6

def process_images():
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    output_folder = f"output-{timestamp}"
    os.makedirs(output_folder, exist_ok=True)
    
    print(f"Output directory: {output_folder}")
    
    current_directory = os.getcwd()

    static_grids = {}  
    dynamic_sheets = {}  
    dynamic_sheet_heights = {}  

    for filename in sorted(os.listdir(current_directory)):
        if filename.endswith(".png"):
            with Image.open(filename) as img:
                width, height = img.size

                if width == height:  
                    if width not in static_grids:
                        static_grids[width] = {
                            "grid_img": create_blank_grid(width, 1, STATIC_GRID_WIDTH),
                            "filled_spots": set(),
                            "current_row": 0,
                            "max_rows": 1,
                        }

                    static_grid_data = static_grids[width]
                    static_filled_spots = static_grid_data["filled_spots"]

                    if len(static_filled_spots) >= STATIC_GRID_WIDTH * static_grid_data["max_rows"]:
                        static_grid_data["max_rows"] += 1
                        new_static_grid_img = create_blank_grid(width, static_grid_data["max_rows"], STATIC_GRID_WIDTH)
                        new_static_grid_img.paste(static_grid_data["grid_img"], (0, 0))  
                        static_grid_data["grid_img"] = new_static_grid_img

                    grid_position = find_next_spot(static_filled_spots, static_grid_data["current_row"], STATIC_GRID_WIDTH)
                    if grid_position is None:
                        static_grid_data["current_row"] += 1
                        grid_position = find_next_spot(static_filled_spots, static_grid_data["current_row"], STATIC_GRID_WIDTH)

                    place_sprite_on_grid(static_grid_data["grid_img"], img, grid_position, width)
                    static_filled_spots.add(grid_position)
                else:
                    if is_mask_image(img):
                        dynamic_type = "masks"
                    else:
                        aspect_ratio = width / height
                        dynamic_type = "enemies" if aspect_ratio == 7 / 1 else "skins" if aspect_ratio == 7 / 3 else None

                    if dynamic_type:
                        dynamic_key = (width, dynamic_type)

                        if dynamic_key not in dynamic_sheets:
                            dynamic_sheets[dynamic_key] = create_blank_dynamic_sheet(width, height)
                            dynamic_sheet_heights[dynamic_key] = height
                        else:
                            total_height = dynamic_sheet_heights[dynamic_key] + height
                            new_dynamic_sheet = create_blank_dynamic_sheet(width, total_height)
                            new_dynamic_sheet.paste(dynamic_sheets[dynamic_key], (0, 0))
                            dynamic_sheets[dynamic_key] = new_dynamic_sheet
                            dynamic_sheet_heights[dynamic_key] = total_height

                        sheet_y_position = dynamic_sheet_heights[dynamic_key] - height
                        dynamic_sheets[dynamic_key].paste(img, (0, sheet_y_position))

    for cell_size, static_data in static_grids.items():
        output_filename_static = os.path.join(output_folder, f"static_{cell_size}.png")
        static_data["grid_img"].save(output_filename_static)
        print(f"static_{cell_size}.png has been generated.")
    
    for (width, dynamic_type), dynamic_sheet in dynamic_sheets.items():
        output_filename_dynamic = os.path.join(output_folder, f"{dynamic_type}_{width // 7}.png")
        dynamic_sheet.save(output_filename_dynamic)
        print(f"{dynamic_type}_{width // 7}.png has been generated.")

if __name__ == "__main__":
    process_images()
