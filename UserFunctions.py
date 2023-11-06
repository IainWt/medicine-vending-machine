import openai
import csv

from Medicine_Inventory_Management_System import Inventory

inventory = Inventory()

# ------------------- OPENAI API INTERACTION -----------------

key = "ADD YOUR OPENAI API KEY"

# OpenAI completion text response
def get_openai_completion(instruction):
    openai.api_key = key
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=instruction,
    max_tokens=100,
    temperature=0
    )

    return response["choices"][0]["text"]

def get_image(instruction):
    openai.api_key = key
    image = openai.Image.create(
    prompt=instruction,
    n=1,
    size="512x512"
    )

    return image["data"][0]["url"]


# --------------- PRODUCT FUNCTIONS ------------------

# Get text explanation of given pharmaceutical product
def explain_product(product_name):
    instruction = f"Explain this pharmaceutical product: {product_name}"
    return get_openai_completion(instruction)

# Get image of item
def get_product_image(product_name):
    return get_image(product_name)

# Get translation into given language
def get_translation(language, text):
    instruction = f"Translate this into {language}: {text}"
    return get_openai_completion(instruction)


def buy_stock(product_name, quantity):
    product_id = inventory.get_product_id(product_name)
    inventory.buying_stock(product_id, quantity)

def refill_stock(product_name, quantity):
    product_id = inventory.get_product_id(product_name)
    inventory.refill_stock(product_id, quantity)

def check_stock(product_name):
    product_id = inventory.get_product_id(product_name)
    inventory.check_stock(product_id)




def create_sold_data_file():
    inventory_data_filepath = "/path/to/inventory_data/"
    filename = inventory_data_filepath + "sold_data.csv"
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID", "number_sold"])
        for key, value in inventory.get_sold_data().items():
            writer.writerow((key, value))


def get_intention(text):
    instruction = "Summarize the intention of the following text in one word which should be one of these words: 'explain, show, translate, buy'. The text is: " + text
    return get_openai_completion(instruction)

def get_number_and_product(text):
    instruction = "Tell me the item this person wants to buy and how many they want to buy, replying with only the number as a numeral and the name of the item in the form 'numeral item': " + text
    return get_openai_completion(instruction)



# --------------------- USER INPUT MANAGEMENT ----------------
def run_program():

    request = input("\nWhat do you want to do? ")
    request_word = get_intention(request).strip().lower()
    request_words = request.split(" ")

    if request_words[0] == "explain":
        response = explain_product(request_words[1])
        print(response)

    elif request_words[0] == "show":
        response = get_product_image(request_words[1])
        print("Follow this link:\n", response)

    elif request_words[0] == "translate":
        language = request_words[1]
        text = " ".join(request_words[2:])
        print(get_translation(language, text))

    elif request_words[0] == "buy" or request_word == "buy":
        request = get_number_and_product(request)
        request_words = request.split(" ")
        quantity = int(request_words[0])
        product_name = " ".join(request_words[1:]).title()
        buy_stock(product_name, quantity)

    elif request_words[0] == "refill":
        product_name = request_words[1].title()
        refill_stock(product_name)

    elif request_words[0] == "set":
        email_address = request_words[1]
        inventory.set_email_address(email_address)


if __name__ == "__main__":
    for i in range(5):
        run_program()
    create_sold_data_file()


