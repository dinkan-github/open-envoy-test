# Import the required modules
import random
import string


# Define a function to generate a random password
def generate_password(length):
    """
    Generates a random password of the specified length.
    The password will contain lowercase letters and digits.
    """

    # Use the string module to create a string of all lowercase letters and digits
    chars = string.ascii_lowercase + string.digits

    # Use the random module to shuffle the characters
    password = ''.join(random.sample(chars, length))

    return password


# Prompt the user to enter the desired password length
length = int(input("Enter the desired password length: "))

# Generate the password and print it to the screen
password = generate_password(length)
print("Your new password is: " + password)

# Save the password to a file
with open("password.txt", "w") as f:
    f.write(password)

# Print a message indicating that the password has been saved to a file
print("Password saved to 'password.txt'")

# Open the file in read-only mode
with open("password.txt", "r") as f:
    # Read the contents of the file
    contents = f.read()

    # Print the contents of the file
    print("File contents: " + contents)