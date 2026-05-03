from src.Image import Image


def main():
    img = Image("test/input/test.jpg")
    print(img.get_date())
    output = img.copy_image("test/output/test.jpg")
    output.change_date("2018:04:09 18:46:35")
    print(output.get_date())


if __name__ == "__main__":
    main()
