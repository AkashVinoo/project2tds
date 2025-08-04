def main():
    user_input = input("Enter numbers separated by spaces: ")
    # Replace spaces with +
    expr = user_input.replace(' ', '+')
    try:
        result = eval(expr)
        print(f"Sum: {result}")
    except Exception as e:
        print(f"Error evaluating expression: {e}")

if __name__ == "__main__":
    main() 