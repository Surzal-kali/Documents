import shutil
import os 

class Librarian():
    #ok step one, enumerate library. step two, index directories sith key:pair for variable matching. 
        # --- Public API ---
    # TODO: Librarian - Notes management system with features like:
    # [ ] Reindexing to detect new/removed notes
    # [ ] Organize by directory with indentation
    # [ ] Show metadata (file size, modification date, note count per folder)
    # [ ] Use consistent column alignment (filename, size, date)
    # [ ] Add a header like "Available Notes" with divider
    # [ ] Strip .md and / cleanly, capitalize/title-case folder/note names
    # [ ] Truncate long paths to avoid clutter
    # [ ] Add counters like [3/10 notes] per category
    def __init__(self, library_path):
        self.library_path = library_path
        self.library_index = {}
        self.build_library_index()

    def build_library_index(self):
        for root, dirs, files in os.walk(self.library_path):
            for file in files:
                if file.endswith(".md") or file.endswith(".txt"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r") as f:
                        content = f.read()
                    self.library_index[file] = content
                    #should return a dict
    def search_library(self, query):
        results = {}
        for file, content in self.library_index.items():
            if query.lower() in content.lower():
                results[file] = content.find(query)
        stuff=results.items()
        print(f"[+] Found {len(results)} matches for '{query}':")
        for file, index in stuff:
            snippet = self.print_snippet(file, query)
            print(f"- {file}: ...{snippet}...")
    
    def print_snippet(self, file, query, context=30):
        content = self.library_index[file]
        index = content.lower().find(query.lower())
        if index == -1:
            return None
        start = max(0, index - context)
        end = min(len(content), index + len(query) + context)
        snippet = content[start:end]
        return snippet.replace("\n", " ")
    
    def get_library_entry(self, name):
        return self.library_index.get(name, None)
    
    def print_library_index(self):
        for file in self.library_index:
            print(f"- {file}")

    def open_bookmark(self, name):
        content = self.get_library_entry(name)
        if content:
            print(f"[+] Opening bookmark '{name}':")
            print(content)
        else:
            print(f"[-] Bookmark '{name}' not found in library.")