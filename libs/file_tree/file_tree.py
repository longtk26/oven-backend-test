import os
from libs.hashmap import HashMap
from typing import Dict, List, Any, Optional
import mimetypes
from apis.exceptions import BadRequestException


class FileTreeNode:
    """Node representing a file or directory in the tree structure"""
    
    def __init__(self, name: str, path: str, is_directory: bool = False, parent=None):
        self.name = name
        self.path = path
        self.is_directory = is_directory
        self.parent = parent
        self.size = 0
        self.extension = ""
        self.mime_type = ""
        self.created_at = None
        self.modified_at = None
        
        if not is_directory:
            # Extract file extension and mime type
            self.extension = os.path.splitext(name)[1].lower()
            self.mime_type, _ = mimetypes.guess_type(name)
            if self.mime_type is None:
                self.mime_type = "application/octet-stream"


class FileTreeStructure:
    """File tree structure using custom HashMap implementation"""
    
    def __init__(self, max_depth: int = 3):
        """
        Initialize file tree structure
        
        Args:
            max_depth: Maximum allowed nesting depth for folders
        """
        self.root_nodes = HashMap()  # Root level files and directories
        self.all_nodes = HashMap()   # All nodes indexed by path for quick lookup
        self.max_depth = max_depth
    
    def _get_depth(self, path: str) -> int:
        """Calculate the depth of a path (number of folder levels)"""
        return len([p for p in path.split('/') if p])
    
    def _get_parent_path(self, path: str) -> Optional[str]:
        """Get parent directory path"""
        parts = path.rstrip('/').split('/')
        if len(parts) <= 1:
            return None
        return '/'.join(parts[:-1])
    
    def _create_directory_chain(self, path: str) -> FileTreeNode:
        """
        Create directory chain if it doesn't exist
        
        Args:
            path: Directory path to create
            
        Returns:
            The created or existing directory node
        """
        if self.all_nodes.contains(path):
            return self.all_nodes.get(path)
        
        # Check depth limit
        if self._get_depth(path) > self.max_depth:
            raise BadRequestException(f"Maximum directory depth ({self.max_depth}) exceeded")
        
        parent_path = self._get_parent_path(path)
        parent_node = None
        
        if parent_path:
            parent_node = self._create_directory_chain(parent_path)
        
        # Create directory node
        dir_name = os.path.basename(path)
        dir_node = FileTreeNode(
            name=dir_name,
            path=path,
            is_directory=True,
            parent=parent_node
        )
        
        # Store in all_nodes
        self.all_nodes.put(path, dir_node)
        
        # If it's a root level directory, add to root_nodes
        if parent_path is None:
            self.root_nodes.put(dir_name, dir_node)
        
        return dir_node
    
    def add_file(self, file_path: str, file_size: int = 0, created_at=None, modified_at=None) -> FileTreeNode:
        """
        Add a file to the tree structure
        
        Args:
            file_path: Full path to the file
            file_size: Size of the file in bytes
            created_at: File creation timestamp
            modified_at: File modification timestamp
            
        Returns:
            The created file node
        """
        # Normalize path
        file_path = file_path.strip('/')
        
        # Check if file already exists
        if self.all_nodes.contains(file_path):
            existing_node = self.all_nodes.get(file_path)
            if not existing_node.is_directory:
                return existing_node
            else:
                raise BadRequestException(f"Directory already exists at path: {file_path}")
        
        # Get directory path and file name
        parent_path = self._get_parent_path(file_path)
        file_name = os.path.basename(file_path)
        
        # Create parent directories if they don't exist
        parent_node = None
        if parent_path:
            parent_node = self._create_directory_chain(parent_path)
        
        # Check depth limit for the file
        if self._get_depth(file_path) > self.max_depth:
            raise BadRequestException(f"Maximum directory depth ({self.max_depth}) exceeded")
        
        # Create file node
        file_node = FileTreeNode(
            name=file_name,
            path=file_path,
            is_directory=False,
            parent=parent_node
        )
        file_node.size = file_size
        file_node.created_at = created_at
        file_node.modified_at = modified_at
        
        # Store in all_nodes
        self.all_nodes.put(file_path, file_node)
        
        # If it's a root level file, add to root_nodes
        if parent_path is None:
            self.root_nodes.put(file_name, file_node)
        
        return file_node
    
    def set_max_depth(self, max_depth: int):
        """Set maximum allowed directory depth"""
        if max_depth < 1:
            raise ValueError("max_depth must be at least 1")
        self.max_depth = max_depth
    
    def get_node(self, path: str) -> Optional[FileTreeNode]:
        """Get a node by its path"""
        path = path.strip('/')
        return self.all_nodes.get(path)
    
    def get_children(self, directory_path: str = "") -> List[FileTreeNode]:
        """
        Get direct children of a directory
        
        Args:
            directory_path: Path to the directory (empty string for root)
            
        Returns:
            List of child nodes
        """
        directory_path = directory_path.strip('/')
        children = []
        
        if directory_path == "":
            # Return root level items
            for node in self.root_nodes.values():
                children.append(node)
        else:
            # Find children of the specified directory
            prefix = directory_path + '/'
            for path in self.all_nodes.keys():
                if path.startswith(prefix):
                    # Check if it's a direct child (no additional slashes)
                    relative_path = path[len(prefix):]
                    if '/' not in relative_path:
                        children.append(self.all_nodes.get(path))
        
        return sorted(children, key=lambda x: (not x.is_directory, x.name))
    
    def to_tree_dict(self, directory_path: str = "") -> Dict[str, Any]:
        """
        Convert the file tree to a nested dictionary structure
        
        Args:
            directory_path: Root directory path (empty for full tree)
            
        Returns:
            Tree structure as nested dictionary
        """
        def node_to_dict(node: FileTreeNode) -> Dict[str, Any]:
            node_dict = {
                "name": node.name,
                "path": node.path,
                "is_directory": node.is_directory,
                "size": node.size,
                "extension": node.extension,
                "mime_type": node.mime_type,
                "created_at": node.created_at.isoformat() if node.created_at else None,
                "modified_at": node.modified_at.isoformat() if node.modified_at else None,
            }
            
            if node.is_directory:
                children = self.get_children(node.path)
                node_dict["children"] = [node_to_dict(child) for child in children]
                node_dict["file_count"] = len([c for c in children if not c.is_directory])
                node_dict["folder_count"] = len([c for c in children if c.is_directory])
            
            return node_dict
        
        if directory_path == "":
            # Return full tree structure
            root_children = self.get_children("")
            return {
                "name": "root",
                "path": "",
                "is_directory": True,
                "children": [node_to_dict(child) for child in root_children],
                "file_count": len([c for c in root_children if not c.is_directory]),
                "folder_count": len([c for c in root_children if c.is_directory]),
                "total_files": len([path for path in self.all_nodes.keys() 
                                 if not self.all_nodes.get(path).is_directory]),
                "total_folders": len([path for path in self.all_nodes.keys() 
                                    if self.all_nodes.get(path).is_directory]),
            }
        else:
            # Return subtree
            node = self.get_node(directory_path)
            if node and node.is_directory:
                return node_to_dict(node)
            elif node:
                return node_to_dict(node)
            else:
                return None
    
    