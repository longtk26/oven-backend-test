from django.test import TestCase
from .hashmap import HashMap, Node


class TestHashMap(TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.hashmap = HashMap()
    
    def test_initialization(self):
        """Test HashMap initialization with default and custom capacity."""
        # Default capacity
        hm = HashMap()
        self.assertEqual(hm.capacity, 16)
        self.assertEqual(hm.size, 0)
        self.assertEqual(len(hm.buckets), 16)
        
        # Custom capacity
        hm_custom = HashMap(32)
        self.assertEqual(hm_custom.capacity, 32)
        self.assertEqual(len(hm_custom.buckets), 32)
    
    def test_put_and_get_basic(self):
        """Test basic put and get operations."""
        self.hashmap.put("key1", "value1")
        self.assertEqual(self.hashmap.get("key1"), "value1")
        
        self.hashmap.put("key2", 42)
        self.assertEqual(self.hashmap.get("key2"), 42)
        
        self.hashmap.put(123, "numeric_key")
        self.assertEqual(self.hashmap.get(123), "numeric_key")
    
    def test_put_update_existing_key(self):
        """Test updating value for existing key."""
        self.hashmap.put("key1", "original")
        self.hashmap.put("key1", "updated")
        self.assertEqual(self.hashmap.get("key1"), "updated")
        self.assertEqual(len(self.hashmap), 1)  # Size should not increase
    
    def test_get_nonexistent_key(self):
        """Test getting value for non-existent key."""
        self.assertIsNone(self.hashmap.get("nonexistent"))
        
        # Add some data and test again
        self.hashmap.put("key1", "value1")
        self.assertIsNone(self.hashmap.get("nonexistent"))
    
    def test_remove(self):
        """Test removing key-value pairs."""
        # Remove from empty map
        self.assertFalse(self.hashmap.remove("nonexistent"))
        
        # Add and remove single item
        self.hashmap.put("key1", "value1")
        self.assertTrue(self.hashmap.remove("key1"))
        self.assertIsNone(self.hashmap.get("key1"))
        self.assertEqual(len(self.hashmap), 0)
        
        # Remove non-existent key from non-empty map
        self.hashmap.put("key1", "value1")
        self.assertFalse(self.hashmap.remove("nonexistent"))
        self.assertEqual(len(self.hashmap), 1)
    
    def test_contains(self):
        """Test contains method."""
        self.assertFalse(self.hashmap.contains("key1"))
        
        self.hashmap.put("key1", "value1")
        self.assertTrue(self.hashmap.contains("key1"))
        
        self.hashmap.remove("key1")
        self.assertFalse(self.hashmap.contains("key1"))
    
    def test_collision_handling(self):
        """Test collision handling with chaining."""
        # Create a small capacity map to force collisions
        small_map = HashMap(2)
        
        # Add multiple items that should collide
        small_map.put("a", 1)
        small_map.put("b", 2)
        small_map.put("c", 3)
        small_map.put("d", 4)
        
        # All items should be retrievable
        self.assertEqual(small_map.get("a"), 1)
        self.assertEqual(small_map.get("b"), 2)
        self.assertEqual(small_map.get("c"), 3)
        self.assertEqual(small_map.get("d"), 4)
        self.assertEqual(len(small_map), 4)
    
    def test_resize(self):
        """Test automatic resizing when load factor is exceeded."""
        # Create small map to trigger resize quickly
        small_map = HashMap(4)  # capacity 4, load factor 0.75, so resize when adding 4th item
        original_capacity = small_map.capacity
        
        # Add items to trigger resize
        small_map.put("key1", "value1")
        small_map.put("key2", "value2")
        small_map.put("key3", "value3")
        small_map.put("key4", "value4")  # This should trigger resize
        
        # Capacity should have doubled
        self.assertEqual(small_map.capacity, original_capacity * 2)
        
        # All items should still be accessible
        self.assertEqual(small_map.get("key1"), "value1")
        self.assertEqual(small_map.get("key2"), "value2")
        self.assertEqual(small_map.get("key3"), "value3")
        self.assertEqual(small_map.get("key4"), "value4")
    
    def test_keys(self):
        """Test keys method."""
        self.assertEqual(self.hashmap.keys(), [])
        
        self.hashmap.put("key1", "value1")
        self.hashmap.put("key2", "value2")
        keys = self.hashmap.keys()
        self.assertEqual(len(keys), 2)
        self.assertIn("key1", keys)
        self.assertIn("key2", keys)
    
    def test_values(self):
        """Test values method."""
        self.assertEqual(self.hashmap.values(), [])
        
        self.hashmap.put("key1", "value1")
        self.hashmap.put("key2", "value2")
        values = self.hashmap.values()
        self.assertEqual(len(values), 2)
        self.assertIn("value1", values)
        self.assertIn("value2", values)
    
    def test_items(self):
        """Test items method."""
        self.assertEqual(self.hashmap.items(), [])
        
        self.hashmap.put("key1", "value1")
        self.hashmap.put("key2", "value2")
        items = self.hashmap.items()
        self.assertEqual(len(items), 2)
        self.assertIn(("key1", "value1"), items)
        self.assertIn(("key2", "value2"), items)
    
    def test_len(self):
        """Test __len__ method."""
        self.assertEqual(len(self.hashmap), 0)
        
        self.hashmap.put("key1", "value1")
        self.assertEqual(len(self.hashmap), 1)
        
        self.hashmap.put("key2", "value2")
        self.assertEqual(len(self.hashmap), 2)
        
        self.hashmap.remove("key1")
        self.assertEqual(len(self.hashmap), 1)
    
    def test_str(self):
        """Test __str__ method."""
        self.assertEqual(str(self.hashmap), "{}")
        
        self.hashmap.put("key1", "value1")
        self.assertIn("key1: value1", str(self.hashmap))
        
        self.hashmap.put("key2", "value2")
        str_repr = str(self.hashmap)
        self.assertIn("key1: value1", str_repr)
        self.assertIn("key2: value2", str_repr)
    
    def test_none_values(self):
        """Test handling of None values."""
        self.hashmap.put("key1", None)
        self.assertIsNone(self.hashmap.get("key1"))
        self.assertTrue(self.hashmap.contains("key1"))  # Key exists even with None value
        
        # Verify we can distinguish between None value and missing key
        self.assertFalse(self.hashmap.contains("nonexistent_key"))

    def test_remove_from_chain(self):
        """Test removing items from collision chains."""
        # Force collisions with small capacity
        small_map = HashMap(2)
        
        # Add items that will collide
        small_map.put("a", 1)
        small_map.put("b", 2)
        small_map.put("c", 3)
        
        # Remove middle item from chain
        self.assertTrue(small_map.remove("b"))
        self.assertIsNone(small_map.get("b"))
        self.assertEqual(small_map.get("a"), 1)
        self.assertEqual(small_map.get("c"), 3)
        
        # Remove first item from chain
        self.assertTrue(small_map.remove("a"))
        self.assertIsNone(small_map.get("a"))
        self.assertEqual(small_map.get("c"), 3)


class TestNode(TestCase):
    """Test the Node class."""
    
    def test_node_creation(self):
        """Test Node initialization."""
        node = Node("key", "value")
        self.assertEqual(node.key, "key")
        self.assertEqual(node.value, "value")
        self.assertIsNone(node.next)
