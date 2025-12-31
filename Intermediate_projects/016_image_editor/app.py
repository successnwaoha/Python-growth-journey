import argparse
import os
from image_ops import open_image, save_image, grayscale_image, blur_image, resize_image

def main():
    # 1. Setup the Argument Parser
    parser = argparse.ArgumentParser(description="A simple Python Image Editor")
    
    # 2. Define inputs
    parser.add_argument("--input", required=True, help="Path to input image or folder")
    parser.add_argument("--output", required=True, help="Path to save the result")
    parser.add_argument("--filter", choices=['gray', 'blur'], help="Apply a filter")
    parser.add_argument("--resize", nargs=2, type=int, metavar=('WIDTH', 'HEIGHT'), help="Resize image")

    args = parser.parse_args()

    # 3. Logic to handle a single file
    if os.path.isfile(args.input):
        process_single_file(args.input, args.output, args)
    
    elif os.path.isdir(args.input):
        #Loop through every file in the folder using get_all_images
        from image_ops import get_all_images
        image_files = get_all_images(args.input)
        for img_file in image_files:
            in_path = os.path.join(args.input, img_file)
            out_path = os.path.join(args.output, img_file)
            process_single_file(in_path, out_path, args)
    else:
        print("Error: Input file not found.")

def process_single_file(in_path, out_path, args):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    
    img = open_image(in_path)
    print(f"Processing: {in_path}...")

    # Apply operations based on user flags
    if args.filter == 'gray':
        img = grayscale_image(img)
    elif args.filter == 'blur':
        img = blur_image(img)

    if args.resize:
        img = resize_image(img, args.resize[0], args.resize[1])

    # Save the result
    save_image(img, out_path)
    print(f"Saved to: {out_path}")

# This boilerplate ensures the code only runs if the file is executed directly
if __name__ == "__main__":
    main()