class Node:
    """Node for chaining in case of collisions"""
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashMap:
    def __init__(self, capacity=16):
        """Initialize HashMap with given capacity"""
        self.capacity = capacity
        self.size = 0
        self.buckets = [None] * self.capacity
        self.load_factor = 0.75
    
    def _hash(self, key):
        """Generate hash for a given key"""
        # Convert key to string and compute hash
        hash_val = 0
        key_str = str(key)
        for char in key_str:
            hash_val = (hash_val * 31 + ord(char)) % self.capacity
        return hash_val
    
    def _resize(self):
        """Resize the hashmap when load factor is exceeded"""
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [None] * self.capacity
        self.size = 0
        
        # Rehash all existing elements
        for bucket in old_buckets:
            current = bucket
            while current:
                self.put(current.key, current.value)
                current = current.next
    
    def put(self, key, value):
        """Insert or update key-value pair"""
        # Check if resize is needed before adding
        if (self.size + 1) / self.capacity > self.load_factor:
            self._resize()
        
        index = self._hash(key)
        
        # If bucket is empty, create new node
        if self.buckets[index] is None:
            self.buckets[index] = Node(key, value)
            self.size += 1
            return
        
        # Check if key exists and update, otherwise add to chain
        current = self.buckets[index]
        while current:
            if current.key == key:
                current.value = value  # Update existing key
                return
            if current.next is None:
                break
            current = current.next
        
        # Add new node to end of chain
        current.next = Node(key, value)
        self.size += 1
    
    def get(self, key):
        """Retrieve value for a given key"""
        index = self._hash(key)
        current = self.buckets[index]
        
        while current:
            if current.key == key:
                return current.value
            current = current.next
        
        return None  # Key not found
    
    def remove(self, key):
        """Remove key-value pair from hashmap"""
        index = self._hash(key)
        current = self.buckets[index]
        prev = None
        
        while current:
            if current.key == key:
                if prev is None:
                    # Remove first node in chain
                    self.buckets[index] = current.next
                else:
                    # Remove node from middle/end of chain
                    prev.next = current.next
                self.size -= 1
                return True
            prev = current
            current = current.next
        
        return False  # Key not found
    
    def contains(self, key):
        """Check if key exists in hashmap"""
        index = self._hash(key)
        current = self.buckets[index]
        
        while current:
            if current.key == key:
                return True
            current = current.next
        
        return False
    
    def keys(self):
        """Return list of all keys"""
        result = []
        for bucket in self.buckets:
            current = bucket
            while current:
                result.append(current.key)
                current = current.next
        return result
    
    def values(self):
        """Return list of all values"""
        result = []
        for bucket in self.buckets:
            current = bucket
            while current:
                result.append(current.value)
                current = current.next
        return result
    
    def items(self):
        """Return list of all key-value pairs as tuples"""
        result = []
        for bucket in self.buckets:
            current = bucket
            while current:
                result.append((current.key, current.value))
                current = current.next
        return result
    
    def __len__(self):
        """Return number of key-value pairs"""
        return self.size
    
    def __str__(self):
        """String representation of hashmap"""
        items = self.items()
        return '{' + ', '.join(f'{k}: {v}' for k, v in items) + '}'
