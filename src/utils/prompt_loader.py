def load_prompt(file_path):
    """Helper function to load prompts from files"""
    with open(file_path, 'r') as file:
        return file.read()