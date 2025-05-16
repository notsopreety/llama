#!/usr/bin/env python3
import os
import sys
import json
import requests

API_URL = "https://api.deepinfra.com/v1/openai/chat/completions"
CONV_FILE = os.path.expanduser("~/.llama_conversation.json")
MODEL = "meta-llama/Llama-3.2-90B-Vision-Instruct"
DEFAULT_PROMPT = "Be a helpful assistant"
MAX_TURNS = 20

def load_conversation():
    if os.path.exists(CONV_FILE):
        with open(CONV_FILE, "r") as f:
            return json.load(f)
    return new_conversation(DEFAULT_PROMPT)

def save_conversation(conv):
    msgs = conv["messages"]
    sys_msg = msgs[0]
    others = msgs[1:]
    turns = len([m for m in others if m["role"]=="user"])
    if turns > MAX_TURNS:
        drop = turns - MAX_TURNS
        new_others, cnt = [], 0
        for m in others:
            if m["role"]=="user":
                if cnt < drop:
                    cnt += 1
                    continue
                new_others.append(m)
            else:
                if cnt >= drop:
                    new_others.append(m)
        others = new_others
    conv["messages"] = [sys_msg] + others
    with open(CONV_FILE, "w") as f:
        json.dump(conv, f, indent=2)

def new_conversation(system_prompt):
    return {
        "model": MODEL,
        "messages": [{"role": "system", "content": system_prompt}],
        "stream": True,
        "stream_options": {
            "include_usage": True,
            "continuous_usage_stats": True
        }
    }

def stream_request(conv):
    headers = {
        "Accept": "text/event-stream",
        "Content-Type": "application/json",
        "X-Deepinfra-Source": "cli"
    }
    resp = requests.post(API_URL, headers=headers, json=conv, stream=True)
    assistant_msg = ""
    for line in resp.iter_lines(decode_unicode=True):
        if not line or not line.startswith("data: "):
            continue
        data = line[6:]
        if data == "[DONE]":
            break
        try:
            chunk = json.loads(data)
            delta = chunk["choices"][0]["delta"].get("content", "")
            assistant_msg += delta
            print(delta, end="", flush=True)
        except:
            continue
    print()
    return assistant_msg

def do_send(user_text, conv):
    conv["messages"].append({"role": "user", "content": user_text})
    save_conversation(conv)
    assistant_text = stream_request(conv)
    conv["messages"].append({"role": "assistant", "content": assistant_text})
    save_conversation(conv)

def repl():
    conv = load_conversation()
    print("Entering llama REPL. Type 'exit' to quit.")
    while True:
        try:
            line = input("> ").strip()
        except EOFError:
            break
        if not line:
            continue
        cmd, *rest = line.split(" ", 1)
        arg = rest[0] if rest else ""
        if cmd == "exit":
            break
        elif cmd == "clear":
            conv = new_conversation(conv["messages"][0]["content"])
            save_conversation(conv)
            print("[conversation cleared]")
        elif cmd == "context" and arg:
            conv["messages"][0]["content"] = arg
            save_conversation(conv)
            print(f"[system prompt set to: {arg}]")
        elif cmd == "reset":
            conv = new_conversation(DEFAULT_PROMPT)
            save_conversation(conv)
            print("[conversation reset to default system prompt]")
        else:
            do_send(line, conv)
    print("Goodbye.")

def main():
    conv = load_conversation()

    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        arg = " ".join(sys.argv[2:]).strip()

        if cmd == "clear":
            conv = new_conversation(conv["messages"][0]["content"])
            save_conversation(conv)
            print("[conversation cleared]")
        elif cmd == "context" and arg:
            conv["messages"][0]["content"] = arg
            save_conversation(conv)
            print(f"[system prompt set to: {arg}]")
        elif cmd == "reset":
            conv = new_conversation(DEFAULT_PROMPT)
            save_conversation(conv)
            print("[conversation reset to default system prompt]")
        else:
            do_send(" ".join(sys.argv[1:]), conv)
        sys.exit(0)
    else:
        repl()

if __name__ == "__main__":
    main()
