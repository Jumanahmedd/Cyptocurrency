#import the hashlii library to be used in the hashing function
from hashlib import sha256

def updatehash(*args): #*arg will create a list of all the aruments passed inside the function
    hashing_text = ""; h= sha256()
    #this loops over all the data inside the list to turn the list into a string in one variable
    for arg in args:
        hashing_text += str(arg)

    #returns the hash value
    h.update(hashing_text.encode('utf-8'))
    return h.hexdigest()

#--------------------------------------Block class-------------------------------------------------
class Block():
    #initializing the class attributes
    def __init__(self,number=0,previous_hash="0"*64,data=None,nonce=0):
        self.data = data
        self.number = number
        self.previous_hash = previous_hash
        self.nonce = nonce

    #a function that takes the block's data and returns its hash by using a function called updatehash
    def hash(self):
        return updatehash(
            self.number,
            self.previous_hash,
            self.data,
            self.nonce
            )

    #a function to output the blocks data in a more organized way
    def __str__(self):
        return str("Block number: %s\nHash value: %s\nPrevious hash: %s\nData: %s\nNonce: %s\n" %(
            self.number,
            self.hash(),
            self.previous_hash,
            self.data,
            self.nonce))


#--------------------------------------Blockchain class-------------------------------------------------
class Blockchain():
    #the higher the difficulty value the harder and longer time it will take to mine a block
    difficulty = 4 #the number of 0s at the start of the hash

    def __init__(self):
        self.chain = []

    #function to append a new block to the chian list
    def add(self,block):
        self.chain.append(block)

    #function to remove a block from the chain list
    def remove(self,block):
        self.chain.remove(block)

    def mine(self,block):
        try:
            #change the previous hash value to be the block's previous hash if there was a block before this one
            block.previous_hash = self.chain[-1].hash()
        #this prevents an index error incase this is the first block and there was no block before it
        except IndexError:
            pass
        #this is an infinite loop because condition is always true, the loop will break after a block is added to the chain list
        while True:
            #if the first 4 values of the block's hash are 0s (4 since the difficulty value is 4) then the block will be added to the chain
            if block.hash()[:self.difficulty] == "0" * self.difficulty:
                self.add(block); break
            else:
                #the value of the nonce incrases by one everytime the hash value is incorrect did not have 4 0s at the beginning)
                block.nonce += 1

    #this function makes sure tha the chain is not corrupted which means that the hash value of each block matches the previous hash value in the next block
    def isValid(self):
        #a for loop to loop over each block starting from the second to see if the previous hash's is correct
        for i in range(1,len(self.chain)):
            _previous = self.chain[i].previous_hash
            _current = self.chain[i-1].hash()
            if _previous != _current or _current[:self.difficulty] != "0" * self.difficulty:
                return False

        return True
