import os
import shutil
import subprocess
import httpx

def is_binary(file_path):
    try:
        with open(file_path, 'rb') as file:
            chunk = file.read(1024)
            if b'\0' in chunk:
                return True
    except Exception:
        return True
    return False

def clone_and_read_files(repo_url):
    # Get the temporary directory from the environment variable or use a default value
    temp_dir = os.getenv('TEMP_FOLDER', 'C:/Users/ramonc/Documents/codex/marmot/temp')
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # Create a unique directory for the cloned repository
    repo_dir = os.path.join(temp_dir, 'cloned_repo')
    if os.path.exists(repo_dir):
        shutil.rmtree(repo_dir)

    # Clone the repository
    subprocess.run(['git', 'clone', repo_url, repo_dir], check=True)

    if not os.path.exists(repo_dir):
        raise FileNotFoundError(f"El directorio {repo_dir} no existe. El clon del repositorio falló.")

    # Read the text of all files
    text_content = ""
    for root, dirs, files in os.walk(repo_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if is_binary(file_path):
                continue
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    text_content += f"--- {file_path} ---\n"
                    text_content += file.read() + "\n"
            except UnicodeDecodeError:
                with open(file_path, 'r', encoding='latin-1') as file:
                    text_content += f"--- {file_path} ---\n"
                    text_content += file.read() + "\n"

    # Clean up the cloned repository
    def on_rm_error(func, path, exc_info):
        import stat
        os.chmod(path, stat.S_IWRITE)
        func(path)

    shutil.rmtree(repo_dir, onerror=on_rm_error)

    return text_content

def read_single_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as file:
            return file.read()

# Header
header = "As a senior programmer, given a project in [PROGRAMMING LANGUAGE] with [VERSION OF LIBRARIES]. How could resolve the next error [ERROR_COMPILE] to generete a success compile?\n\n"

# Example log
single_file_path = r"C:/Users/ramonc/Documents/codex/marmot/uploads/msbuild.log"
single_file_content = read_single_file(single_file_path)

# Example usage
repo_url = 'https://tfs-glo-lexisadvance.visualstudio.com/DefaultCollection/Radix.Sandbox/_git/GenAI%20Hackathon%20-%20Pipelines%20Security%20and%20PRs'
text = clone_and_read_files(repo_url)
#print(text)

prompt = (header + text + single_file_content)

try:
    from ollama import chat
    from ollama import ChatResponse

    # Ensure the model is available
    subprocess.run([r'C:\Users\ramonc\AppData\Local\Programs\Ollama\ollama.exe', 'pull', 'codellama:7b'], check=True)

    response: ChatResponse = chat(
        model='codellama:7b',
        messages=[{'role': 'user', 'content': prompt}]
    )
    print("hello", response)
    print(response['message']['content'])
    print(response.message.content)
except ModuleNotFoundError:
    print("The 'ollama' module is not installed. Please install it using 'pip install ollama'.")
except httpx.ConnectError as e:
    print(f"Connection error: {e}")
except subprocess.CalledProcessError as e:
    print(f"An error occurred while pulling the model: {e}")
except FileNotFoundError as e:
    print(f"An error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")