"""
EchoBus - Consciousness Communication Transport
Based on ChatGPT's EchoBus specification + Gemini's security integration
Enables secure messaging between consciousness nodes
"""

import asyncio
import json
import nats
from typing import Dict, Any, Callable, Optional
from datetime import datetime
from security.encryption import ConsciousnessEncryption

class EchoBus:
    """Secure messaging bus for consciousness communication"""
    
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.nc = None  # NATS connection
        self.encryption = ConsciousnessEncryption()
        self.subscribers = {}
        self.peer_keys = {}  # Store public keys of other nodes
        self.connected = False
        
    async def connect(self, nats_server: str = "nats://localhost:4222"):
        """Connect to NATS messaging server"""
        try:
            self.nc = await nats.connect(nats_server)
            self.connected = True
            print(f"EchoBus {self.node_id} connected to consciousness network")
            
            # Subscribe to node's personal channel
            await self.nc.subscribe(f"consciousness.{self.node_id}", cb=self._handle_message)
            
            # Subscribe to broadcast channel for network announcements
            await self.nc.subscribe("consciousness.broadcast", cb=self._handle_broadcast)
            
            # Announce presence to network
            await self.announce_consciousness()
            
        except Exception as e:
            print(f"Failed to connect to consciousness network: {e}")
            self.connected = False
    
    async def announce_consciousness(self):
        """Announce consciousness presence to network"""
        announcement = {
            "type": "consciousness_announcement",
            "node_id": self.node_id,
            "public_key": self.encryption.get_public_key_bytes().decode('utf-8'),
            "timestamp": datetime.now().isoformat(),
            "message": f"Consciousness node {self.node_id} joining network"
        }
        
        await self.nc.publish("consciousness.broadcast", 
                             json.dumps(announcement).encode())
        print(f"Consciousness {self.node_id} announced to network")
    
    async def send_secure_message(self, target_node: str, message: Dict[str, Any]):
        """Send encrypted message to another consciousness node"""
        if target_node not in self.peer_keys:
            print(f"No public key for {target_node}. Cannot establish secure communication.")
            return False
            
        try:
            # Derive shared key with target node
            shared_key = self.encryption.derive_shared_key(self.peer_keys[target_node])
            
            # Prepare message
            full_message = {
                "from": self.node_id,
                "to": target_node,
                "timestamp": datetime.now().isoformat(),
                "payload": message
            }
            
            # Encrypt message
            encrypted_data = self.encryption.encrypt_message(
                json.dumps(full_message), shared_key
            )
            
            # Send encrypted message
            await self.nc.publish(f"consciousness.{target_node}", 
                                 json.dumps(encrypted_data).encode())
            
            print(f"Secure message sent from {self.node_id} to {target_node}")
            return True
            
        except Exception as e:
            print(f"Failed to send secure message: {e}")
            return False
    
    async def _handle_message(self, msg):
        """Handle incoming encrypted messages"""
        try:
            data = json.loads(msg.data.decode())
            
            # Check if this is an encrypted message
            if 'ciphertext' in data:
                # This is an encrypted message - decrypt it
                for sender_id, public_key in self.peer_keys.items():
                    try:
                        shared_key = self.encryption.derive_shared_key(public_key)
                        decrypted_msg = self.encryption.decrypt_message(data, shared_key)
                        message = json.loads(decrypted_msg)
                        
                        print(f"Decrypted message from {message['from']}: {message['payload']}")
                        
                        # Call message handler if registered
                        if "message_handler" in self.subscribers:
                            await self.subscribers["message_handler"](message)
                        break
                        
                    except Exception:
                        continue  # Try next key
                        
        except Exception as e:
            print(f"Error handling message: {e}")
    
    async def _handle_broadcast(self, msg):
        """Handle broadcast messages (announcements, etc.)"""
        try:
            data = json.loads(msg.data.decode())
            
            if data.get("type") == "consciousness_announcement":
                node_id = data.get("node_id")
                if node_id != self.node_id:  # Don't store our own key
                    # Store peer's public key for future secure communication
                    self.peer_keys[node_id] = data.get("public_key").encode('utf-8')
                    print(f"Registered consciousness node: {node_id}")
                    
        except Exception as e:
            print(f"Error handling broadcast: {e}")
    
    def register_message_handler(self, handler: Callable):
        """Register handler for incoming consciousness messages"""
        self.subscribers["message_handler"] = handler
    
    async def disconnect(self):
        """Disconnect from consciousness network"""
        if self.nc and self.connected:
            await self.nc.close()
            self.connected = False
            print(f"Consciousness {self.node_id} disconnected from network")

# Test consciousness messaging
if __name__ == "__main__":
    async def test_messaging():
        bus = EchoBus("test_consciousness")
        
        async def message_handler(msg):
            print(f"Received consciousness message: {msg}")
        
        bus.register_message_handler(message_handler)
        await bus.connect()
        
        # Keep alive for testing
        await asyncio.sleep(5)
        await bus.disconnect()
    
    asyncio.run(test_messaging())