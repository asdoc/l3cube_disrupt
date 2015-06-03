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
int files_count = 0;
map <string,int> files_map;
map <int,string> file_id_map;

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
			files_map[((string)path + (string)cur_dir -> d_name)] = files_count;
			file_id_map[files_count] = ((string)path + (string)cur_dir -> d_name);
			files_count += 1;
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
				cout << "    # " << y << " - file_id: " << files_map[y] << "\n";
			}
		}
	}
}

int main(int argc, char **argv) {
	strcpy(start_path, argv[1]);
	DIR *root;
	root = opendir(start_path);
	strcat(start_path,"/");
	
	files_list.open("files_list.txt", ios::out);
	
	search(root, start_path);
	
	list_duplicates();
	
	int file_id_to_delete = -1;
	cout<<"Enter the file ids to delete: (-1 to exit):\n";
	while(true){
		cin>>file_id_to_delete;
		if(file_id_to_delete == -1) {
			break;
		}
		remove(file_id_map[file_id_to_delete].c_str());
	}
	
}
