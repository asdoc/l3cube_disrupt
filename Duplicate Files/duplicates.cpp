#include <dirent.h>
#include <iostream>
#include <fstream>
#include <cstring>
#include <sys/types.h>
#include <map>
#include <set>
using namespace std;

#define MAXFILES 1000
#define MAXLEN 256

ofstream files_list;
char start_path[MAXLEN];

map<string, set<string> > count_map; // Maps filename -> paths where file with same name exists

void search(DIR* directory, char path[]) {
	struct dirent* cur_dir;
	char next_dir_path[MAXLEN];
	DIR* next_dir;
	
	while((cur_dir = readdir(directory)) != NULL) { // get next directory in directory stream
		if(cur_dir -> d_type == DT_DIR) { 
		// if directory
			if(strcmp(cur_dir -> d_name, ".") == 0 ||
			   strcmp(cur_dir -> d_name, "..") == 0) { 
				// do nothing 
			}
			else {
				// scan next directory
				strcpy(next_dir_path, path);
				strcat(next_dir_path, cur_dir -> d_name);
				strcat(next_dir_path, "/");
				next_dir = opendir(next_dir_path);
				if(next_dir != NULL) {
					search(next_dir, next_dir_path);
					closedir(next_dir);
				}
			}
		}
		else { 
		// if file
			files_list << path << cur_dir -> d_name << "\n";
			string str_filename(cur_dir->d_name);
			string str_filepath(string(path) + str_filename);
			count_map[str_filename].insert(str_filepath);
		}
	}
}

void list_duplicates() {
	cout << "\n--\nListing duplicate files.\n--\n";
	for(auto x: count_map) {
		if(x.second.size() > 1) { // if there exists more than 1 instance of the same file name
			cout << x.first << ":\n";
			for(auto y: x.second) {
				cout << "    # " << y << "\n";
			}
		}
	}
}

int main(int argc, char **argv) {
	strcpy(start_path, argv[1]);
	DIR *root;
	root = opendir(start_path);
	
	files_list.open("files_list.txt", ios::out);
	
	search(root, start_path);
	
	list_duplicates();
	
}
