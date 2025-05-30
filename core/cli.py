from memory import save_memory
from injector import inject_memory
from store import load_memories
import time

def main():
    print("💡 Submind CLI – Interactive Memory Layer\n")
    
    while True:
        prompt = input("\n🗣️ Prompt (or 'exit'): ")
        if prompt.strip().lower() == 'exit':
            break

        # Inject memory
        context = inject_memory(prompt, top_k=5)
        print("\n🧠 Injected Context:")
        print(context)

        # Ask to save
        save = input("\n💾 Save this prompt as memory? (y/n): ").strip().lower()
        if save == 'y':
            tags = input("🏷️  Tags (comma-separated): ").strip()
            tag_list = [t.strip() for t in tags.split(",") if t.strip()]
            save_memory(prompt, tags=tag_list)
            print("✅ Memory saved.")

        # Small delay to make UX cleaner
        time.sleep(0.5)

if __name__ == "__main__":
    main()
