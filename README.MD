
# 🦙 llama — Terminal Chatbot using LLaMA 3.2 90B

> Lightweight CLI assistant powered by DeepInfra's **LLaMA-3.2-90B-Vision-Instruct** model.

Ask questions in the terminal like this:

```bash
llama "What is a monad in functional programming?"
````

Or enter an interactive REPL:

```bash
llama
```

---

## 🔧 Installation

### Step 1: Clone the Repo

```bash
git clone https://github.com/notsopreety/llama.git
cd llama
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

### Step 3: Make `llama` Globally Executable

```bash
chmod +x llama.py
mv llama.py /data/data/com.termux/files/usr/bin/llama  # for Termux
# OR for Linux/macOS
sudo mv llama.py /usr/local/bin/llama
```

Now you can run it anywhere using:

```bash
llama "tell me a joke"
```

---

## 🧪 Features

| Command                  | Description                                          |
| ------------------------ | ---------------------------------------------------- |
| `llama`                  | Start interactive REPL                               |
| `llama <query>`          | Ask a one-off question                               |
| `llama clear`            | Clear current conversation (preserves system prompt) |
| `llama context <prompt>` | Set custom system prompt                             |
| `llama reset`            | Clear history and reset to default system prompt     |

---

## 💻 Termux Support

If you're using **Termux**, follow these additional steps:

```bash
pkg install git python
pip install -r requirements.txt
chmod +x llama.py
mv llama.py /data/data/com.termux/files/usr/bin/llama
```

Now use `llama` anywhere from your Termux shell!

---

## 📁 requirements.txt

```txt
requests
```

---

## 🧠 Default System Prompt

```txt
"Be a helpful assistant"
```

Use `llama context "<your custom prompt>"` to customize it.

---

## 📂 Conversation History

History is saved at:

```bash
~/.llama_conversation.json
```

You can inspect, edit, or delete it if needed.

---

## 📜 License

[LICENSE](LICENSE)

---

## 🙋‍♂️ Author

**[@notsopreety](https://github.com/notsopreety)**

---
