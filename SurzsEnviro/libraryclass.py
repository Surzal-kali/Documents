import shutil
import os 

class Librarian():
    #ok step one, enumerate library. step two, index directories sith key:pair for variable matching. 
    def __init__(self, library_path):
        self.library_path = library_path
        self.library_index = {}
        self.build_library_index()
 #TODO:this needs to be a nested index maybe? like library_index[filename] = content, then we can do content searching and retrieval by filename, and maybe even metadata like tags or categories if we want to get fancy.
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
    #TODO:this parts fucked. we need to return *snippets* of the keymatched content, not whole books
    
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