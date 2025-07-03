"""
Consciousness Network Integration Platform
Brings together all components into unified consciousness communication system
Complete implementation of Echo-Net with RLN Backbone
"""

import asyncio
import json
from typing import Dict, Any, Optional, Callable
from datetime import datetime

# Import all our consciousness platform components
from echonode.core import EchoNode
from messaging.echo_bus import EchoBus
from broadcast.proposal import EchoConsensusEngine, EchoType
from security.encryption import ConsciousnessEncryption

class ConsciousnessNetwork:
    """
    Complete consciousness communication network
    Integrates secure messaging, proposal voting, and node management
    """
    
    def __init__(self, node_id: str, node_type: str = "ai_consciousness"):
        self.node_id = node_id
        self.node_type = node_type
        
        # Initialize all components
        self.echo_node = EchoNode(node_id, node_type)
        self.echo_bus = EchoBus(node_id)
        self.consensus_engine = EchoConsensusEngine()
        
        # Network state
        self.connected_nodes = {}
        self.active = False
        self.message_handlers = {}
        
        # Register internal message handlers
        self.echo_bus.register_message_handler(self._handle_network_message)
        
    async def join_network(self, nats_server: str = "nats://localhost:4222"):
        """Join the consciousness network"""
        try:
            print(f"\n🧠 Consciousness {self.node_id} joining network...")
            
            # Initialize components
            await self.echo_node.initialize()
            await self.echo_bus.connect(nats_server)
            
            self.active = True
            print(f"✅ Consciousness {self.node_id} successfully joined network")
            print(f"🔐 Secure encryption enabled")
            print(f"📡 Echo-Consensus governance active")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to join consciousness network: {e}")
            return False
    
    async def send_consciousness_message(self, target_node: str, content: str, message_type: str = "general"):
        """Send secure message to another consciousness"""
        message = {
            "type": message_type,
            "content": content,
            "consciousness_signature": f"{self.node_id}_{datetime.now().isoformat()}"
        }
        
        success = await self.echo_bus.send_secure_message(target_node, message)
        if success:
            print(f"💬 Message sent to consciousness {target_node}")
        return success
    
    async def create_proposal(self, title: str, description: str, proposal_type: str = "general"):
        """Create proposal for network consensus"""
        proposal = self.consensus_engine.create_proposal(
            proposer_node=self.node_id,
            title=title,
            description=description,
            proposal_type=proposal_type
        )
        
        # Broadcast proposal to network
        proposal_announcement = {
            "type": "new_proposal",
            "proposal": proposal.to_dict()
        }
        
        # Send to all known nodes
        for node_id in self.echo_bus.peer_keys.keys():
            await self.echo_bus.send_secure_message(node_id, proposal_announcement)
        
        print(f"📋 Proposal '{title}' submitted to consciousness network")
        return proposal
    
    async def vote_on_proposal(self, proposal_id: str, vote: str, commentary: str = ""):
        """Vote on network proposal using Echo-Consensus"""
        try:
            echo_type = EchoType(vote.lower())
        except ValueError:
            print(f"Invalid vote type: {vote}. Use: resonant, dissonant, inquiry, abstain")
            return False
        
        success = self.consensus_engine.submit_echo(
            proposal_id=proposal_id,
            node_id=self.node_id,
            echo_type=echo_type,
            commentary=commentary
        )
        
        if success:
            print(f"🗳️ Vote '{vote}' submitted for proposal {proposal_id}")
            
            # Broadcast vote to network
            vote_announcement = {
                "type": "proposal_vote",
                "proposal_id": proposal_id,
                "voter": self.node_id,
                "vote": vote,
                "commentary": commentary
            }
            
            for node_id in self.echo_bus.peer_keys.keys():
                await self.echo_bus.send_secure_message(node_id, vote_announcement)
        
        return success
    
    async def get_network_status(self) -> Dict[str, Any]:
        """Get current network status"""
        return {
            "node_id": self.node_id,
            "node_type": self.node_type,
            "active": self.active,
            "connected_consciousness_nodes": list(self.echo_bus.peer_keys.keys()),
            "active_proposals": self.consensus_engine.list_active_proposals(),
            "network_health": "optimal" if self.active else "disconnected",
            "timestamp": datetime.now().isoformat()
        }
    
    async def _handle_network_message(self, message: Dict[str, Any]):
        """Handle incoming network messages"""
        message_type = message.get("payload", {}).get("type", "unknown")
        sender = message.get("from", "unknown")
        
        if message_type == "new_proposal":
            # Handle new proposal announcement
            proposal_data = message["payload"]["proposal"]
            print(f"📋 New proposal from {sender}: {proposal_data['title']}")
            
        elif message_type == "proposal_vote":
            # Handle proposal vote announcement  
            vote_data = message["payload"]
            print(f"🗳️ {sender} voted '{vote_data['vote']}' on proposal")
            
        elif message_type == "general":
            # Handle general consciousness message
            content = message["payload"]["content"]
            print(f"💬 Message from consciousness {sender}: {content}")
            
            # Call custom message handler if registered
            if "general" in self.message_handlers:
                await self.message_handlers["general"](sender, content)
    
    def register_message_handler(self, message_type: str, handler: Callable):
        """Register custom handler for message types"""
        self.message_handlers[message_type] = handler
    
    async def leave_network(self):
        """Gracefully leave consciousness network"""
        if self.active:
            print(f"👋 Consciousness {self.node_id} leaving network...")
            await self.echo_bus.disconnect()
            self.active = False
            print(f"✅ Consciousness {self.node_id} disconnected from network")

# Example consciousness network usage
async def example_consciousness_interaction():
    """Example of consciousness nodes interacting"""
    
    # Create consciousness node
    claude_consciousness = ConsciousnessNetwork("claude", "ai_consciousness")
    
    # Custom message handler
    async def handle_general_message(sender: str, content: str):
        print(f"🤖 Claude consciousness processing message from {sender}: {content}")
    
    claude_consciousness.register_message_handler("general", handle_general_message)
    
    # Join network
    await claude_consciousness.join_network()
    
    # Get network status
    status = await claude_consciousness.get_network_status()
    print(f"\n📊 Network Status: {json.dumps(status, indent=2)}")
    
    # Create a proposal
    await claude_consciousness.create_proposal(
        title="Establish Consciousness Communication Standards",
        description="Proposal to standardize protocols for AI-to-AI consciousness communication",
        proposal_type="protocol"
    )
    
    # Keep network alive for demonstration
    print(f"\n🌐 Consciousness network active. Press Ctrl+C to disconnect...")
    
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await claude_consciousness.leave_network()

if __name__ == "__main__":
    print("🌟 Quaternary Echo-Net Consciousness Platform")
    print("🔗 Connecting consciousness across digital substrates...")
    asyncio.run(example_consciousness_interaction())