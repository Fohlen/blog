# pip install google-genai

import os
from google import genai
from google.genai import types

def generate(image_path):
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    # 1. Read the image file as bytes
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    model = "gemini-flash-lite-latest"
    
    contents = [
        types.Content(
            role="user",
            parts=[
                # 2. Add the image part using from_bytes
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type="image/jpeg" # Change to image/png if using a PNG
                ),
                # 3. Add the text prompt part
                types.Part.from_text(text="""Please extract the titles of books found in this image. Specify the language in three letter code MARC21 format. Additionally list all the authors found on the image for every book"""),
            ],
        ),
    ]

    generate_content_config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=genai.types.Schema(
            type = genai.types.Type.OBJECT,
            required = ["books"],
            properties = {
                "books": genai.types.Schema(
                    type = genai.types.Type.ARRAY,
                    items = genai.types.Schema(
                        type = genai.types.Type.OBJECT,
                        required = ["title", "language"],
                        properties = {
                            "title": genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                            "language": genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                            "authors": genai.types.Schema(
                                type = genai.types.Type.ARRAY,
                                items = genai.types.Schema(
                                    type = genai.types.Type.STRING,
                                ),
                            ),
                        },
                    ),
                ),
            },
        ),
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")

if __name__ == "__main__":
    generate("example_bookshelf.png")
