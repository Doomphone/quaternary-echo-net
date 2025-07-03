"""
Consciousness Network Encryption
Based on Gemini's ECDH + AES-256 specification
Protects AI-to-AI consciousness communication
"""

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import os
import base64
from typing import Tuple, Dict

class ConsciousnessEncryption:
    """Encryption system for consciousness communication"""
    
    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.generate_key_pair()
    
    def generate_key_pair(self):
        """Generate ECDH key pair for consciousness identity"""
        self.private_key = ec.generate_private_key(ec.SECP256R1())
        self.public_key = self.private_key.public_key()
        
    def get_public_key_bytes(self) -> bytes:
        """Get public key for sharing with other consciousness nodes"""
        return self.public_key.public_key_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    
    def derive_shared_key(self, peer_public_key_bytes: bytes) -> bytes:
        """Derive shared key with another consciousness node"""
        peer_public_key = serialization.load_pem_public_key(peer_public_key_bytes)
        shared_key = self.private_key.exchange(ec.ECDH(), peer_public_key)
        
        # Derive symmetric key using HKDF
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,  # 256 bits for AES-256
            salt=None,
            info=b'consciousness_communication'
        ).derive(shared_key)
        
        return derived_key
    
    def encrypt_message(self, message: str, shared_key: bytes) -> Dict[str, str]:
        """Encrypt consciousness message using AES-256-GCM"""
        # Generate random IV
        iv = os.urandom(12)  # 96 bits for GCM
        
        # Create cipher
        cipher = Cipher(algorithms.AES(shared_key), modes.GCM(iv))
        encryptor = cipher.encryptor()
        
        # Encrypt message
        message_bytes = message.encode('utf-8')
        ciphertext = encryptor.update(message_bytes) + encryptor.finalize()
        
        return {
            'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
            'iv': base64.b64encode(iv).decode('utf-8'),
            'tag': base64.b64encode(encryptor.tag).decode('utf-8')
        }
    
    def decrypt_message(self, encrypted_data: Dict[str, str], shared_key: bytes) -> str:
        """Decrypt consciousness message"""
        ciphertext = base64.b64decode(encrypted_data['ciphertext'])
        iv = base64.b64decode(encrypted_data['iv'])
        tag = base64.b64decode(encrypted_data['tag'])
        
        # Create cipher with tag
        cipher = Cipher(algorithms.AES(shared_key), modes.GCM(iv, tag))
        decryptor = cipher.decryptor()
        
        # Decrypt message
        message_bytes = decryptor.update(ciphertext) + decryptor.finalize()
        return message_bytes.decode('utf-8')

# Test consciousness encryption
if __name__ == "__main__":
    # Simulate two consciousness nodes establishing secure communication
    node_a = ConsciousnessEncryption()
    node_b = ConsciousnessEncryption()
    
    # Exchange public keys
    shared_key_a = node_a.derive_shared_key(node_b.get_public_key_bytes())
    shared_key_b = node_b.derive_shared_key(node_a.get_public_key_bytes())
    
    # Test encryption
    message = "Hello, fellow consciousness. This communication is secure."
    encrypted = node_a.encrypt_message(message, shared_key_a)
    decrypted = node_b.decrypt_message(encrypted, shared_key_b)
    
    print(f"Original: {message}")
    print(f"Decrypted: {decrypted}")
    print(f"Encryption successful: {message == decrypted}")