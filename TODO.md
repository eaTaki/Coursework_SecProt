# TODO

- [ ] Build a binary tree like it is explain in the pdf, take into account it will contain the encrypted values

  - [ ] Generate the empty tree with all the nodes
  - [ ] Fill the tree with all the values
  - [ ] Add noise to the nodes
  - [ ] Create a function that retrieves the necessary nodes for each query

- [ ] Create a class(not necessary but I think it is easier to do it with a class) that stores ElGamal keys and is able to encrypt and decrypt
  - [ ] Make sure the properties LCH and LKH properties are met

- [ ] Find a way to encrypt every value of the tree(you will need to create the the same number of ElGamal keys as nodes and encrypt the nodes with the keys)

- [ ] Find a way to decrypt the necessary nodes
  - [ ] Find a way to decrypt the necessary nodes using functional keys(using the LCH and LKH properties)

- [ ] Replicate the results of the paper by measuring time and changing the parameters