# BY ROBIN LEMAN, robin.leman@mail.mcgill.ca

import requests
import hashlib
import time

################################################# HELPERS

def get_hash(url):
    """ str -> str
    Get hashcode from URL
    """
    response = requests.get(url)
    return response.text

def int_to_7char_str(i):
    """ int -> str
    Builds a 7 characters string from an int
    """
    #the pins always have 7 digits
    pin = str(i)
    l = len(pin)
    if (l < 7):
        zeros = ""
        for j in range(7-l):
            zeros += "0"
            pin = zeros + pin
    return pin

# just for fun, ~ 10s
def brute_force(hash_md5):
    """str -> int
    return PIN by brute force
    """
    for i in range(10**7):
        pin = int_to_7char_str(i)  
        if (encode_hash(i) == hash_md5):
            return i
    return -1

def build_hash_dictionary(hash_dic):
    """ dic -> void
    builds a dictionary storing all the 10**7 7 digits pin by hash code
    """
    for i in range(10**7):
        pin = int_to_7char_str(i)
        hash_code = encode_hash(pin)
        hash_dic[hash_code] = pin

def encode_hash(pin):
    """ str -> str
    encrypts a PIN with md5, for testing purposes
    """
    return hashlib.md5(pin.encode()).hexdigest()

def post_pin(url, pin):
    """ str, str -> str
    posts the answer
    """
    response = requests.post(url = url, data = pin)
    return response.text

def create_request(url, hash_dic):
    """ str -> void
    Gets the hashcode and posts the pin
    """
    begin = time.time()
    
    hash_code = get_hash(url)
    pin = hash_dic[hash_code.strip()]
    
    end = time.time()
    
    print("time : " + str(round(end-begin, 2)) + "s")
    print(str(hash_code) + " : " + str(pin))

    print(url + hash_code)
    r = post_pin((url + hash_code), str(pin))

    print(r)

########################################################### MAIN

def main():
    hash_dic = {}
    build_hash_dictionary(hash_dic)
    create_request("https://cracking-challenge.now.sh/", hash_dic)

main()
