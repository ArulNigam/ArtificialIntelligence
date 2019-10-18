# Name: Arul Nigam
# Period: 3

import pickle

def is_adjacent(w1, w2):
   return sum(w1[i] != w2[i] for i in range(6)) == 1

def generate_adjacents(current, word_list):
   adj_list = set()
   for word in word_list:
      if(is_adjacent(current, word)):
         adj_list.add(word)
   return adj_list

def main():
   # fill the word_list
   word_list = []
   file = open("words.txt", "r")
   for word in file.readlines():
      word_list.append(word.rstrip('\n'))
   file.close()
   word_dict = {}
   for word in word_list:
      word_dict[word] = generate_adjacents(word, word_list)

   # Save the pickle file
   with open("Nigam_A_Lab3.pkl", "wb") as outfile:
      pickle.dump(word_dict, outfile, protocol = pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
   main()
